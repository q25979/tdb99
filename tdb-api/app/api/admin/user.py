# -*- coding: utf-8 -*-
import json

from flask import Blueprint, g
from flask_restful import Api, Resource, marshal_with, fields, reqparse, abort

from app.api import AddResource, pagination_query
from app.api.admin import admin_login_required
from app.model.admin_user import AdminUser
from app.model.pin_code import CaptchaPinCode

user_bp = Blueprint('admin_user', __name__)
restful_api = Api(user_bp)
user = AddResource(restful_api)


class AccessFunction(fields.Raw):
    def format(self, value):
        return value


admin_login_fields = {
    'id': fields.String,
    'uid': fields.String,
    'role': fields.Integer,
    'token': fields.String,
    'permission': fields.Raw(attribute=lambda x: json.loads(x.permission if x.permission else '{}'))
}


@user.add_resource('/login')
class LoginApi(Resource):
    @marshal_with(admin_login_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        parser.add_argument('uuid', type=str, required=True, location='json')
        parser.add_argument('pin_code', type=str, required=True, location='json')
        parsed_args = parser.parse_args()

        admin_user = AdminUser.query.filter_by(uid=parsed_args['uid']).first()
        if admin_user is None:
            abort(400, code=1001, message={'uid': 'uid does not exist'})
        else:
            CaptchaPinCode.flask_check(parsed_args['uuid'], parsed_args['pin_code'])
            if admin_user.verify_password(parsed_args['password']):
                admin_user.generate_auth_token()
                if admin_user.locked:
                    abort(400, code=1003, message={'locked': 'The user is locked'})
                return admin_user.save()
            else:
                abort(400, code=1002, message={'password': 'password does not match'})


@user.add_resource('/reset_password')
class AdminResetPasswordApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_login_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=True, location='json')
        parser.add_argument('new_password', type=str, required=True, location='json')
        parsed_args = parser.parse_args()

        if not g.current_user.verify_password(parsed_args['password']):
            abort(400, code=1002, message={'password': 'password does not match'})

        g.current_user.set_password(parsed_args['new_password'])
        g.current_user.generate_auth_token()
        return g.current_user.save()


admin_user_fields = {
    'id': fields.String,
    'created_timestamp': fields.Integer,  # 主要 model 的继承里面有，时间对外都用时间戳
    # 'updated_at': fields.DateTime,  # 一般不带的
    'uid': fields.String,
    'permission': fields.Raw(attribute=lambda x: json.loads(x.permission if x.permission else '{}')),
    'role': fields.Integer,
    'locked': fields.Integer,
}

admin_user_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(admin_user_fields))

}


@user.add_resource()
class AdminUserListApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_user_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('role', type=int, choices=(1, 2), default=2, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parsed_args = parser.parse_args()

        q = AdminUser.query
        q = q.filter(AdminUser.id != g.current_user.id)

        if parsed_args['role']:
            q = q.filter(AdminUser.role == parsed_args['role'])

        q = q.order_by(AdminUser.created_at.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)

    @marshal_with(admin_user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        parser.add_argument('role', type=int, choices=(1, 2), default=2, location='json')
        parser.add_argument('permission', type=json.dumps, required=True, location='json')

        parsed_args = parser.parse_args()
        admin_user = AdminUser.query.filter(AdminUser.uid == parsed_args['uid']).first()
        if admin_user:
            abort(400, code=1006, message={'uid': 'admin uid does exist'})

        admin_user = AdminUser(uid=parsed_args['uid'],
                               permission=parsed_args['permission'],
                               role=parsed_args['role'])
        admin_user.set_password(parsed_args['password'])
        return admin_user.save()


@user.add_resource('/<string:admin_user_id>')
class AdminUserApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_user_fields)
    def get(self, admin_user_id):
        admin_user = AdminUser.query.get(admin_user_id)
        if admin_user is None:
            abort(400, code=1001, message={'admin_user_id': 'admin user does not exist'})
        return admin_user

    @marshal_with(admin_user_fields)
    def put(self, admin_user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, location='json')
        parser.add_argument('locked', type=int, choices=(0, 1), location='json')
        parser.add_argument('role', type=str, location='json')
        parser.add_argument('permission', type=json.dumps, location='json')
        parsed_args = parser.parse_args()

        admin_user = AdminUser.query.get(admin_user_id)
        if admin_user_id == g.current_user.id:
            abort(404)
        if admin_user is None:
            abort(400, code=1001, message={'admin_user_id': 'admin user does not exist'})

        if parsed_args['password']:
            admin_user.set_password(parsed_args['password'])
            admin_user.generate_auth_token()
        if parsed_args['locked'] is not None:
            admin_user.locked = parsed_args['locked']
        if parsed_args['role']:
            admin_user.role = parsed_args['role']
        if parsed_args['permission'] != admin_user.permission:
            admin_user.permission = parsed_args['permission']
            admin_user.generate_auth_token()

        return admin_user.save()
