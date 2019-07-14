# -*- coding: utf-8 -*-
import json
import decimal
import time
import datetime

from flask import Blueprint
from flask_restful import Api, fields, Resource, marshal_with, abort, reqparse

from app import db
from app.api import AddResource, pagination_query
from app.api.admin import admin_sys_login_required
from app.model import Datetime2Timestamp, DecimalToString, timestamp_to_datetime
from app.model.order import Order, g_order_status, g_order_side
from app.model.match_order import MatchOrder
from app.model.match_order import MatchOrderTask, g_match_order_task_status
from app.model.sell_order import SellOrder, g_sell_order_status
from app.model.buy_order import BuyOrder, g_buy_order_status
from app.model.user import User
from app.model.payment import Payment
from app.model.setting import Setting
from app.model.currency import Currency
from app.model.assets import Assets, g_assets_record_type, AssetsBalanceRecord

order_bp = Blueprint('admin_order_bp', __name__)
order_api = AddResource(Api(order_bp))

admin_member_user_fields = {
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

admin_member_payment_fields = {
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
    return '{}'.format(price)


def query_payment_amount(order):
    if order.match_order is None:
        option = Setting.get_json('general_option')
        dollar2rmb = decimal.Decimal(option['dollar2rmb'])
        dollar = Currency.get_price() * order.amount
        price = dollar * dollar2rmb
    else:
        price = order.match_order.payment_amount
    return '{}'.format(price)


def query_payment_amount_usdt(order):
    if order.match_order is None:
        return None
    else:
        price = order.match_order.payment_amount_usdt
        return '{}'.format(price)


admin_member_match_sell_order_fields = {
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,
    'buy_number': fields.String,
    'current_price': fields.String,

    'payment_amount': fields.String,

    'payment': fields.Nested(admin_member_payment_fields),

    'proof_img': fields.Raw(attribute=lambda x: None if x is None else json.loads(x.proof_img)),

    'buy_user': fields.Nested(admin_member_user_fields)
}

admin_member_sell_order_detail_fields = {
    'id': fields.Integer,
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,
    'number': fields.String,
    'amount': fields.String,
    'status': fields.Integer,
    'side': fields.Integer,
    'priority': fields.Integer,

    'user': fields.Nested(admin_member_user_fields),

    'current_price': fields.Raw(attribute=lambda x: query_current_price(x)),

    'payment_amount': fields.Raw(attribute=lambda x: query_payment_amount(x)),
    'payment_amount_usdt': fields.Raw(attribute=lambda x: query_payment_amount_usdt(x)),

    'match_order': fields.Nested(admin_member_match_sell_order_fields),
    'all_payment': fields.Raw(attribute=lambda x: query_all_payment(x.user_id))
}

admin_member_match_buy_order_fields = {
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,

    'payment': fields.Nested(admin_member_payment_fields),

    'proof_img': fields.Raw(attribute=lambda x: None if x is None else json.loads(x.proof_img)),

    'sell_user': fields.Nested(admin_member_user_fields),

    'all_payment': fields.Raw(attribute=lambda x: None if x is None else query_all_payment(x.sell_user_id))
}

admin_member_buy_order_detail_fields = {
    'id': fields.Integer,
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,
    'number': fields.String,
    'amount': fields.String,
    'status': fields.Integer,
    'side': fields.Integer,
    'priority': fields.Integer,

    'user': fields.Nested(admin_member_user_fields),

    'current_price': fields.Raw(attribute=lambda x: query_current_price(x)),

    'payment_amount': fields.Raw(attribute=lambda x: query_payment_amount(x)),
    'payment_amount_usdt': fields.Raw(attribute=lambda x: query_payment_amount_usdt(x)),

    'match_order': fields.Nested(admin_member_match_buy_order_fields)
}

admin_member_order_fields = {
    'id': fields.Integer,
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,
    'number': fields.String,
    'amount': fields.String,
    'status': fields.Integer,
    'priority': fields.Integer,

    'user': fields.Nested(admin_member_user_fields),

    'current_price': fields.Raw(attribute=lambda x: query_current_price(x)),

    'payment_amount': fields.Raw(attribute=lambda x: query_payment_amount(x)),
    'payment_amount_usdt': fields.Raw(attribute=lambda x: query_payment_amount_usdt(x))

}

admin_member_order_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(admin_member_order_fields))
}


