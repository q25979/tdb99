# -*- coding: utf-8 -*-
import datetime
import time
import uuid
import decimal

from flask import Blueprint
from flask_restful import Api, Resource, marshal_with, abort
from flask_restful import fields
from flask_restful import reqparse
from werkzeug.http import dump_cookie

from app import db
from app.api import AddResource, pagination_query
from app.api.admin import admin_sys_login_required, member_user_fields
from app.model import timestamp_to_datetime, DecimalToString
from app.model.assets import AssetsBalanceRecord
from app.model.order import Order
from app.model.user import User, g_user_state_type, g_user_transaction_level

member_bp = Blueprint('admin_member_bp', __name__)
member_api = AddResource(Api(member_bp))


def cal_community_balance(x):
    balance = x.community_balance + x.community_today_balance
    return '{0:.8f}'.format(decimal.Decimal(balance))


admin_member_fields = {
    'id': fields.String,
    'uid': fields.String,
    'created_timestamp': fields.Integer,
    'mobile': fields.String,
    'locked': fields.Integer,
    'avatar': fields.String,
    'sponsor': fields.Nested(member_user_fields),
    'gender': fields.Integer,
    'name': fields.String,
    'nickname': fields.String,
    'wechat': fields.String,
    'state': fields.Integer,
    'allow_transaction': fields.Integer,
    'transaction_level': fields.Integer,
    'buy_order_cnt': fields.Integer,
    'continuous_buy_cnt': fields.Integer,
    'today_have_transaction': fields.Integer,
    'team_qualified_cnt': fields.Integer,
    'is_community_node': fields.Integer,
    'node_profit': fields.String,
    'assets': fields.Nested({
        'id': fields.String,
        'total_balance': DecimalToString,
        'community_balance': fields.Raw(attribute=lambda x: cal_community_balance(x)),
        'transaction_balance': DecimalToString,
    })
}

admin_member_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(admin_member_fields))
}


