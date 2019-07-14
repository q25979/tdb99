import json
import time
import decimal

from flask import Blueprint, g
from flask_restful import Api, fields, Resource, marshal_with, abort, reqparse

from app import db
from app.api import AddResource, CustomRequestParser, pagination_query
from app.api.admin import admin_login_required
from app.model import timestamp_to_datetime, DecimalToString, Datetime2Timestamp
from app.model.assets import Assets, AssetsBalanceRecord, g_assets_type, g_assets_record_type
from app.model.user import User

assets_bp = Blueprint('admin_assets_bp', __name__)
assets_api = AddResource(Api(assets_bp))

admin_assets_user_fields = {
    'id': fields.String,
    'uid': fields.String,
    'name': fields.String,
    'email': fields.String,
    'mobile': fields.String
}


def cal_community_balance(x):
    balance = x.community_balance + x.community_today_balance
    return '{0:.8f}'.format(decimal.Decimal(balance))


admin_assets_fields = {
    'id': fields.Integer,
    'user': fields.Nested(admin_assets_user_fields),
    'total_balance': DecimalToString,
    'community_balance': fields.Raw(attribute=lambda x: cal_community_balance(x)),
    'transaction_balance': DecimalToString,
    'grand_total_balance': DecimalToString,
    'community_frozen_balance': DecimalToString
}

admin_assets_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(admin_assets_fields))
}


@assets_api.add_resource()
class AdminAssetsListApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_assets_list_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('mobile', type=str, location='args')
        parsed_args = parser.parse_args()

        q = Assets.query
        if parsed_args['uid']:
            q = q.filter(Assets.user.has(User.uid.contains(parsed_args['uid'])))
        if parsed_args['mobile']:
            q = q.filter(Assets.user.has(User.mobile.contains(parsed_args['mobile'])))
        q = q.order_by(Assets.id.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)


@assets_api.add_resource('/<int:assets_id>')
class AdminAssetsApi(Resource):
    @admin_login_required
    @marshal_with(admin_assets_fields)
    def get(self, assets_id):
        assets = Assets.query.get(assets_id)
        if assets is None:
            abort(400, code=1001, message={'assets_id': 'assets does not exist'})
        return assets


admin_assets_balance_record_income_fields = {
    'income': fields.String(default='0')
}


@assets_api.add_resource('/balance_record_income')
class AdminAssetsBalanceRecordIncomeApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_assets_balance_record_income_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('create_begin_timestamp', type=int, location='args')
        parser.add_argument('create_end_timestamp', type=int, location='args')
        parsed_args = parser.parse_args()

        q = AssetsBalanceRecord.query.filter(AssetsBalanceRecord.delta_amount > 0)
        q = q.filter(AssetsBalanceRecord.user_id != User.VIRTUAL_ID)
        if parsed_args['uid']:
            user = User.get_user(uid=parsed_args['uid'])
            if user is None:
                abort(400, code=1001, message={'user': 'user does not exist'})
            q = q.filter_by(user_id=user.id)
        if parsed_args['create_begin_timestamp'] is not None:
            create_begin_datetime = timestamp_to_datetime(parsed_args['create_begin_timestamp'])
            q = q.filter(AssetsBalanceRecord.created_at >= create_begin_datetime)
        if parsed_args['create_end_timestamp'] is not None:
            create_end_datetime = timestamp_to_datetime(parsed_args['create_end_timestamp'])
            q = q.filter(AssetsBalanceRecord.created_at < create_end_datetime)
        income = q.with_entities(db.func.sum(AssetsBalanceRecord.delta_amount))
        return {
            'income': income.scalar()
        }


admin_assets_balance_record_expense_fields = {
    'expense': fields.String(default='0')
}


@assets_api.add_resource('/balance_record_expense')
class AdminAssetsBalanceRecordExpenseApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_assets_balance_record_expense_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('create_begin_timestamp', type=int, location='args')
        parser.add_argument('create_end_timestamp', type=int, location='args')
        parsed_args = parser.parse_args()

        q = AssetsBalanceRecord.query.filter(AssetsBalanceRecord.delta_amount < 0)
        if parsed_args['uid']:
            user = User.get_user(uid=parsed_args['uid'])
            q = q.filter_by(user_id=user.id)
        if parsed_args['create_begin_timestamp'] is not None:
            create_begin_datetime = timestamp_to_datetime(parsed_args['create_begin_timestamp'])
            q = q.filter(AssetsBalanceRecord.created_at >= create_begin_datetime)
        if parsed_args['create_end_timestamp'] is not None:
            create_end_datetime = timestamp_to_datetime(parsed_args['create_end_timestamp'])
            q = q.filter(AssetsBalanceRecord.created_at < create_end_datetime)
        expense = q.with_entities(db.func.sum(db.func.abs(AssetsBalanceRecord.delta_amount)))
        return {
            'expense': expense.scalar()
        }


