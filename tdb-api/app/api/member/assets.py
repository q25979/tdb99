import decimal
import json
import datetime

from flask import Blueprint, g
from flask_restful import Api, fields, Resource, marshal_with, abort

from app.api import AddResource, CustomRequestParser, pagination_query
from app.api.member import member_login_required
from app.model import db, Datetime2Timestamp, timestamp_to_datetime, DecimalToString
from app.model.assets import Assets, AssetsBalanceRecord, g_assets_record_type, g_assets_type
from app.model.setting import Setting
from app.model.user import User

assets_bp = Blueprint('member_assets_bp', __name__)
assets_api = AddResource(Api(assets_bp))

member_assets_user_fields = {
    'id': fields.String,
    'uid': fields.String,
    'name': fields.String,
    'email': fields.String
}


def cal_community_balance(x):
    balance = x.community_balance + x.community_today_balance
    return '{0:.8f}'.format(decimal.Decimal(balance))


member_assets_fields = {
    'id': fields.String,
    'user': fields.Nested(member_assets_user_fields),
    'total_balance': DecimalToString,
    'community_balance': fields.Raw(attribute=lambda x: cal_community_balance(x)),
    'transaction_balance': DecimalToString,
    'grand_total_balance': DecimalToString,
    'community_frozen_balance': DecimalToString
}


@assets_api.add_resource('/query')
class MemberAssetsQueryApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_assets_fields)
    def get(self):
        assets = Assets.get_assets(g.current_user.id)
        return assets


member_assets_balance_record_fields = {
    'id': fields.Integer,
    'user': fields.Nested(member_assets_user_fields),
    'current_amount': DecimalToString,
    'delta_amount': DecimalToString,
    'assets_type': fields.Integer,
    'record_type': fields.Integer,
    'details': fields.Raw(attribute=lambda x: json.loads(x.details)),
    'created_at': Datetime2Timestamp
}

member_assets_balance_record_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(member_assets_balance_record_fields))
}


@assets_api.add_resource('/record/<int:record_id>')
class MemberAssetsBalanceRecordDetailsApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_assets_balance_record_fields)
    def get(self, record_id):
        record = AssetsBalanceRecord.query.get(record_id)
        if not record:
            abort(400, code=1001, message={'record': 'record does not exist'})
        return record


@assets_api.add_resource('/list')
class MemberAssetsBalanceRecordQueryApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_assets_balance_record_list_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('assets_type', type=int, location='args')
        parser.add_argument('record_type', type=int, location='args')
        parser.add_argument('create_begin_timestamp', type=int, location='args')
        parser.add_argument('create_end_timestamp', type=int, location='args')
        # delta_amount_flag用来查找兑换中大于0的记录 如果为1则查找
        parser.add_argument('delta_amount_flag', type=int, location='args')
        parsed_args = parser.parse_args()

        q = AssetsBalanceRecord.query
        q = q.filter_by(user_id=g.current_user.id)
        if parsed_args['assets_type']:
            q = q.filter(AssetsBalanceRecord.assets_type.op('&')(parsed_args['assets_type']))
        if parsed_args['record_type']:
            q = q.filter(AssetsBalanceRecord.record_type.op('&')(parsed_args['record_type']))
        if parsed_args['create_begin_timestamp'] is not None:
            create_begin_datetime = timestamp_to_datetime(parsed_args['create_begin_timestamp'])
            q = q.filter(AssetsBalanceRecord.created_at >= create_begin_datetime)
        if parsed_args['create_end_timestamp'] is not None:
            create_end_datetime = timestamp_to_datetime(parsed_args['create_end_timestamp'])
            q = q.filter(AssetsBalanceRecord.created_at < create_end_datetime)
        if parsed_args['delta_amount_flag'] is not None:
            if parsed_args['delta_amount_flag']:
                q = q.filter(AssetsBalanceRecord.delta_amount > 0)
        q = q.order_by(AssetsBalanceRecord.id.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)


