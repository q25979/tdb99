# -*- coding: utf-8 -*-
import datetime
import uuid
from flask import Blueprint, g, request, url_for
from flask_restful import Api, abort, fields, marshal_with, Resource

from app.api import pagination_query, restful_api, CustomRequestParser, UrlNormalize, AddResource
from app.api.member import member_login_required
from app.model import db, Datetime2Timestamp, DecimalToString
from app.model.user import LoginInfo, User, g_user_state_type
from app.model.pin_code import CaptchaPinCode, SmsPinCode
from app.model.payment import Payment
from werkzeug.http import dump_cookie

user_bp = Blueprint('member_user_bp', __name__)
user_api = AddResource(Api(user_bp))


def member_user_mobile_exists(mobile):
    user = User.query.filter(User.mobile == mobile).first()
    return user


member_user_login_fields = {
    'id': fields.String,
    'uid': fields.String,
    'mobile': fields.String,
    'token': fields.String,
}


@user_api.add_resource('/mobile_register')
class MemberUserMobileRegisterApi(Resource):
    @marshal_with(member_user_login_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('country_code', type=str, default='86', location='json')
        parser.add_argument('mobile', type=str, required=True, nullable=False, location='json')
        parser.add_argument('password', type=str, required=True, nullable=False, location='json')
        parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('pin_code', type=str, required=True, nullable=False, location='json')
        parser.add_argument('source', type=str, default='', location='json')
        parser.add_argument('sponsor_uid', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('uuid', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('captcha_pin_code', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        # CaptchaPinCode.flask_check(parsed_args['uuid'], parsed_args['captcha_pin_code'])

        sponsor = User.query.filter(User.uid == parsed_args['sponsor_uid']).first()

        if not sponsor:
            abort(400, code=1001, message={'sponsor': 'sponsor does not exist'})

        # 测试环境，不验证手机验证码
        # product_name = str(current_app.config['PRODUCT_NAME'])

        # country_code = parsed_args['country_code']
        # if parsed_args['country_code']:
        #     if "+" in parsed_args['country_code']:
        #         country_code = parsed_args['country_code'][1:]

        if member_user_mobile_exists(parsed_args['mobile']):
            abort(400, code=1011, message={'mobile': 'mobile already exists'})

        # SmsPinCode.flask_check(parsed_args['mobile'], parsed_args['pin_code'])

        user = User(id=str(uuid.uuid4()),
                    # country_code=country_code,
                    mobile=parsed_args['mobile'],
                    source=parsed_args['source'],
                    sponsor_id=sponsor.id)

        # user.set_uid() # 项目要求完善资料后生成
        user.set_password(parsed_args['password'])
        user.set_security_password(parsed_args['security_password'])
        user.generate_auth_token()
        db.session.add(user)
        db.session.flush()
        user.activate()
        db.session.commit()

        cookie = dump_cookie(key='token', value=user.token, max_age=datetime.timedelta(days=365))
        return user, {'Set-Cookie': cookie}


@user_api.add_resource('/password_login')
class MemberUserPasswordLoginApi(Resource):
    @marshal_with(member_user_login_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('mobile', type=str, required=True, nullable=False, location='json')
        parser.add_argument('uuid', type=str, required=True, nullable=False, location='json')
        parser.add_argument('password', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('captcha_pin_code', type=str, required=True, nullable=False, location='json')
        parser.add_argument('client_ip', type=str, default=request.access_route[0], location='json')
        parser.add_argument('platform', type=str, nullable=False, default='android', location='json')
        parsed_args = parser.parse_args()

        user = User.query.filter(User.mobile == parsed_args['mobile']).first()
        if user is None:
            abort(400, code=1001, message={'unique_id': 'user does not exist'})

        # CaptchaPinCode.flask_check(parsed_args['uuid'], parsed_args['captcha_pin_code'])

        if user.verify_password(parsed_args['password']):
            user.generate_auth_token()
            cookie = dump_cookie(key='token', value=user.token, max_age=datetime.timedelta(days=365))
            login_info = LoginInfo(user_id=user.id,
                                   client_ip=parsed_args['client_ip'])
            # 设置登录平台 ，android or ios
            user.platform = parsed_args['platform']
            db.session.add(login_info)
            db.session.commit()
            return user, {'Set-Cookie': cookie}
        else:
            abort(400, code=1002, message={'password': 'password does not match'})


@user_api.add_resource('/logout')
class MemberUserLogoutApi(Resource):
    decorators = [member_login_required]

    def post(self):
        g.current_user.generate_auth_token()
        db.session.commit()
        return {}, {'Set-Cookie': dump_cookie('token', max_age=0)}


member_current_user_fields = {
    'id': fields.String,
    'uid': fields.String,
    'country_code': fields.String,
    'mobile': fields.String,
    'token': fields.String,
    'avatar': fields.String,
    'name': fields.String,
    'order_mobile': fields.String,
    'nickname': fields.String,
    'gender': fields.Integer,
    'wechat': fields.String,
    'has_security_password': fields.Integer,
    'state': fields.Raw(attribute=lambda x: x.state if x.transaction_level == 0 else 2),
    'allow_transaction': fields.Integer,
    'transaction_level': fields.Integer,
    'cal_team_count': fields.Integer,
    'buy_order_cnt': fields.Integer,
    'continuous_buy_cnt': fields.Integer,
    'today_have_transaction': fields.Integer,
    'team_qualified_cnt': fields.Integer,
    'is_community_node': fields.Integer,
    'node_profit': fields.String
}


def member_user_qr_code(user):
    return url_for('address_qr_code', qr_id=user.id, _external=True)


@user_api.add_resource('/current_user')
class MemberUserCurrentUserApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_current_user_fields)
    def get(self):
        return g.current_user

    @marshal_with(member_current_user_fields)
    def put(self):
        parser = CustomRequestParser()
        parser.add_argument('old_password', type=str, location='json')
        parser.add_argument('new_password', type=str, nullable=False, location='json')
        parser.add_argument('old_security_password', type=str, location='json')
        parser.add_argument('new_security_password', type=str, nullable=False, location='json')
        parser.add_argument('avatar', type=str, location='json')
        parser.add_argument('order_mobile', type=str, location='json')
        parser.add_argument('name', type=str, nullable=False, location='json')  # 姓名
        parser.add_argument('nickname', type=str, nullable=False, location='json')  # 姓名
        parser.add_argument('gender', type=int, default=0, choices=(0, 1, 2), location='json')  # 性别
        parser.add_argument('wechat', type=str, nullable=False, location='json')  # 微信
        parsed_args = parser.parse_args()

        if parsed_args['old_password'] and parsed_args['new_password']:
            if not g.current_user.verify_password(parsed_args['old_password']):
                abort(400, code=1002, message={'old_password': 'old_password does not match'})
            g.current_user.set_password(parsed_args['new_password'])
        if parsed_args['new_security_password']:
            if g.current_user.has_security_password:
                if not g.current_user.verify_security_password(parsed_args['old_security_password']):
                    abort(400, code=1002, message={'old_security_password': 'old_security_password does not match'})
            g.current_user.set_security_password(parsed_args['new_security_password'])
        if parsed_args['avatar']:
            g.current_user.avatar = parsed_args['avatar']
        if parsed_args['name']:
            g.current_user.name = parsed_args['name']
        if parsed_args['nickname']:
            g.current_user.nickname = parsed_args['nickname']
        if parsed_args['gender'] is not None:
            g.current_user.gender = parsed_args['gender']
        if parsed_args['wechat']:
            g.current_user.wechat = parsed_args['wechat']
        if parsed_args['order_mobile']:
            g.current_user.order_mobile = parsed_args['order_mobile']

        if g.current_user.name is not None and g.current_user.gender != 0 and g.current_user.wechat is not None and \
                g.current_user.state == g_user_state_type.UNCOMPLETED_DATA:
            g.current_user.set_uid()
            g.current_user.update_state(g_user_state_type.COMPLETED_DATA)

        db.session.commit()
        return g.current_user


# 通过测试
@user_api.add_resource('/evaluation')
class MemberUserEvaluationFinishApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_current_user_fields)
    def post(self):
        if g.current_user.uid is None:
            abort(400, code=1002, message={'uid': 'incomplete information'})

        g.current_user.update_state(g_user_state_type.EVALUATION)
        db.session.commit()
        return g.current_user


@user_api.add_resource('/reset_password')
class MemberUserResetPasswordApi(Resource):
    @marshal_with(member_user_login_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('mobile', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('pin_code', type=str, required=True, nullable=False, location='json')
        parser.add_argument('password', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('uuid', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('captcha_pin_code', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        # CaptchaPinCode.flask_check(parsed_args['uuid'], parsed_args['captcha_pin_code'])

        # user = User.reset_password(parsed_args['mobile'], parsed_args['pin_code'], parsed_args['password'])
        user = User.reset_password(parsed_args['mobile'], parsed_args['password'])
        if not user:
            abort(400, code=1001, message={'mobile': 'user does not exist'})
        db.session.commit()
        cookie = dump_cookie(key='token', value=user.token, max_age=datetime.timedelta(days=365))
        return user, {'Set-Cookie': cookie}


@user_api.add_resource('/reset_security_password')
class MemberUserResetSecurityPasswordApi(Resource):
    @marshal_with(member_user_login_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('mobile', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('pin_code', type=str, required=True, nullable=False, location='json')
        parser.add_argument('password', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('uuid', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('captcha_pin_code', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        # CaptchaPinCode.flask_check(parsed_args['uuid'], parsed_args['captcha_pin_code'])

        # user = User.reset_security_password(parsed_args['mobile'], parsed_args['pin_code'], parsed_args['password'])
        user = User.reset_security_password(parsed_args['mobile'], parsed_args['password'])
        if not user:
            abort(400, code=1001, message={'mobile': 'user does not exist'})
        db.session.commit()
        return user


@user_api.add_resource('/rebind_id')
class MemberUserRebindIdApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_user_login_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('mobile', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('pin_code', type=str, required=True, nullable=False, location='json')
        parser.add_argument('new_mobile', type=str, required=True, nullable=False, location='json')
        parser.add_argument('new_pin_code', type=str, required=True, nullable=False, location='json')
        parser.add_argument('country_code', type=str, location='json')
        parsed_args = parser.parse_args()

        g.current_user.rebind_id(parsed_args['mobile'],
                                 # parsed_args['pin_code'],
                                 parsed_args['new_mobile'],
                                 # parsed_args['new_pin_code'],
                                 parsed_args['country_code'])
        db.session.commit()
        return {}


member_user_login_info_fields = {
    'id': fields.String,
    'client_ip': fields.String,
    'created_at': Datetime2Timestamp
}

member_user_login_info_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(member_user_login_info_fields))
}


@user_api.add_resource('/login_info')
class MemberUserLoginInfoListApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_user_login_info_list_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parsed_args = parser.parse_args()

        q = LoginInfo.query.filter_by(user_id=g.current_user.id)
        q = q.order_by(LoginInfo.created_at.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)


@user_api.add_resource('/login_info/<string:info_id>')
class MemberUserLoginInfoApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_user_login_info_fields)
    def get(self, info_id):
        login_info = LoginInfo.query.filter_by(id=info_id,
                                               user_id=g.current_user.id).first()
        if login_info is None:
            abort(400, code=1001, message={'info_id': 'login info does not exist'})
        return login_info
