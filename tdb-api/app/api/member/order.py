# -*- coding: utf-8 -*-
import decimal
import logging
import json
import time

import datetime
from flask import Blueprint
from flask import g
from flask_restful import Api, fields, Resource, marshal_with, abort, reqparse
from yunpian_python_sdk.ypclient import YunpianClient
from yunpian_python_sdk.model import constant as YC

from app import db
from app.api import AddResource, pagination_query
from app.api.member import member_login_required
from app.model import Datetime2Timestamp, DecimalToString
from app.model.order import Order, g_order_status, g_order_side
from app.model.sell_order import SellOrder, g_sell_order_status
from app.model.buy_order import BuyOrder, g_buy_order_status
from app.model.match_order import MatchOrder
from app.model.confirm_order import ConfirmOrder
from app.model.setting import Setting
from app.model.currency import Currency, CryptoCurrency
from app.model.user import User, g_user_transaction_level
from app.model.assets import Assets, g_assets_record_type
from app.model.payment import Payment, g_payment_type

order_bp = Blueprint('member_order_bp', __name__)
order_api = AddResource(Api(order_bp))

member_user_fields = {
    'id': fields.String,
    'uid': fields.String,
    'mobile': fields.String,
    'email': fields.String,

    'order_mobile': fields.String,
    'avatar': fields.String,
    'name': fields.String,
    'nickname': fields.String,
    'gender': fields.Integer,
    'wechat': fields.String,
    'transaction_level': fields.Integer
}

member_payment_fields = {
    'id': fields.String,
    'type': fields.Integer,
    'name': fields.String,
    'bank': fields.String,
    'card_number': fields.String,
    'wechat': fields.String,
    'wechat_image': fields.String,
    'alipay': fields.String,
    'alipay_image': fields.String,
    'address': fields.String,
    'remark': fields.String,
    'invalid': fields.Integer
}


def query_all_payment(user_id):
    payment_list = Payment.get_all_payment(user_id)
    all_list = []
    for payment in payment_list:
        d = dict(id=payment.id, type=payment.type, name=payment.name, bank=payment.bank,
                 card_number=payment.card_number, wechat=payment.wechat, wechat_image=payment.wechat_image,
                 alipay=payment.alipay, alipay_image=payment.alipay_image, address=payment.address,
                 remark=payment.remark, invalid=payment.invalid)
        all_list.append(d)
    return all_list


def query_current_price(order):
    if order.match_order is None:
        price = Currency.get_price()
    else:
        price = order.match_order.current_price
    return '{0:.8f}'.format(price)


def query_payment_amount(order):
    if order.match_order is None:
        option = Setting.get_json('general_option')
        dollar2rmb = decimal.Decimal(option['dollar2rmb'])
        dollar = Currency.get_price() * order.amount
        price = dollar * dollar2rmb
    else:
        price = order.match_order.payment_amount
    return '{0:.8f}'.format(price)


def query_payment_amount_usdt(order):
    if order.match_order is None:
        return None
    else:
        price = order.match_order.payment_amount_usdt
        return '{0:.8f}'.format(price)


member_match_sell_order_fields = {
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,

    'payment': fields.Nested(member_payment_fields),

    'proof_img': fields.Raw(attribute=lambda x: None if x is None else json.loads(x.proof_img)),

    'buy_user': fields.Nested(member_user_fields)
}

member_sell_order_detail_fields = {
    'id': fields.Integer,
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,
    'number': fields.String,
    'amount': fields.String,
    'status': fields.Integer,
    'side': fields.Integer,
    'priority': fields.Integer,

    'user': fields.Nested(member_user_fields),

    'current_price': fields.Raw(attribute=lambda x: query_current_price(x)),

    'payment_amount': fields.Raw(attribute=lambda x: query_payment_amount(x)),
    'payment_amount_usdt': fields.Raw(attribute=lambda x: query_payment_amount_usdt(x)),

    'match_order': fields.Nested(member_match_sell_order_fields),
    'all_payment': fields.Raw(attribute=lambda x: query_all_payment(x.user_id))
}

member_match_buy_order_fields = {
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,

    'payment': fields.Nested(member_payment_fields),

    'proof_img': fields.Raw(attribute=lambda x: None if x is None else json.loads(x.proof_img)),

    'sell_user': fields.Nested(member_user_fields),

    'all_payment': fields.Raw(attribute=lambda x: None if x is None else query_all_payment(x.sell_user_id))
}

