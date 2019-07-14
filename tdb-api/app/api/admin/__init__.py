# -*- coding: utf-8 -*-
from functools import wraps
from flask import g, request
from flask_restful import abort, fields


# 管理员授权
def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        from app.model.admin_user import AdminUser
        token = request.args.get('token')
        if not token:
            token = request.cookies.get('token')
        g.current_user = AdminUser.verify_auth_token(token)
        if g.current_user is None:
            abort(401)
        return func(*args, **kwargs)

    return decorated_view


# 系统管理员授权
def admin_sys_login_required(func):
    @admin_login_required
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if g.current_user.role > 2:
            abort(403)
        return func(*args, **kwargs)

    return decorated_view


# 超级管理员授权
def admin_root_login_required(func):
    @admin_login_required
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if g.current_user.role > 1:
            abort(403)
        return func(*args, **kwargs)

    return decorated_view


member_user_fields = {
    'id': fields.String,
    'uid': fields.String,
    'created_timestamp': fields.Integer,
    'mobile': fields.String,
    'name': fields.String,
    'locked': fields.Integer,
    #     'rate_level': fields.Integer,
    'avatar': fields.String,
}