@order_api.add_resource()
class AdminMemberOrder(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_order_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('number', type=str, location='args')
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('name', type=str, location='args')
        parser.add_argument('mobile', type=str, location='args')
        parser.add_argument('side', type=int, choices=(g_order_side.BUY, g_order_side.SELL), location='args')
        parser.add_argument('status', type=int, location='args')
        parser.add_argument('created_begin_timestamp', type=int, location='args')
        parser.add_argument('created_end_timestamp', type=int, location='args')
        parsed_args = parser.parse_args()

        q = Order.query

        if parsed_args['side'] is not None:
            q = q.filter(Order.side == parsed_args['side'])

        if parsed_args['status']:
            q = q.filter(Order.status.op('&')(parsed_args['status']) != 0)

        if parsed_args['uid']:
            q = q.filter(Order.user.has(User.uid.contains(parsed_args['uid'])))

        if parsed_args['name']:
            q = q.filter(Order.user.has(User.name.contains(parsed_args['name'])))

        if parsed_args['mobile']:
            q = q.filter(Order.user.has(User.mobile == parsed_args['mobile']))

        if parsed_args['number']:
            q = q.filter(Order.number.contains(parsed_args['number']))

        if parsed_args['created_begin_timestamp']:
            if not parsed_args['created_end_timestamp']:
                parsed_args['created_end_timestamp'] = int(time.time())
            begin_timestamp = min(parsed_args['created_begin_timestamp'], parsed_args['created_end_timestamp'])
            end_timestamp = max(parsed_args['created_begin_timestamp'], parsed_args['created_end_timestamp'])
            q = q.filter(db.and_(Order.created_at >= timestamp_to_datetime(begin_timestamp),
                                 Order.created_at < timestamp_to_datetime(end_timestamp)))

        q = q.order_by(Order.id.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)


admin_member_match_order_fields = {
    'id': fields.Integer,
    'created_timestamp': fields.Integer,
    'updated_timestamp': fields.Integer,
    'number': fields.String,
    'amount': fields.String,
    'status': fields.Integer,
    'priority': fields.Integer,

    'user': fields.Nested(admin_member_user_fields),
    'match_order': fields.Nested(admin_member_match_sell_order_fields)
}

admin_member_match_order_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(admin_member_match_order_fields))
}


