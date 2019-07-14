# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import abort, fields, marshal_with, Resource, Api

from app.api import AddResource, CustomRequestParser, pagination_query
from app.model import DecimalToString, timestamp_to_datetime
from app.model.currency import Currency, CryptoCurrency, FiatCurrency, CurrencyPriceRecord

currency_bp = Blueprint('member_currency_bp', __name__)
currency_api = AddResource(Api(currency_bp))

member_currency_fields = {
    'usd_price': DecimalToString,
    'transaction_cnt': fields.Integer,
    'today_transaction_amount': fields.Integer
}


@currency_api.add_resource('/usd_price')
class MemberCurrencyApi(Resource):

    @marshal_with(member_currency_fields)
    def get(self):
        currency = Currency.get_currency()
        if currency is None:
            abort(400, code=1001, message={'currency': 'currency does not exist'})
        return currency


member_currency_price_record_fields = {
    'created_timestamp': fields.Integer,
    'current_price': DecimalToString,
    'delta_price': DecimalToString,
    'transaction_cnt': fields.Integer,
}

member_currency_price_record_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(member_currency_price_record_fields))
}


@currency_api.add_resource('/price_record')
class MemberCurrencyPriceRecordApi(Resource):

    @marshal_with(member_currency_price_record_list_fields)
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
        q = q.order_by(CurrencyPriceRecord.id.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)


member_crypto_currency_fields = {
    'currency_code': fields.String,
    'erc20_token': fields.Integer,
    'usd_price': DecimalToString,
    'percent_change': DecimalToString  # 涨幅
}


@currency_api.add_resource('/cryptocurrency')
class MemberQueryCryptoCurrencyApi(Resource):
    @marshal_with(member_crypto_currency_fields, envelope='objects')
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('currency_list', type=str, location='args')
        parsed_args = parser.parse_args()

        if parsed_args['currency_list']:
            currency_list = parsed_args['currency_list'].split(',')
            q = CryptoCurrency.query.filter(CryptoCurrency.currency_code.in_(currency_list))
        else:
            q = CryptoCurrency.query
        q = q.order_by(CryptoCurrency.sequence.asc())
        return q.all()


member_fiat_currency_fields = {
    'country': fields.String,
    'country_code': fields.String,
    'currency': fields.String,
    'currency_code': fields.String,
    'usd_rate': DecimalToString
}


@currency_api.add_resource('/currency')
class MemberQueryFiatCurrencyApi(Resource):
    @marshal_with(member_fiat_currency_fields, envelope='objects')
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('currency_list', type=str, location='args')
        parsed_args = parser.parse_args()

        if parsed_args['currency_list']:
            currency_list = parsed_args['currency_list'].split(',')
            q = FiatCurrency.query.filter(FiatCurrency.currency_code.in_(currency_list))
        else:
            q = FiatCurrency.query
        q = q.order_by(FiatCurrency.sequence.asc())
        return q.all()
