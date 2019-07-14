# -*- coding: utf-8 -*-
import decimal
import datetime
import json
import logging
from yunpian_python_sdk.ypclient import YunpianClient
from yunpian_python_sdk.model import constant as YC

from app.model import AutoIncrementBase, db
from app.model.user import User, g_user_transaction_level
from app.model.sell_order import SellOrder, g_sell_order_status
from app.model.buy_order import BuyOrder, g_buy_order_status
from app.model.match_order import MatchOrder, MatchOrderTask, g_match_order_task_status
from app.model.confirm_order import ConfirmOrder, g_confirm_order_status
from app.model.payment import Payment
from app.model.currency import CryptoCurrency
from app.model.setting import Setting
from app.model.currency import Currency
from app.model.assets import Assets, g_assets_record_type
from app.type.typedef_const import TypedefConst

g_order_status = TypedefConst()

g_order_status.PENDING = 1  # 挂单中
g_order_status.MATCH = 2  # 匹配中
g_order_status.PAID = 4  # 已付款
g_order_status.CONFIRMED = 8  # 已确认
g_order_status.CANCELLED = 16  # 已取消
g_order_status.DELETE = 32  # 删除

g_order_side = TypedefConst()

g_order_side.BUY = 1  # 买单
g_order_side.SELL = 2  # 卖单