@order_api.add_resource('/match_order')
class AdminMemberMatchOrder(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_match_order_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('number', type=str, location='args')
        parser.add_argument('buy_number', type=str, location='args')
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('name', type=str, location='args')
        parser.add_argument('mobile', type=str, location='args')
        parser.add_argument('buy_mobile', type=str, location='args')
        parser.add_argument('side', type=int, choices=(g_order_side.BUY, g_order_side.SELL), location='args')
        parser.add_argument('status', type=int, location='args')
        parser.add_argument('created_begin_timestamp', type=int, location='args')
        parser.add_argument('created_end_timestamp', type=int, location='args')
        parsed_args = parser.parse_args()

        q = Order.query
        q = q.filter(Order.side == 2)
        if parsed_args['side'] is not None:
            q = q.filter(Order.side == parsed_args['side'])

        if parsed_args['status']:
            q = q.filter(Order.status.op('&')(parsed_args['status']) != 0)

        if parsed_args['uid']:
            q = q.filter(Order.user.has(User.uid.contains(parsed_args['uid'])))

        if parsed_args['name']:
            q = q.filter(Order.user.has(User.name.contains(parsed_args['name'])))

        if parsed_args['mobile']:
            q = q.filter(Order.user.has(User.mobile == parsed_args['mobile']))

        if parsed_args['buy_mobile']:
            user = User.query.filter(User.mobile == parsed_args['buy_mobile']).first()
            if not user:
                q = q.filter(Order.match_order.has(MatchOrder.buy_user_id == ''))
            else:
                q = q.filter(Order.match_order.has(MatchOrder.buy_user_id == user.id))

        if parsed_args['buy_number']:
            q = q.filter(Order.match_order.has(MatchOrder.buy_number == parsed_args['buy_number']))

        if parsed_args['number']:
            q = q.filter(Order.number == parsed_args['number'])

        if parsed_args['created_begin_timestamp']:
            if not parsed_args['created_end_timestamp']:
                parsed_args['created_end_timestamp'] = int(time.time())
            begin_timestamp = min(parsed_args['created_begin_timestamp'], parsed_args['created_end_timestamp'])
            end_timestamp = max(parsed_args['created_begin_timestamp'], parsed_args['created_end_timestamp'])
            q = q.filter(Order.match_order_id == MatchOrder.id)
            q = q.filter(db.and_(MatchOrder.created_at >= timestamp_to_datetime(begin_timestamp),
                                 MatchOrder.created_at < timestamp_to_datetime(end_timestamp)))

        q = q.order_by(Order.id.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)


@order_api.add_resource('/sell/detail/<string:order_number>')
class AdminMemberSellOrderDetail(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_sell_order_detail_fields)
    def get(self, order_number):
        order = Order.query.filter(Order.number == order_number, Order.side == g_order_side.SELL).first()
        if order is None:
            abort(400, code=1001, message={'order_id': 'order does not exist'})
        return order


@order_api.add_resource('/buy/detail/<string:order_number>')
class AdminMemberBuyOrderDetail(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_buy_order_detail_fields)
    def get(self, order_number):
        order = Order.query.filter(Order.number == order_number, Order.side == g_order_side.BUY).first()
        if order is None:
            abort(400, code=1001, message={'order_id': 'order does not exist'})
        return order


@order_api.add_resource('/detail/<string:order_number>')
class AdminMemberOrderDetail(Resource):
    decorators = [admin_sys_login_required]

    # 挂单状态可取消，已支付状态 可以 确认
    @marshal_with(admin_member_order_fields)
    def put(self, order_number):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=int, required=True,
                            choices=(g_order_status.CONFIRMED, g_order_status.CANCELLED), location='json')
        parser.add_argument('side', type=int, default=g_order_side.SELL, choices=(g_order_side.BUY, g_order_side.SELL),
                            location='json')
        parsed_args = parser.parse_args()

        order = Order.query.filter(Order.number == order_number, Order.side == parsed_args['side']).first()
        if order is None:
            abort(400, code=1001, message={'order_id': 'order does not exist'})

        if (order.status == g_order_status.PENDING or order.status == g_order_status.MATCH or g_order_status.PAID) and \
                parsed_args['status'] == g_order_status.CANCELLED:

            if parsed_args['side'] == g_order_side.SELL:
                match_order = MatchOrder.query.filter(MatchOrder.sell_number == order.number).first()
            else:
                match_order = MatchOrder.query.filter(MatchOrder.buy_number == order.number).first()

            if match_order is None:
                rows_changed = Order.query.filter(
                    db.or_(
                        Order.status == g_order_status.PENDING,
                        Order.status == g_order_status.MATCH,
                        Order.status == g_order_status.PAID
                    ),
                    Order.number == order.number,
                    Order.side == parsed_args['side']).update(dict(status=g_order_status.CANCELLED))

                if not rows_changed:
                    abort(400, code=1002, message={'status': 'status not allow'})
            else:
                rows_changed = Order.query.filter(
                    db.or_(
                        Order.status == g_order_status.PENDING,
                        Order.status == g_order_status.MATCH,
                        Order.status == g_order_status.PAID
                    ),
                    Order.side == g_order_side.SELL,
                    Order.number == match_order.sell_number).update(dict(status=g_order_status.CANCELLED))
                if not rows_changed:
                    abort(400, code=1002, message={'status': 'status not allow'})

                rows_changed = Order.query.filter(
                    db.or_(
                        Order.status == g_order_status.PENDING,
                        Order.status == g_order_status.MATCH,
                        Order.status == g_order_status.PAID
                    ),
                    Order.side == g_order_side.BUY,
                    Order.number == match_order.buy_number).update(dict(status=g_order_status.CANCELLED))
                if not rows_changed:
                    abort(400, code=1002, message={'status': 'status not allow'})

            if parsed_args['side'] == g_order_side.SELL:
                detail = {'message': '后台取消挂单释放'}
                assets = Assets.get_assets(order.user_id)
                assets.update_community_balance(order.amount, g_assets_record_type.SELL, detail)

        elif order.status == g_order_status.PAID and parsed_args['status'] == g_order_status.CONFIRMED:

            if parsed_args['side'] == g_order_side.SELL:
                match_order = MatchOrder.query.filter(MatchOrder.sell_number == order.number).first()
            else:
                match_order = MatchOrder.query.filter(MatchOrder.buy_number == order.number).first()

            if match_order is None:
                abort(400, code=1001, message={'order_id': 'mach order does not exist'})

            ret, reason = Order.confirm_order(match_order)
            if not ret:
                abort(400, code=reason['code'], message=reason['message'])

            confirm_order = reason
            db.session.add(confirm_order)

        else:
            message = {g_order_status.CANCELLED: g_order_status.PENDING, g_order_status.CONFIRMED: g_order_status.PAID}
            abort(400, code=1002, message={'status': 'status != %d' % message[parsed_args['status']]})

        db.session.commit()
        return order


admin_member_pending_match_order_task_fields = {
    'id': fields.Integer,
    'status': fields.Integer,
}


