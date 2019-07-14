# -*- coding: utf-8 -*-
import datetime
from flask import current_app
from flask_restful import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from app.model import db


class PinCodeBase(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow,
                           nullable=False)
    pin_code_signature = db.Column(db.String(256), nullable=False)
    try_times = db.Column(db.SmallInteger, default=0)

    def generate_signature(self, pin_code, expiration=30 * 60):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        self.pin_code_signature = s.dumps({'id': pin_code})
        self.try_times = 0
        db.session.add(self)
        db.session.commit()

    # 返回值
    #   0 成功
    #   1 尝试次数太多
    #   2 PIN码错误
    #   3 PIN码过期
    @classmethod
    def verify(cls, unique_id, pin_code):
        result = cls.query.get(unique_id)
        if result is None:
            return 2
        result.try_times = cls.try_times + 1
        db.session.commit()
        if result.try_times > 5:
            return 1
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(result.pin_code_signature)
        except SignatureExpired:
            return 3  # valid signature, but expired
        except BadSignature:
            return 2  # invalid signature
        if data['id'] == pin_code.lower():
            db.session.delete(result)
            db.session.commit()
            return 0
        return 2

    @classmethod
    def flask_check(cls, unique_id, pin_code):
        result = cls.verify(unique_id, pin_code)
        if result == 1:
            abort(400, code=1005, message={'pin_code': 'try too many times'})
        elif result == 2:
            abort(400, code=1002, message={'pin_code': 'pin code does not match'})
        elif result == 3:
            abort(400, code=1006, message={'pin_code': 'pin code is expired'})


class SmsPinCode(PinCodeBase):
    id = db.Column(db.String(11), primary_key=True)


class CaptchaPinCode(PinCodeBase):
    id = db.Column(db.String(36), primary_key=True)


class EmailPinCode(PinCodeBase):
    id = db.Column(db.String(60), primary_key=True)
