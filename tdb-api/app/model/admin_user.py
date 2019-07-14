# -*- coding: utf-8 -*-
import decimal
import hashlib
import random
from flask import current_app, g, request
from flask_restful import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash
from app.model import db, UuidBase


class AdminUserBase(UuidBase):
    __abstract__ = True

    ROOT_ID = '00000000-0000-0000-0000-000000000000'

    uid = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)  # 1 超级管理员  2 系统管理员  4 代理
    locked = db.Column(db.SmallInteger, default=0, nullable=False)  # 0 未锁定  1 锁定
    token = db.Column(db.String(256))
    permission = db.Column(db.Text)  # 权限

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=365 * 24 * 60 * 60):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        self.token = s.dumps({'id': self.id})

    @classmethod
    def verify_auth_token(cls, token):
        if not token:
            return None
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = cls.query.get(data['id'])
        if user and not user.locked and user.token == token:
            return user
        return None


class AdminUser(AdminUserBase):
    parent_id = db.Column(db.String(36), db.ForeignKey('admin_user.id'))

    # relationship
    parent = db.relationship('AdminUser', foreign_keys=[parent_id], remote_side="AdminUser.id")

    @staticmethod
    def initialize():
        root_admin = AdminUser.query.get(AdminUserBase.ROOT_ID)
        if root_admin is None:
            root_admin = AdminUser(id=AdminUserBase.ROOT_ID,
                                   uid='admin',
                                   role=1)
            root_admin.set_password('888888')
            root_admin.generate_auth_token()
            db.session.add(root_admin)
            db.session.commit()