@assets_api.add_resource('/exchange')
class MemberAssets2SelfApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_assets_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('amount', type=int, required=True, nullable=False, location='json')
        parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        if parsed_args['amount'] <= 0:
            abort(400, code=1003, message={'amount': 'amount <= 0'})

        if not g.current_user.security_password:
            abort(400, code=1012, message={'security_password': 'security password is empty'})
        if not g.current_user.verify_security_password(parsed_args['security_password']):
            abort(400, code=1002, message={'security_password': 'security password does not match'})

        option = Setting.get_json('general_option')
        exchange_amount_min = option['exchange_amount_min']
        exchange_amount_max = option['exchange_amount_max']

        if parsed_args['amount'] % exchange_amount_min > 0:
            abort(400, code=1001,
                  message={'amount': 'the amount must be a multiple of {}'.format(exchange_amount_min)})

        # 用于计算今天兑换的数量
        str_time = datetime.datetime.now().strftime('%Y-%m-%d')
        sum_amount = db.session.query(db.func.sum(AssetsBalanceRecord.delta_amount)).filter(
            db.func.date_format(AssetsBalanceRecord.created_at, '%Y-%m-%d') == str_time,
            AssetsBalanceRecord.user_id == g.current_user.id,
            AssetsBalanceRecord.record_type == g_assets_record_type.EXCHANGE,
            AssetsBalanceRecord.assets_type == g_assets_type.COMMUNITY).first()[0]
        sum_amount = sum_amount if sum_amount is not None else 0
        if sum_amount + parsed_args['amount'] > exchange_amount_max:
            abort(400, code=1006,
                  message={
                      'amount': 'already amount {} + current amount {} > {}'.format(sum_amount, parsed_args['amount'],
                                                                                    exchange_amount_max)})

        assets = Assets.get_assets(g.current_user.id)
        detail = {'message': '兑换'}

        if not assets.update_transaction_balance(-parsed_args['amount'], g_assets_record_type.EXCHANGE, detail):
            abort(400, code=1008, message={'balance': 'current balance < {}'.format(parsed_args['amount'])})

        assets.update_community_balance(parsed_args['amount'], g_assets_record_type.EXCHANGE, detail)

        db.session.commit()
        return assets


@assets_api.add_resource('/transaction')
class MemberAssetsTransactionApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_assets_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('mobile', type=str, required=True, nullable=False, location='json') # 收款人的用户手机号
        parser.add_argument('amount', type=int, required=True, nullable=False, location='json')
        parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        user = User.query.filter(User.mobile == parsed_args['mobile']).first()
        if user is None:
            abort(400, code=1001, message={'mobile': 'user does not exist'})

        if parsed_args['amount'] <= 0:
            abort(400, code=1003, message={'amount': 'amount <= 0'})

        if not g.current_user.security_password:
            abort(400, code=1012, message={'security_password': 'security password is empty'})
        if not g.current_user.verify_security_password(parsed_args['security_password']):
            abort(400, code=1002, message={'security_password': 'security password does not match'})

        if not g.current_user.is_community_node:
            abort(400, code=1001, message={'current_user': 'current user does not community node'})

        if user.is_community_node:
            abort(400, code=1001, message={'user': 'user does not normal node'})

        option = Setting.get_json('general_option')
        community_transaction_fee_rate = option['community_transaction_fee_rate']
        # exchange_amount_min = option['exchange_amount_min']
        # exchange_amount_max = option['exchange_amount_max']
        #
        # if parsed_args['amount'] < exchange_amount_min or parsed_args['amount'] > exchange_amount_max:
        #     abort(400, code=1006,
        #           message={'amount': 'amount < {} or amount > {}'.format(exchange_amount_min, exchange_amount_max)})

        fee = decimal.Decimal(parsed_args['amount']) * decimal.Decimal(community_transaction_fee_rate)
        amount = decimal.Decimal(parsed_args['amount']) + decimal.Decimal(fee)
        assets = Assets.get_assets(g.current_user.id)
        detail = {
            'message': '{}转给{}, 金额:{}, 手续费:{}'.format(
                g.current_user.mobile, user.mobile, parsed_args['amount'], fee)
        }

        if not assets.update_transaction_balance(-amount, g_assets_record_type.TRANSACTION, detail):
            abort(400, code=1008, message={'balance': 'current balance < {}'.format(amount)})

        assets = Assets.get_assets(user.id)
        assets.update_total_balance(parsed_args['amount'], g_assets_record_type.TRANSACTION, detail)

        db.session.commit()
        return assets
