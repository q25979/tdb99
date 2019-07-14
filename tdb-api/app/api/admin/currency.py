# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import abort, fields, marshal_with, Resource, Api
from app.api import AddResource, CustomRequestParser, pagination_query

from app.model import DecimalToString, timestamp_to_datetime
from app.model.currency import Currency, CurrencyPriceRecord

currency_bp = Blueprint('admin_currency_bp', __name__)
currency_api = AddResource(Api(currency_bp))

admin_currency_fields = {
    'usd_price': DecimalToString,
    'transaction_cnt': fields.Integer,
    'today_transaction_amount': fields.Integer
}


@currency_api.add_resource('/usd_price')
class AdminCurrencyApi(Resource):

    @marshal_with(admin_currency_fields)
    def get(self):
        currency = Currency.get_currency()
        if currency is None:
            abort(400, code=1001, message={'currency': 'currency does not exist'})
        return currency


admin_currency_price_record_fields = {
    'created_timestamp': fields.Integer,
    'current_price': DecimalToString,
    'delta_price': DecimalToString,
    'transaction_cnt': fields.Integer
}

admin_currency_price_record_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(admin_currency_price_record_fields))
}


@currency_api.add_resource('/price_record')
class AdminCurrencyPriceRecordApi(Resource):

    @marshal_with(admin_currency_price_record_list_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('create_begin_timestamp', type=int, location='args')
        parser.add_argument('create_end_timestamp', type=int, location='args')
        parsed_args = parser.parse_args()

        q = CurrencyPriceRecord.query
        if parsed_args['create_begin_timestamp'] is not None:
            create_begin_datetime = timestamp_to_datetime(parsed_args['create_begin_timestamp'])
            q = q.filter(CurrencyPriceRecord.created_at >= create_begin_datetime)
        if parsed_args['create_end_timestamp'] is not None:
            create_end_datetime = timestamp_to_datetime(parsed_args['create_end_timestamp'])
            q = q.filter(CurrencyPriceRecord.created_at < create_end_datetime)
        q = q.order_by(CurrencyPriceRecord.id.asc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)