member_buy_order_detail_fields = {
    'id': fields.Integer,
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,
    'number': fields.String,
    'amount': fields.String,
    'status': fields.Integer,
    'side': fields.Integer,
    'priority': fields.Integer,

    'user': fields.Nested(member_user_fields),

    'current_price': fields.Raw(attribute=lambda x: query_current_price(x)),

    'payment_amount': fields.Raw(attribute=lambda x: query_payment_amount(x)),
    'payment_amount_usdt': fields.Raw(attribute=lambda x: query_payment_amount_usdt(x)),

    'match_order': fields.Nested(member_match_buy_order_fields)
}

member_order_fields = {
    'id': fields.Integer,
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,
    'number': fields.String,
    'amount': fields.String,
    'status': fields.Integer,
    'side': fields.Integer,
    'priority': fields.Integer,

    'user': fields.Nested(member_user_fields),

    'current_price': fields.Raw(attribute=lambda x: query_current_price(x)),

    'payment_amount': fields.Raw(attribute=lambda x: query_payment_amount(x)),
    'payment_amount_usdt': fields.Raw(attribute=lambda x: query_payment_amount_usdt(x))
}

member_order_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(member_order_fields))
}

member_pending_order_fields = {
    'id': fields.Integer,
    'number': fields.String,
    'status': fields.Integer,
    'details': fields.Raw(attribute=lambda x: json.loads(x.details))
}


@order_api.add_resource()
class MemberOrder(Resource):
    decorators = [member_login_required]

    @marshal_with(member_order_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('number', type=str, location='args')
        parser.add_argument('side', type=int, choices=(g_order_side.BUY, g_order_side.SELL), location='args')
        parser.add_argument('status', type=int, location='args')
        parsed_args = parser.parse_args()

        q = Order.query

        q = q.filter(Order.status != g_order_status.DELETE)

        q = q.filter(Order.user_id == g.current_user.id)

        if parsed_args['side'] is not None:
            q = q.filter(Order.side == parsed_args['side'])

        if parsed_args['status']:
            q = q.filter(Order.status.op('&')(parsed_args['status']) != 0)

        if parsed_args['number']:
            q = q.filter(Order.number.contains(parsed_args['number']))

        q = q.order_by(Order.id.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)


@order_api.add_resource('/sell')
class MemberSellOrder(Resource):
    decorators = [member_login_required]

    @marshal_with(member_pending_order_fields)
    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('price', type=decimal.Decimal, required=True, nullable=False, location='json')
        # parser.add_argument('amount', type=decimal.Decimal, required=True, nullable=False, location='json')
        parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        start_time = time.time()
        option = Setting.get_json('general_option')
        sell_amount = option['sell_amount']
        transaction_time_begin = [time.strptime(x, '%H:%M') for x in option['transaction_time_begin']]
        transaction_time_end = [time.strptime(x, '%H:%M') for x in option['transaction_time_end']]

        if not g.current_user.security_password:
            abort(400, code=1012, message={'security_password': 'security password is empty'})
        if not g.current_user.verify_security_password(parsed_args['security_password']):
            abort(400, code=1002, message={'security_password': 'security password does not match'})

        if g.current_user.allow_transaction == 0:
            abort(400, code=1006, message={'user': 'user does not allow transaction'})

        if g.current_user.transaction_level != g_user_transaction_level.ULTIMATE:

            time_now = time.strptime(time.strftime('%H:%M'), '%H:%M')
            if ((time_now < transaction_time_begin[0] or time_now > transaction_time_end[0]) and (
                    (time_now < transaction_time_begin[1] or time_now > transaction_time_end[1]))):
                abort(400, code=1006, message={'time': 'current time does not allow transaction'})

            order = SellOrder.query.filter(SellOrder.user_id == g.current_user.id,
                                           SellOrder.status == g_sell_order_status.UNPROCESSED).first()
            if order:
                return order

        ret, reason = SellOrder.order_create(g.current_user, sell_amount)
        if not ret:
            abort(400, code=reason['code'], message=reason['message'])

        order = reason
        db.session.add(order)
        db.session.commit()
        crl_time = time.time() - start_time
        logging.info('sell_crl_time:{}'.format(crl_time))

        return order


@order_api.add_resource('/buy')
class MemberBuyOrder(Resource):
    decorators = [member_login_required]

    @marshal_with(member_pending_order_fields)
    def post(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price', type=decimal.Decimal, required=True, nullable=False, location='json')
        # parser.add_argument('amount', type=decimal.Decimal, required=True, nullable=False, location='json')
        # parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        # parsed_args = parser.parse_args()

        start_time = time.time()
        option = Setting.get_json('general_option')
        buy_amount = option['sell_amount']
        transaction_time_begin = [time.strptime(x, '%H:%M') for x in option['transaction_time_begin']]
        transaction_time_end = [time.strptime(x, '%H:%M') for x in option['transaction_time_end']]

        # if not g.current_user.security_password:
        #     abort(400, code=1012, message={'security_password': 'security password is empty'})
        # if not g.current_user.verify_security_password(parsed_args['security_password']):
        #     abort(400, code=1002, message={'security_password': 'security password does not match'})

        time_now = time.strptime(time.strftime('%H:%M'), '%H:%M')
        if ((time_now < transaction_time_begin[0] or time_now > transaction_time_end[0]) and (
                (time_now < transaction_time_begin[1] or time_now > transaction_time_end[1]))):
            abort(400, code=1006, message={'time': 'current time does not allow transaction'})

        if g.current_user.allow_transaction == 0:
            abort(400, code=1006, message={'user': 'user does not allow transaction'})

        order = BuyOrder.query.filter(BuyOrder.user_id == g.current_user.id,
                                      BuyOrder.status == g_sell_order_status.UNPROCESSED).first()
        if order:
            return order

        # order = Order.query.filter(
        #   Order.match_user_id == g.current_user.id,
        #   Order.status.op('&')(g_order_status.CONFIRMED | g_order_status.CANCELLED) == 0).all()
        # if len(order) > 0:
        #     abort(400, code=1006, message={'user': 'user have order does not finish'})

        ret, reason = BuyOrder.order_create(g.current_user, buy_amount)
        if not ret:
            abort(400, code=reason['code'], message=reason['message'])

        order = reason
        db.session.add(order)
        db.session.commit()
        crl_time = time.time() - start_time
        logging.info('buy_crl_time:{}'.format(crl_time))

        return order


@order_api.add_resource('/pending/<int:order_id>')
class MemberPendingSellOrder(Resource):
    decorators = [member_login_required]

    @marshal_with(member_pending_order_fields)
    def get(self, order_id):
        parser = reqparse.RequestParser()
        parser.add_argument('side', type=int, required=True, choices=(g_order_side.BUY, g_order_side.SELL),
                            location='args')
        parsed_args = parser.parse_args()

        if parsed_args['side'] == g_order_side.SELL:
            order = SellOrder.query.filter(SellOrder.id == order_id, SellOrder.user_id == g.current_user.id).first()
        else:
            order = BuyOrder.query.filter(BuyOrder.id == order_id, BuyOrder.user_id == g.current_user.id).first()

        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})
        return order