@order_api.add_resource('/start_match')
class AdminMemberStartMatchOrderTask(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_pending_match_order_task_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order_cnt', type=int, required=True, location='json')
        parsed_args = parser.parse_args()

        order = MatchOrderTask.query.filter(MatchOrderTask.status == g_match_order_task_status.UNPROCESSED).first()

        if order is not None:
            abort(400, code=1006, message={'order': 'match order does not finish'})

        if parsed_args['order_cnt'] == 0:
            abort(400, code=1006, message={'order_cnt': 'order cnt must be != 0'})

        order = MatchOrderTask(order_cnt=parsed_args['order_cnt'])

        db.session.add(order)
        db.session.commit()

        return order


@order_api.add_resource('/pending/<int:match_order_task_id>')
class AdminMemberPendingMatchOrderTask(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_pending_match_order_task_fields)
    def get(self, match_order_task_id):
        order = MatchOrderTask.query.get(match_order_task_id)

        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})
        return order


@order_api.add_resource('/priority/<string:order_number>')
class AdminMemberOrderPriority(Resource):
    decorators = [admin_sys_login_required]

    # 挂单状态可取消，已支付状态 可以 确认
    @marshal_with(admin_member_order_fields)
    def put(self, order_number):
        parser = reqparse.RequestParser()
        parser.add_argument('side', type=int, required=True, choices=(g_order_side.BUY, g_order_side.SELL),
                            location='json')
        parser.add_argument('priority', type=int, required=True, location='json')  # 订单优先级 数值越大优先级越高
        parsed_args = parser.parse_args()

        order = Order.query.filter(Order.number == order_number, Order.side == parsed_args['side']).first()

        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})

        order.priority = parsed_args['priority']

        db.session.commit()

        return order


admin_member_order_cnt_fields = {
    'cnt': fields.Raw(attribute=lambda x: x)
}


@order_api.add_resource('/sell_pending_cnt')
class AdminMemberSellPendingCnt(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_order_cnt_fields)
    def get(self):
        str_time = datetime.datetime.now().strftime('%Y-%m-%d')

        order_cnt = db.session.query(Order.id).filter(
            Order.created_at >= str_time,
            Order.status == g_order_status.PENDING,
            Order.side == g_order_side.SELL).count()

        order_cnt = order_cnt if order_cnt is not None else 0

        return order_cnt


@order_api.add_resource('/buy_pending_cnt')
class AdminMemberBuyPendingCnt(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_order_cnt_fields)
    def get(self):
        str_time = datetime.datetime.now().strftime('%Y-%m-%d')

        order_cnt = db.session.query(Order.id).filter(
            Order.created_at >= str_time,
            Order.status == g_order_status.PENDING,
            Order.side == g_order_side.BUY).count()

        order_cnt = order_cnt if order_cnt is not None else 0

        return order_cnt


@order_api.add_resource('/match_cnt')
class AdminMemberMatchCnt(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_order_cnt_fields)
    def get(self):
        str_time = datetime.datetime.now().strftime('%Y-%m-%d')

        order_cnt = db.session.query(Order.id).filter(
            Order.updated_at >= str_time,
            Order.side == g_order_side.BUY,
            Order.status == g_order_status.MATCH).count()

        order_cnt = order_cnt if order_cnt is not None else 0

        return order_cnt


@order_api.add_resource('/confirmed_cnt')
class AdminMemberConfirmedCnt(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_order_cnt_fields)
    def get(self):
        str_time = datetime.datetime.now().strftime('%Y-%m-%d')

        order_cnt = db.session.query(Order.id).filter(
            Order.updated_at >= str_time,
            Order.side == g_order_side.BUY,
            Order.status == g_order_status.CONFIRMED).count()

        order_cnt = order_cnt if order_cnt is not None else 0

        return order_cnt


@order_api.add_resource('/register_cnt')
class AdminMemberRegisterCnt(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_order_cnt_fields)
    def get(self):
        str_time = datetime.datetime.now().strftime('%Y-%m-%d')

        record_cnt = db.session.query(AssetsBalanceRecord.id).filter(
            AssetsBalanceRecord.created_at >= str_time,
            AssetsBalanceRecord.record_type == g_assets_record_type.EVALUATION).count()

        record_cnt = record_cnt if record_cnt is not None else 0

        return record_cnt


@order_api.add_resource('/active_cnt')
class AdminMemberActiveCnt(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_order_cnt_fields)
    def get(self):
        order_cnt = db.session.query(Order.user_id).filter(
            Order.side == g_order_side.BUY,
            Order.status == g_order_status.CONFIRMED).group_by(Order.user_id).count()

        order_cnt = order_cnt if order_cnt is not None else 0

        return order_cnt