class Order(AutoIncrementBase):
    match_order_id = db.Column(db.Integer, db.ForeignKey('match_order.id'), nullable=True)  # 匹配订单

    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)  # 用户
    side = db.Column(db.SmallInteger, nullable=False)  # 单类型 参见 g_order_side
    number = db.Column(db.String(16), nullable=False)

    amount = db.Column(db.Numeric(24, 8), nullable=False)  # 数量

    status = db.Column(db.SmallInteger, default=g_order_status.PENDING, nullable=False)  # 订单状态参见 g_order_status

    priority = db.Column(db.SmallInteger, default=0)  # 订单优先级 数值越大优先级越高

    user = db.relationship(User, foreign_keys=[user_id])
    match_order = db.relationship(MatchOrder, foreign_keys=[match_order_id])

    __table_args__ = (db.UniqueConstraint('side', 'number'),)

    @staticmethod
    def confirm_order(match_order):
        rows_changed = Order.query.filter_by(
            user_id=match_order.sell_user_id,
            side=g_order_side.SELL,
            number=match_order.sell_number,
            status=g_order_status.PAID).update(dict(status=g_order_status.CONFIRMED))
        if not rows_changed:
            return False, dict(code=1001, message={'order_number': 'order does not exist'})

        rows_changed = Order.query.filter_by(
            user_id=match_order.buy_user_id,
            side=g_order_side.BUY,
            number=match_order.buy_number,
            status=g_order_status.PAID).update(dict(status=g_order_status.CONFIRMED))
        if not rows_changed:
            return False, dict(code=1001, message={'order_number': 'order does not exist'})

        confirm_order = ConfirmOrder(sell_user_id=match_order.sell_user_id,
                                     buy_user_id=match_order.buy_user_id,
                                     amount=match_order.sell_order.amount)

        return True, confirm_order

    @staticmethod
    def generate_order_process():
        option = Setting.get_json('general_option')
        sell_people = option['sell_people']
        buy_people = option['buy_people']
        sell_count = option['sell_count']
        buy_count = option['buy_count']

        str_time = datetime.datetime.now().strftime('%Y-%m-%d')

        order_list = SellOrder.query.filter(SellOrder.status == g_sell_order_status.UNPROCESSED).all()
        buy_list = BuyOrder.query.filter(BuyOrder.status == g_buy_order_status.UNPROCESSED).all()

        order_list.extend(buy_list)

        order_list = sorted(order_list, key=lambda e: e.created_at)

        for item in order_list:
            logging.info('Order side:{}, id:{}'.format(item.side, item.id))

            if item.side == g_order_side.SELL:

                if item.user.transaction_level != g_user_transaction_level.ULTIMATE:

                    order = Order.query.filter(Order.user_id == item.user_id,
                                               Order.side == g_order_side.BUY,
                                               Order.status == g_order_status.CONFIRMED).first()
                    if not order:
                        # 提示语"该用户从未购买过"
                        error_details = dict(code=1001, message={'user': 'user does not have buy order'})
                        item.details = json.dumps(error_details)
                        item.status = g_sell_order_status.FAILED
                        db.session.commit()
                        continue

                    order_people = db.session.query(Order.user_id).filter(
                        Order.created_at >= str_time, Order.side == g_order_side.SELL,
                        Order.status != g_order_status.CANCELLED).count()
                    order_people = order_people if order_people else 0
                    if order_people >= sell_people:
                        # 提示语"当日入场单量已满"
                        error_details = dict(code=1003, message={'count': 'count >= {}'.format(sell_people)})
                        item.details = json.dumps(error_details)
                        item.status = g_sell_order_status.FAILED
                        db.session.commit()
                        continue

                    count = db.session.query(db.func.count(SellOrder.id)).filter(
                        db.func.date_format(SellOrder.created_at, '%Y-%m-%d') == str_time,
                        SellOrder.user_id == item.user_id,
                        SellOrder.status == g_sell_order_status.PROCESSED).first()[0]
                    count = count if count else 0
                    if count >= sell_count:
                        # 提示语"今天卖出的单数已满"
                        error_details = dict(code=1006, message={'user': 'today sell order >= {}'.format(sell_count)})
                        item.details = json.dumps(error_details)
                        item.status = g_sell_order_status.FAILED
                        db.session.commit()
                        continue

                detail = {'message': '挂单冻结'}
                assets = Assets.get_assets(item.user_id)
                if not assets.update_community_balance(-item.amount, g_assets_record_type.SELL, detail):
                    # 提示语"余额不足"
                    if assets.community_today_balance > 0:
                        error_details = dict(code=1007,
                                             message={
                                                 'order': 'please tomorrow to sell, today buy balance:{}'.format(
                                                     assets.community_today_balance)})
                    else:
                        error_details = dict(code=1008,
                                             message={'balance': 'current balance < {}'.format(item.amount)})
                    item.details = json.dumps(error_details)
                    item.status = g_sell_order_status.FAILED
                    db.session.commit()
                    continue

                item.status = g_sell_order_status.PROCESSED
            else:
                order_people = db.session.query(Order.user_id).filter(
                    Order.created_at >= str_time, Order.side == g_order_side.BUY,
                    Order.status != g_order_status.CANCELLED).count()
                order_people = order_people if order_people else 0
                if order_people >= buy_people:
                    # 提示语"当日入场单量已满"
                    error_details = dict(code=1003, message={'count': 'count >= {}'.format(buy_people)})
                    item.details = json.dumps(error_details)
                    item.status = g_sell_order_status.FAILED
                    db.session.commit()
                    continue

                # 用于计算今天买入的单数
                count = db.session.query(db.func.count(BuyOrder.id)).filter(
                    db.func.date_format(BuyOrder.created_at, '%Y-%m-%d') == str_time,
                    BuyOrder.user_id == item.user_id,
                    BuyOrder.status == g_buy_order_status.PROCESSED).first()[0]
                count = count if count else 0
                if count >= buy_count:
                    # 提示语"今天买入的单数已满"
                    error_details = dict(code=1006, message={'user': 'today buy order >= {}'.format(buy_count)})
                    item.details = json.dumps(error_details)
                    item.status = g_sell_order_status.FAILED
                    db.session.commit()
                    continue

                item.status = g_buy_order_status.PROCESSED

            order = Order(created_at=item.created_at,
                          user_id=item.user_id,
                          side=item.side,
                          amount=item.amount,
                          number=item.number)

            db.session.add(order)
            db.session.commit()

    @staticmethod
    def match_order_process():
        option = Setting.get_json('general_option')
        # match_order_cnt = option['match_order_cnt']
        dollar2rmb = decimal.Decimal(option['dollar2rmb'])

        task = MatchOrderTask.query.filter(MatchOrderTask.status == g_match_order_task_status.UNPROCESSED).first()
        if task is None:
            return

        change = MatchOrderTask.query.filter(MatchOrderTask.status == g_match_order_task_status.UNPROCESSED).update(
            dict(status=g_match_order_task_status.PROCESSED))
        if not change:
            return

        sell_list = Order.query.filter(
            Order.side == g_order_side.SELL, Order.status == g_order_status.PENDING)

        sell_list = sell_list.order_by(Order.priority.desc(), Order.created_at.asc())

        i = 0
        for item in sell_list:
            if i >= task.order_cnt:
                break

            buy_order = Order.query.filter(
                Order.side == g_order_side.BUY, Order.user_id != item.user_id,
                Order.status == g_order_status.PENDING).order_by(Order.priority.desc(), Order.created_at.asc()).first()

            if buy_order is None:
                continue

            change = Order.query.filter(Order.id == item.id, Order.status == g_order_status.PENDING).update(
                dict(status=g_order_status.MATCH))
            if not change:
                continue
            change = Order.query.filter(Order.id == buy_order.id, Order.status == g_order_status.PENDING).update(
                dict(status=g_order_status.MATCH))
            if not change:
                item.status = g_order_status.PENDING
                db.session.commit()
                continue

            usd_price = CryptoCurrency.query.filter(CryptoCurrency.currency_code == 'USDT').first().usd_price
            dollar = Currency.get_price() * item.amount
            usdt = dollar / usd_price

            order = MatchOrder(sell_user_id=item.user_id,
                               buy_user_id=buy_order.user_id,
                               sell_order_id=item.id,
                               buy_order_id=buy_order.id,
                               sell_number=item.number,
                               buy_number=buy_order.number,
                               payment_amount=dollar * dollar2rmb,
                               payment_amount_usdt=usdt,
                               current_price=Currency.get_price())
            db.session.add(order)
            db.session.flush()
            item.match_order_id = order.id
            buy_order.match_order_id = order.id
            db.session.commit()
            try:
                if order.buy_user.order_mobile:
                    clnt = YunpianClient('fcf725316cbb8ff1438c90ff76c6cebe')
                    param = {YC.MOBILE: '+' + order.buy_user.order_mobile.replace(' ', ''),
                             YC.TEXT: "【乐宝】您的订单{}已匹配成功，请尽快安排处理。".format('')}
                    clnt.sms().single_send(param)
            except:
                pass

            i += 1
        db.session.commit()

    @staticmethod
    def confirm_order_process():
        order_list = ConfirmOrder.query.filter(ConfirmOrder.status == g_confirm_order_status.UNPROCESSED).all()

        for order in order_list:
            change = ConfirmOrder.query.filter(
                ConfirmOrder.id == order.id, ConfirmOrder.status == g_confirm_order_status.UNPROCESSED).update(
                dict(status=g_confirm_order_status.PROCESSED))
            if not change:
                continue

            detail = {'message': '挂单交易'}
            assets = Assets.get_assets(order.buy_user_id)
            assets.update_community_today_balance(order.amount, g_assets_record_type.BUY, detail)

            # 用于计算一个买卖周期
            order.buy_user.buy_order_cnt += 1

            if order.sell_user.buy_order_cnt > 0:
                order.sell_user.buy_order_cnt -= 1
                option = Setting.get_json('general_option')
                buy_sell_free_amount = option['buy_sell_free_amount']
                buy_sell_rate = decimal.Decimal(option['buy_sell_rate'])
                fee = order.amount * buy_sell_rate
                amount = buy_sell_free_amount - fee
                detail = {
                    'message': '成功买卖各一单，释放数量：{}， 单数量：{}， 扣除手续费：{}'.format(
                        buy_sell_free_amount, order.amount, fee)
                }
                assets = Assets.get_assets(order.sell_user_id)
                if assets.update_total_balance(-buy_sell_free_amount, g_assets_record_type.BUY_SELL_FREE, detail):
                    assets.update_transaction_balance(amount, g_assets_record_type.BUY_SELL_FREE, detail)

                sell_user = order.sell_user
                sell_user.update_today_have_transaction()
                sell_user.update_transaction_free()

            currency = Currency.get_currency()
            currency.update_transaction_cnt()

            db.session.commit()

    @staticmethod
    def check_order_process():

        option = Setting.get_json('general_option')
        change_time = int(option['order_status_change_time'])

        # 接单后不打款
        q = db.session.query(Order).filter(Order.id == MatchOrder.sell_order_id,
                                           MatchOrder.created_at <
                                           datetime.datetime.now() - datetime.timedelta(hours=change_time),
                                           Order.status == g_order_status.MATCH).all()

        for order in q:
            match_order = order.match_order
            if match_order is None:
                continue

            rows_changed = Order.query.filter(
                Order.side == g_order_side.SELL,
                Order.number == match_order.sell_number,
                Order.status == g_order_status.MATCH).update(dict(status=g_order_status.CANCELLED))
            if not rows_changed:
                continue

            detail = {'message': "超时不打款,卖单号:{},买单号:{},买方手机:{}".format(match_order.sell_number,
                                                                      match_order.buy_number,
                                                                      match_order.buy_user.mobile)}
            rows_changed = Order.query.filter(
                Order.side == g_order_side.BUY,
                Order.number == match_order.buy_number,
                Order.status == g_order_status.MATCH).update(dict(status=g_order_status.CANCELLED))
            if rows_changed:
                assets = Assets.get_assets(order.user_id)
                assets.update_community_balance(order.amount, g_assets_record_type.SELL, detail)
            else:
                order.status = g_order_status.MATCH

            db.session.commit()

        # 打款后不确认
        # q = Order.query.filter(
        #     Order.paid_at > datetime.datetime.utcnow() - datetime.timedelta(hours=change_time),
        #     Order.status == g_order_status.PAID)
        #
        # detail = {'message': "付款后未确认超过时限, 时限为：{}".format(change_time)}
        # for order in q:
        #     rows_changed = Order.query.filter_by(
        #         number=order.number,
        #         status=g_order_status.PAID).update(dict(status=g_order_status.CONFIRMED, details=json.dumps(detail)))
        #     if rows_changed:
        #         assets = Assets.get_assets(order.match_user_id)
        #         assets.update_community_balance(order.amount, g_assets_record_type.BUY, detail)
        #
        #         # 用于计算一个买卖周期
        #         user = User.query.get(order.match_user_id)
        #         user.update_buy_order_cnt(1)
        #         user = User.query.get(order.user_id)
        #         rows_changed = user.update_buy_order_cnt(-1)
        #         if rows_changed:
        #             fee = order.amount * buy_sell_rate
        #             amount = buy_sell_free_amount - fee
        #             detail = {
        #                 'message': '成功买卖各一单，释放数量：{}， 单数量：{}， 扣除手续费：{}'.format(
        #                     buy_sell_free_amount, order.amount, fee)
        #             }
        #             assets = Assets.get_assets(user.id)
        #             if assets.update_total_balance(-buy_sell_free_amount, g_assets_record_type.BUY_SELL_FREE, detail):
        #                 assets.update_transaction_balance(amount, g_assets_record_type.BUY_SELL_FREE, detail)
        #
        #             user.update_today_have_transaction()
        #             user.update_transaction_free()
        #
        #         currency = Currency.get_currency()
        #         currency.update_transaction_cnt()
        #         db.session.commit()
