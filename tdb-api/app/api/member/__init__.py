# -*- coding: utf-8 -*-
from functools import wraps

from flask import g, request
from flask_restful import abort


def member_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        from app.model.user import User
        token = request.args.get('token')
        if not token:
            token = request.cookies.get('token')
        g.current_user = User.verify_auth_token(token)
        if g.current_user is None:
            abort(401)
        return func(*args, **kwargs)

    return decorated_view