admin_assets_balance_record_fields = {
    'id': fields.Integer,
    'user': fields.Nested(admin_assets_user_fields),
    'current_amount': DecimalToString,
    'delta_amount': DecimalToString,
    'assets_type': fields.Integer,
    'record_type': fields.Integer,
    'details': fields.Raw(attribute=lambda x: json.loads(x.details)),
    'created_at': Datetime2Timestamp
}

admin_assets_balance_record_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(admin_assets_balance_record_fields))
}


@assets_api.add_resource('/record')
class MemberBalanceRecordListApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_assets_balance_record_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('assets_type', type=int, location='args')
        parser.add_argument('mobile', type=str, location='args')
        parser.add_argument('record_type', type=int, location='args')
        parser.add_argument('amount_type', type=int, choices=(0, 1, 2), location='args')
        parser.add_argument('created_begin_timestamp', type=int, location='args')
        parser.add_argument('created_end_timestamp', type=int, location='args')
        parsed_args = parser.parse_args()

        q = AssetsBalanceRecord.query
        if parsed_args['mobile']:
            q = q.filter(AssetsBalanceRecord.user.has(User.mobile == parsed_args['mobile']))
        if parsed_args['amount_type']:
            if parsed_args['amount_type'] == 1:
                q = q.filter(AssetsBalanceRecord.delta_amount >= 0)
            if parsed_args['amount_type'] == 2:
                q = q.filter(AssetsBalanceRecord.delta_amount < 0)

        if parsed_args['assets_type']:
            q = q.filter(AssetsBalanceRecord.assets_type.op('&')(parsed_args['assets_type']))
        if parsed_args['record_type']:
            q = q.filter(AssetsBalanceRecord.record_type.op('&')(parsed_args['record_type']))
        if parsed_args['created_begin_timestamp'] is not None:
            create_begin_datetime = timestamp_to_datetime(parsed_args['created_begin_timestamp'])
            q = q.filter(AssetsBalanceRecord.created_at >= create_begin_datetime)
        if parsed_args['created_end_timestamp'] is not None:
            create_end_datetime = timestamp_to_datetime(parsed_args['created_end_timestamp'])
            q = q.filter(AssetsBalanceRecord.created_at < create_end_datetime)
        q = q.order_by(AssetsBalanceRecord.id.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)


@assets_api.add_resource('/record/<string:record_id>')
class MemberBalanceRecordApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_assets_balance_record_fields)
    def get(self, record_id):
        record = AssetsBalanceRecord.query.filter_by(id=record_id).first()
        if record is None:
            abort(400, code=1001, message={'record_id': 'record does not exist'})
        return record


@assets_api.add_resource('/recharge')
class AdminAssetsRechargeApi(Resource):
    decorators = [admin_login_required]

    def post(self):
        parser = CustomRequestParser()

        parser.add_argument('id', type=str, required=True, location='json')
        parser.add_argument('assets_type', type=int, required=True,
                            choices=(g_assets_type.TOTAL, g_assets_type.COMMUNITY, g_assets_type.TRANSACTION),
                            location='json')
        parser.add_argument('amount', type=decimal.Decimal, required=True, location='json')
        parsed_args = parser.parse_args()

        assets = Assets.query.get(parsed_args['id'])
        if assets is None:
            abort(400, code=1001, message={'assets': 'assets does not exist'})

        details = {'message': '管理员：{}'.format(g.current_user.uid)}
        if parsed_args['assets_type'] == g_assets_type.TOTAL:
            if not assets.update_total_balance(parsed_args['amount'], g_assets_record_type.RECHARGE, details):
                abort(400, code=1008, message={'balance': 'current balance < {}'.format(parsed_args['amount'])})
        elif parsed_args['assets_type'] == g_assets_type.COMMUNITY:
            if not assets.update_community_balance(parsed_args['amount'], g_assets_record_type.RECHARGE, details):
                abort(400, code=1008, message={'balance': 'current balance < {}'.format(parsed_args['amount'])})
        else:
            if not assets.update_transaction_balance(parsed_args['amount'], g_assets_record_type.RECHARGE, details):
                abort(400, code=1008, message={'balance': 'current balance < {}'.format(parsed_args['amount'])})

        db.session.commit()
        return {}