# ################################# 卖单逻辑实现 ###################################
@order_api.add_resource('/sell/detail/<string:order_number>')
class MemberSellOrderDetail(Resource):
    decorators = [member_login_required]

    @marshal_with(member_sell_order_detail_fields)
    def get(self, order_number):
        order = Order.query.filter(Order.side == g_order_side.SELL, Order.number == order_number,
                                   Order.user_id == g.current_user.id).first()
        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})
        return order

    # 确认订单
    @marshal_with(member_sell_order_detail_fields)
    def post(self, order_number):
        parser = reqparse.RequestParser()
        parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        if not g.current_user.security_password:
            abort(400, code=1012, message={'security_password': 'security password is empty'})
        if not g.current_user.verify_security_password(parsed_args['security_password']):
            abort(400, code=1002, message={'security_password': 'security password does not match'})

        order = Order.query.filter(Order.side == g_order_side.SELL, Order.number == order_number,
                                   Order.user_id == g.current_user.id).first()
        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})

        match_order = order.match_order
        if match_order is None:
            abort(400, code=1001, message={'match_order': 'order does not match'})

        match_order.updated_at = datetime.datetime.now()
        ret, reason = Order.confirm_order(match_order)
        if not ret:
            abort(400, code=reason['code'], message=reason['message'])

        confirm_order = reason
        db.session.add(confirm_order)
        db.session.commit()
        return order

    # 取消挂单
    @marshal_with(member_order_fields)
    def delete(self, order_number):
        # parser = reqparse.RequestParser()
        # parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        # parsed_args = parser.parse_args()
        #
        # if not g.current_user.security_password:
        #     abort(400, code=1012, message={'security_password': 'security password is empty'})
        # if not g.current_user.verify_security_password(parsed_args['security_password']):
        #     abort(400, code=1002, message={'security_password': 'security password does not match'})

        order = Order.query.filter(
            Order.side == g_order_side.SELL, Order.number == order_number, Order.user_id == g.current_user.id).first()
        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})

        detail = {'message': '卖家取消挂单'}
        rows_changed = Order.query.filter_by(
            user_id=g.current_user.id,
            side=g_order_side.SELL,
            number=order_number,
            status=g_order_status.PENDING).update(dict(status=g_order_status.CANCELLED))
        if rows_changed == 1:
            assets = Assets.get_assets(order.user_id)
            assets.update_community_balance(order.amount, g_assets_record_type.SELL, detail)
        else:
            abort(400, code=1002, message={'status': 'status != g_order_status.PENDING'})

        db.session.commit()
        return order


