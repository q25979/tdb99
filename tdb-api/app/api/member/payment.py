# -*- coding: utf-8 -*-
import datetime
import uuid
from flask import Blueprint, g, request, url_for
from flask_restful import Api, abort, fields, marshal_with, Resource

from app.api import pagination_query, restful_api, CustomRequestParser, UrlNormalize, AddResource
from app.api.member import member_login_required
from app.model import db, Datetime2Timestamp, DecimalToString
from app.model.payment import Payment, g_payment_type

payment_bp = Blueprint('member_payment_bp', __name__)
payment_api = AddResource(Api(payment_bp))

member_payment_user_fields = {
    'id': fields.String,
    'uid': fields.String,
    'name': fields.String
}

member_payment_fields = {
    'id': fields.String,
    'user': fields.Nested(member_payment_user_fields),
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

member_payment_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(member_payment_fields))
}


@payment_api.add_resource('/list')
class MemberPaymentListApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_payment_list_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('type', type=int, choices=(g_payment_type.BANK, g_payment_type.WECHAT,
                                                       g_payment_type.ALIPAY, g_payment_type.USDT), location='args')
        parser.add_argument('invalid', type=int, default=0, location='args')
        parsed_args = parser.parse_args()

        q = Payment.query.filter_by(user_id=g.current_user.id)
        if parsed_args['type'] is not None:
            q = q.filter(Payment.type == parsed_args['type'])
        if parsed_args['invalid'] is not None:
            q = q.filter(Payment.invalid == parsed_args['invalid'])

        q = q.order_by(Payment.created_at.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)

    @marshal_with(member_payment_fields)
    def post(self):
        parser = CustomRequestParser()
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
        parser.add_argument('security_password', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        if not g.current_user.security_password:
            abort(400, code=1012, message={'security_password': 'security password is empty'})
        if not g.current_user.verify_security_password(parsed_args['security_password']):
            abort(400, code=1002, message={'security_password': 'security_password does not match'})

        payment = Payment.get_payment(g.current_user.id, parsed_args['type'])
        if payment is not None:
            abort(400, code=1006, message={'type': 'payment type does exist'})

        if parsed_args['type'] == g_payment_type.BANK:
            if parsed_args['name'] is None or parsed_args['bank'] is None or parsed_args['card_number'] is None:
                abort(400, code=1001, message={'payment': 'name|bank|card_number does not exist'})
            payment = Payment(user_id=g.current_user.id, type=parsed_args['type'], name=parsed_args['name'],
                              bank=parsed_args['bank'], card_number=parsed_args['card_number'])
        elif parsed_args['type'] == g_payment_type.WECHAT:
            if parsed_args['name'] is None or parsed_args['wechat'] is None:
                abort(400, code=1001, message={'payment': 'name|wechat does not exist'})
            payment = Payment(user_id=g.current_user.id, type=parsed_args['type'], name=parsed_args['name'],
                              wechat=parsed_args['wechat'], wechat_image=parsed_args['wechat_image'])
        elif parsed_args['type'] == g_payment_type.ALIPAY:
            if parsed_args['name'] is None or parsed_args['alipay'] is None:
                abort(400, code=1001, message={'payment': 'name|alipay does not exist'})
            payment = Payment(user_id=g.current_user.id, type=parsed_args['type'], name=parsed_args['name'],
                              alipay=parsed_args['alipay'], alipay_image=parsed_args['alipay_image'])
        else:
            if parsed_args['address'] is None:
                abort(400, code=1001, message={'payment': 'address does not exist'})
            payment = Payment(user_id=g.current_user.id, type=parsed_args['type'], address=parsed_args['address'],
                              remark=parsed_args['remark'])

        db.session.add(payment)
        db.session.commit()
        return payment


@payment_api.add_resource('/details/<string:payment_id>')
class MemberPaymentDetailsApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_payment_fields)
    def get(self, payment_id):
        payment = Payment.query.filter(Payment.id == payment_id, Payment.user_id == g.current_user.id).first()
        if payment is None:
            abort(400, code=1001, message={'payment': 'payment does not exist'})
        return payment

    # def delete(self, payment_id):
    #     payment = Payment.query.get(payment_id)
    #     if payment is None:
    #         abort(400, code=1001, message={'payment': 'payment does not exist'})
    #
    #     return payment.delete()
