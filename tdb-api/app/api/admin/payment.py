# -*- coding: utf-8 -*-
import datetime
import uuid
from flask import Blueprint, g, request, url_for
from flask_restful import Api, abort, fields, marshal_with, Resource

from app.api import pagination_query, restful_api, CustomRequestParser, UrlNormalize, AddResource
from app.api.admin import admin_login_required
from app.model import db, Datetime2Timestamp, DecimalToString
from app.model.payment import Payment, g_payment_type
from app.model.user import User

payment_bp = Blueprint('admin_payment_bp', __name__)
payment_api = AddResource(Api(payment_bp))

admin_payment_user_fields = {
    'id': fields.String,
    'uid': fields.String,
    'name': fields.String
}

admin_payment_fields = {
    'id': fields.String,
    'user': fields.Nested(admin_payment_user_fields),
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

admin_payment_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(admin_payment_fields))
}


@payment_api.add_resource('/list')
class AdminPaymentListApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_payment_list_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('user_id', type=str, location='args')
        parser.add_argument('type', type=int, choices=(g_payment_type.BANK, g_payment_type.WECHAT,
                                                       g_payment_type.ALIPAY, g_payment_type.USDT), location='args')
        parser.add_argument('invalid', type=int, default=0, location='args')
        parsed_args = parser.parse_args()

        q = Payment.query
        if parsed_args['user_id'] is not None:
            q = q.filter(Payment.user_id == parsed_args['user_id'])
        if parsed_args['type'] is not None:
            q = q.filter(Payment.type == parsed_args['type'])
        if parsed_args['invalid'] is not None:
            q = q.filter(Payment.invalid == parsed_args['invalid'])

        q = q.order_by(Payment.created_at.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)

    @marshal_with(admin_payment_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('user_id', type=str, required=True, nullable=False, location='json')
        parser.add_argument('type', type=int, required=True, choices=(g_payment_type.BANK, g_payment_type.WECHAT,
                                                                      g_payment_type.ALIPAY, g_payment_type.USDT),
                            location='json')
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('bank', type=str, location='json')
        parser.add_argument('card_number', type=str, location='json')
        parser.add_argument('wechat', type=str, location='json')
        parser.add_argument('wechat_image', type=str, default='', location='json')
        parser.add_argument('alipay', type=str, location='json')
        parser.add_argument('alipay_image', type=str, default='', location='json')
        parser.add_argument('address', type=str, location='json')
        parser.add_argument('remark', type=str, default='', location='json')
        parsed_args = parser.parse_args()

        user = User.query.get(parsed_args['user_id'])
        if user is None:
            abort(400, code=1001, message={'user': 'user does not exist'})

        payment = Payment.get_payment(user.id, parsed_args['type'])
        if payment is not None:
            abort(400, code=1006, message={'type': 'payment type does exist'})

        if parsed_args['type'] == g_payment_type.BANK:
            if parsed_args['name'] is None and parsed_args['bank'] is None and parsed_args['card_number'] is None:
                abort(400, code=1001, message={'payment': 'name|bank|card_number does not exist'})
            payment = Payment(user_id=user.id, type=parsed_args['type'], name=parsed_args['name'],
                              bank=parsed_args['bank'], card_number=parsed_args['card_number'])
        elif parsed_args['type'] == g_payment_type.WECHAT:
            if parsed_args['name'] is None and parsed_args['wechat'] is None:
                abort(400, code=1001, message={'payment': 'name|wechat does not exist'})
            payment = Payment(user_id=user.id, type=parsed_args['type'], name=parsed_args['name'],
                              wechat=parsed_args['wechat'], wechat_image=parsed_args['wechat_image'])
        elif parsed_args['type'] == g_payment_type.ALIPAY:
            if parsed_args['name'] is None and parsed_args['alipay'] is None:
                abort(400, code=1001, message={'payment': 'name|alipay does not exist'})
            payment = Payment(user_id=user.id, type=parsed_args['type'], name=parsed_args['name'],
                              alipay=parsed_args['alipay'], alipay_image=parsed_args['alipay_image'])
        else:
            if parsed_args['address'] is None:
                abort(400, code=1001, message={'payment': 'address does not exist'})
            payment = Payment(user_id=user.id, type=parsed_args['type'], address=parsed_args['address'],
                              remark=parsed_args['remark'])

        db.session.add(payment)
        db.session.commit()
        return payment


@payment_api.add_resource('/details/<string:payment_id>')
class AdminPaymentDetailsApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_payment_fields)
    def get(self, payment_id):
        payment = Payment.query.get(payment_id)
        if payment is None:
            abort(400, code=1001, message={'payment': 'payment does not exist'})
        return payment

    @marshal_with(admin_payment_fields)
    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)
        if payment is None:
            abort(400, code=1001, message={'payment': 'payment does not exist'})

        payment.invalid = 1
        db.session.commit()
        return payment