# ################################# 买单逻辑实现 ###################################
@order_api.add_resource('/buy/detail/<string:order_number>')
class MemberBuyOrderDetail(Resource):
    decorators = [member_login_required]

    @marshal_with(member_buy_order_detail_fields)
    def get(self, order_number):
        order = Order.query.filter(Order.side == g_order_side.BUY, Order.number == order_number,
                                   Order.user_id == g.current_user.id).first()
        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})
        return order

    @marshal_with(member_buy_order_detail_fields)
    def put(self, order_number):
        parser = reqparse.RequestParser()
        parser.add_argument('proof_img', type=list, default=[], location='json')
        parser.add_argument('payment_id', type=str, required=True, location='json')
        parsed_args = parser.parse_args()

        order = Order.query.filter(Order.side == g_order_side.BUY, Order.number == order_number,
                                   Order.user_id == g.current_user.id).first()
        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})

        match_order = order.match_order

        if match_order is None:
            abort(400, code=1001, message={'match_order': 'order does not match'})

        payment = Payment.query.filter(Payment.id == parsed_args['payment_id'], Payment.invalid == 0).first()
        if payment is None:
            abort(400, code=1001, message={'payment': 'payment does not exist'})

        # 已支付
        rows_changed = Order.query.filter(
            Order.user_id == match_order.sell_user_id,
            Order.side == g_order_side.SELL,
            Order.number == match_order.sell_number,
            db.or_(Order.status == g_order_status.MATCH, Order.status == g_order_status.PAID)).update(
            dict(status=g_order_status.PAID))
        if not rows_changed:
            abort(400, code=1001, message={'order_number': 'order does not exist'})

        rows_changed = Order.query.filter(
            Order.user_id == match_order.buy_user_id,
            Order.side == g_order_side.BUY,
            Order.number == match_order.buy_number,
            db.or_(Order.status == g_order_status.MATCH, Order.status == g_order_status.PAID)).update(
            dict(status=g_order_status.PAID))
        if not rows_changed:
            abort(400, code=1001, message={'order_number': 'order does not exist'})

        match_order.proof_img = json.dumps(parsed_args['proof_img'])

        # order.payment_id = json.dumps(parsed_args['payment_id'])
        match_order.payment_id = payment.id
        db.session.commit()

        try:
            if match_order.sell_user.order_mobile:
                clnt = YunpianClient('fcf725316cbb8ff1438c90ff76c6cebe')
                param = {YC.MOBILE: '+' + match_order.sell_user.order_mobile.replace(' ', ''),
                         YC.TEXT: "【乐宝】您的订单{}已完成，请尽快安排确认。".format('')}
                clnt.sms().single_send(param)
        except:
            pass

        # db.session.commit()
        return order

    # 取消订单
    @marshal_with(member_order_fields)
    def delete(self, order_number):
        # parser = reqparse.RequestParser()
        # parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        # parsed_args = parser.parse_args()
        #
        # if not g.current_user.security_password:
        #     abort(400, code=1012, message={'security_password': 'security password is empty'})
        # if not g.current_user.verify_security_password(parsed_args['security_password']):
        #     abort(400, code=1002, message={'security_password': 'security password does not match'})

        order = Order.query.filter(
            Order.side == g_order_side.BUY, Order.number == order_number, Order.user_id == g.current_user.id).first()
        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})

        rows_changed = Order.query.filter_by(
            user_id=g.current_user.id,
            side=g_order_side.SELL,
            number=order_number,
            status=g_order_status.PENDING).update(dict(status=g_order_status.CANCELLED))
        if not rows_changed:
            abort(400, code=1002, message={'status': 'status != g_order_status.PENDING'})

        db.session.commit()
        return order