@member_api.add_resource()
class AdminMember(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('locked', type=int, choices=(0, 1, 2), location='args')
        parser.add_argument('name', type=str, location='args')
        parser.add_argument('nickname', type=str, location='args')
        parser.add_argument('uid', type=str, location='args')
        parser.add_argument('sponsor', type=str, location='args')
        parser.add_argument('mobile', type=str, location='args')
        parser.add_argument('wechat', type=str, location='args')
        parser.add_argument('state', type=str, location='args')
        parser.add_argument('allow_transaction', type=int, choices=(0, 1), location='args')
        parser.add_argument('is_community_node', type=int, choices=(0, 1), location='args')
        parser.add_argument('transaction_level', type=int, choices=(
            g_user_transaction_level.NORMAL, g_user_transaction_level.PRIORITY, g_user_transaction_level.ULTIMATE),
                            location='args')
        parser.add_argument('created_begin_timestamp', type=int, location='args')
        parser.add_argument('created_end_timestamp', type=int, location='args')
        parsed_args = parser.parse_args()

        q = User.query.filter(User.locked != 2)
        if parsed_args['name']:
            q = q.filter(User.name.contains(parsed_args['name']))
        if parsed_args['nickname']:
            q = q.filter(User.nickname.contains(parsed_args['nickname']))
        if parsed_args['uid']:
            q = q.filter(User.uid.contains(parsed_args['uid']))
        if parsed_args['mobile']:
            q = q.filter(User.mobile.contains(parsed_args['mobile']))
        if parsed_args['wechat']:
            q = q.filter(User.wechat.contains(parsed_args['wechat']))
        if parsed_args['sponsor']:
            q = q.filter(User.sponsor.has(User.mobile.contains(parsed_args['sponsor'])))
        if parsed_args['locked'] is not None:
            q = q.filter(User.locked == parsed_args['locked'])
        if parsed_args['state']:
            q = q.filter(User.state == parsed_args['state'])
        if parsed_args['is_community_node'] is not None:
            q = q.filter(User.is_community_node == parsed_args['is_community_node'])

        if parsed_args['allow_transaction'] is not None:
            q = q.filter(User.allow_transaction == parsed_args['allow_transaction'])
        if parsed_args['transaction_level'] is not None:
            q = q.filter(User.transaction_level == parsed_args['transaction_level'])
        if parsed_args['is_community_node'] is not None:
            q = q.filter(User.is_community_node == parsed_args['is_community_node'])

        if parsed_args['created_begin_timestamp']:
            if not parsed_args['created_end_timestamp']:
                parsed_args['created_end_timestamp'] = int(time.time())
            begin_timestamp = min(parsed_args['created_begin_timestamp'], parsed_args['created_end_timestamp'])
            end_timestamp = max(parsed_args['created_begin_timestamp'], parsed_args['created_end_timestamp'])
            q = q.filter(db.and_(User.created_at >= timestamp_to_datetime(begin_timestamp),
                                 User.created_at < timestamp_to_datetime(end_timestamp)))

        q = q.order_by(User.created_at.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)

    @marshal_with(admin_member_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('country_code', type=str, default='', location='json')
        parser.add_argument('mobile', type=str, required=True, nullable=False, location='json')
        parser.add_argument('password', type=str, required=True, nullable=False, location='json')
        parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        parser.add_argument('source', type=str, default='', location='json')
        parser.add_argument('sponsor', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        sponsor = User.query.filter(User.mobile == parsed_args['sponsor']).first()

        if sponsor is None:
            abort(400, code=1001, message={'sponsor': 'sponsor does not exist'})

        if User.query.filter(User.mobile == parsed_args['mobile']).first():
            abort(400, code=1011, message={'uid': 'uid already exists'})

        user = User(id=str(uuid.uuid4()),
                    country_code=parsed_args['country_code'],
                    mobile=parsed_args['mobile'],
                    source=parsed_args['source'],
                    sponsor_id=sponsor.id)
        user.set_password(parsed_args['password'])
        user.set_security_password(parsed_args['security_password'])

        user.generate_auth_token()

        db.session.add(user)
        db.session.flush()
        user.set_uid()
        user.update_state(g_user_state_type.EVALUATION)

        user.activate()

        db.session.commit()
        return user


@member_api.add_resource('/detail/<string:member_id>')
class AdminMemberDetail(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_fields)
    def get(self, member_id):
        member = User.query.get(member_id)
        if not member:
            abort(400, code=1001, message={'member_id': 'member does not exist'})
        return member

    @marshal_with(admin_member_fields)
    def put(self, member_id):
        parser = reqparse.RequestParser()
        parser.add_argument('mobile', type=str, location='json')
        parser.add_argument('locked', type=int, choices=(0, 1, 2), location='json')
        parser.add_argument('password', type=str, nullable=False, location='json')
        parser.add_argument('security_password', type=str, location='json')
        parser.add_argument('avatar', type=str, location='json')
        parser.add_argument('wechat', type=str, location='json')
        parser.add_argument('name', type=str, nullable=False, location='json')
        parser.add_argument('nickname', type=str, nullable=False, location='json')
        parser.add_argument('wechat', type=str, nullable=False, location='json')
        parser.add_argument('gender', type=int, choices=(0, 1, 2), location='json')
        parser.add_argument('state', type=int, choices=(
            g_user_state_type.UNCOMPLETED_DATA, g_user_state_type.COMPLETED_DATA, g_user_state_type.EVALUATION),
                            location='json')
        parser.add_argument('allow_transaction', type=int, choices=(0, 1), location='json')
        parser.add_argument('transaction_level', type=int, choices=(
            g_user_transaction_level.NORMAL, g_user_transaction_level.PRIORITY, g_user_transaction_level.ULTIMATE),
                            location='json')
        parsed_args = parser.parse_args()

        member = User.query.get(member_id)
        if not member:
            abort(400, code=1001, message={'member_id': 'member does not exist'})

        if parsed_args['password']:
            member.set_password(parsed_args['password'])
            member.generate_auth_token()
        if parsed_args['security_password']:
            member.set_security_password(parsed_args['security_password'])
        if parsed_args['locked'] is not None:
            member.locked = parsed_args['locked']
            if parsed_args['locked'] == 2:
                if User.query.filter(User.sponsor_id == member.id,
                                     User.locked != 2).first():
                    abort(400, code=1011, message={'sponsor_id': 'sponsor does  exist'})
                if Order.query.filter(Order.user_id == member.id).first():
                    abort(400, code=1011, message={'order': 'order does exist'})

                member.mobile = None
                member.uid = None

        if parsed_args['mobile']:
            member.mobile = parsed_args['mobile']
        if parsed_args['avatar']:
            member.avatar = parsed_args['avatar']
        if parsed_args['name']:
            member.name = parsed_args['name']
        if parsed_args['nickname']:
            member.name = parsed_args['nickname']
        if parsed_args['gender'] is not None:
            member.gender = parsed_args['gender']
        if parsed_args['wechat']:
            member.wechat = parsed_args['wechat']
        if parsed_args['state']:
            member.update_state(parsed_args['state'])
        if parsed_args['allow_transaction'] is not None:
            member.allow_transaction = parsed_args['allow_transaction']
        if parsed_args['transaction_level'] is not None:
            member.transaction_level = parsed_args['transaction_level']
            member.set_uid()

        db.session.commit()
        return member


@member_api.add_resource('/login')
class AdminMemberLogin(Resource):
    decorators = [admin_sys_login_required]

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, location='args')
        parser.add_argument('redirect', type=str, required=True, location='args')
        parsed_args = parser.parse_args()

        member = User.query.get(parsed_args['id'])
        cookie = dump_cookie(key='token', value=member.token, max_age=datetime.timedelta(days=365))
        return {}, 301, {'Set-Cookie': cookie,
                         'Location': parsed_args['redirect']}


admin_member_cnt_fields = {
    'register_cnt': fields.Raw(attribute=lambda x: x)
}


@member_api.add_resource('/register_cnt')
class AdminMemberRegisterCnt(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_member_cnt_fields)
    def get(self):

        str_time = datetime.datetime.now().strftime('%Y-%m-%d')

        user_cnt = db.session.query(User.id).filter(
            User.created_at >= str_time, User.state == g_user_state_type.EVALUATION).count()
        user_cnt = user_cnt if user_cnt is not None else 0

        return user_cnt
