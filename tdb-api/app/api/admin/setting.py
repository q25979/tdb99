# -*- coding: utf-8 -*-
import json

from flask import Blueprint
from flask_restful import Resource, fields, marshal_with, Api, reqparse, abort

from app.api import AddResource
from app.api.admin import admin_sys_login_required
from app.model import db
from app.model.setting import Setting

setting_bp = Blueprint('admin_setting_bp', __name__)
setting_api = AddResource(Api(setting_bp))

admin_setting_fields = {
    "name": fields.String,
    "title": fields.String,
    "value": fields.Raw(attribute=lambda x: json.loads(x.value)),
    "description": fields.Raw(attribute=lambda x: json.loads(x.description))
}


@setting_api.add_resource('/general_option')
class AdminSettingGeneralOptionApi(Resource):
    decorators = [admin_sys_login_required]

    @marshal_with(admin_setting_fields)
    def get(self):
        return Setting.query.get('general_option')

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('evaluation_reward_amount', type=int, location='json')
        parser.add_argument('lebo_price', type=str, location='json')
        parser.add_argument('lebo_change_price_cnt', type=int, location='json')
        parser.add_argument('lebo_price_step', type=str, location='json')
        parser.add_argument('transaction_allow_amount', type=int, location='json')
        parser.add_argument('sell_amount', type=int, location='json')
        parser.add_argument('sell_people', type=int, location='json')
        parser.add_argument('buy_people', type=int, location='json')
        parser.add_argument('buy_count', type=int, location='json')
        parser.add_argument('sell_count', type=int, location='json')
        parser.add_argument('order_fee_rate', type=str, location='json')
        parser.add_argument('contact_us', type=str, location='json')
        parser.add_argument('buy_sell_free_amount', type=int, location='json')
        parser.add_argument('buy_sell_rate', type=str, location='json')
        parser.add_argument('transaction_free_generation', type=int, location='json')
        parser.add_argument('transaction_free_amount', type=int, location='json')
        parser.add_argument('exchange_amount_min', type=int, location='json')
        parser.add_argument('exchange_amount_max', type=int, location='json')
        parser.add_argument('community_transaction_day_cnt', type=int, location='json')
        parser.add_argument('community_line_people_cnt', type=int, location='json')
        parser.add_argument('community_dividend_rate', type=str, location='json')
        parser.add_argument('community_transaction_fee_rate', type=str, location='json')
        parser.add_argument('community_free_amount', type=int, location='json')
        parser.add_argument('community_free_generation', type=int, location='json')
        parser.add_argument('order_status_change_time', type=int, location='json')
        parser.add_argument('match_order_cnt', type=int, location='json')
        parser.add_argument('dollar2rmb', type=str, location='json')
        parser.add_argument('recommend_reward_amount', type=list, location='json')
        parser.add_argument('transaction_time_begin', type=list, location='json')
        parser.add_argument('transaction_time_end', type=list, location='json')
        parser.add_argument('community_node_cnt', type=list, location='json')
        parser.add_argument('community_total_balance', type=list, location='json')
        parser.add_argument('community_sponsor_cnt', type=list, location='json')
        parser.add_argument('community_line_cnt', type=list, location='json')

        parsed_args = parser.parse_args()

        setting = Setting.query.get('general_option')
        option = json.loads(setting.value)

        if parsed_args['evaluation_reward_amount'] is not None:
            option['evaluation_reward_amount'] = parsed_args['evaluation_reward_amount']

        if parsed_args['lebo_price'] is not None:
            option['lebo_price'] = parsed_args['lebo_price']

        if parsed_args['lebo_change_price_cnt'] is not None:
            option['lebo_change_price_cnt'] = parsed_args['lebo_change_price_cnt']

        if parsed_args['lebo_price_step'] is not None:
            option['lebo_price_step'] = parsed_args['lebo_price_step']

        if parsed_args['transaction_allow_amount'] is not None:
            option['transaction_allow_amount'] = parsed_args['transaction_allow_amount']

        if parsed_args['sell_amount'] is not None:
            option['sell_amount'] = parsed_args['sell_amount']

        if parsed_args['sell_people'] is not None:
            option['sell_people'] = parsed_args['sell_people']

        if parsed_args['buy_people'] is not None:
            option['buy_people'] = parsed_args['buy_people']

        if parsed_args['buy_count'] is not None:
            option['buy_count'] = parsed_args['buy_count']

        if parsed_args['sell_count'] is not None:
            option['sell_count'] = parsed_args['sell_count']

        if parsed_args['order_fee_rate'] is not None:
            option['order_fee_rate'] = parsed_args['order_fee_rate']

        if parsed_args['contact_us'] is not None:
            option['contact_us'] = parsed_args['contact_us']

        if parsed_args['buy_sell_free_amount'] is not None:
            option['buy_sell_free_amount'] = parsed_args['buy_sell_free_amount']

        if parsed_args['buy_sell_rate'] is not None:
            option['buy_sell_rate'] = parsed_args['buy_sell_rate']

        if parsed_args['transaction_free_generation'] is not None:
            option['transaction_free_generation'] = parsed_args['transaction_free_generation']

        if parsed_args['transaction_free_amount'] is not None:
            option['transaction_free_amount'] = parsed_args['transaction_free_amount']

        if parsed_args['exchange_amount_min'] is not None:
            option['exchange_amount_min'] = parsed_args['exchange_amount_min']

        if parsed_args['exchange_amount_max'] is not None:
            option['exchange_amount_max'] = parsed_args['exchange_amount_max']

        if parsed_args['community_transaction_day_cnt'] is not None:
            option['community_transaction_day_cnt'] = parsed_args['community_transaction_day_cnt']

        if parsed_args['community_line_people_cnt'] is not None:
            option['community_line_people_cnt'] = parsed_args['community_line_people_cnt']

        if parsed_args['community_dividend_rate'] is not None:
            option['community_dividend_rate'] = parsed_args['community_dividend_rate']

        if parsed_args['community_transaction_fee_rate'] is not None:
            option['community_transaction_fee_rate'] = parsed_args['community_transaction_fee_rate']

        if parsed_args['community_free_amount'] is not None:
            option['community_free_amount'] = parsed_args['community_free_amount']

        if parsed_args['community_free_generation'] is not None:
            option['community_free_generation'] = parsed_args['community_free_generation']

        if parsed_args['order_status_change_time'] is not None:
            option['order_status_change_time'] = parsed_args['order_status_change_time']

        if parsed_args['match_order_cnt'] is not None:
            option['match_order_cnt'] = parsed_args['match_order_cnt']

        if parsed_args['lebo_change_price_cnt'] is not None:
            option['lebo_change_price_cnt'] = parsed_args['lebo_change_price_cnt']

        if parsed_args['lebo_price_step'] is not None:
            option['lebo_price_step'] = str(parsed_args['lebo_price_step'])

        if parsed_args['exchange_amount_max'] is not None:
            option['exchange_amount_max'] = parsed_args['exchange_amount_max']

        if parsed_args['dollar2rmb'] is not None:
            option['dollar2rmb'] = parsed_args['dollar2rmb']

        if parsed_args['recommend_reward_amount']:
            if len(parsed_args['recommend_reward_amount']) != 10:
                abort(400, code=1000, message={'recommend_reward_amount': 'The length must be 10'})
            option['recommend_reward_amount'] = parsed_args['recommend_reward_amount']

        if parsed_args['transaction_time_begin']:
            if len(parsed_args['transaction_time_begin']) != 2:
                abort(400, code=1000, message={'transaction_time_begin': 'The length must be 2'})
            option['transaction_time_begin'] = parsed_args['transaction_time_begin']

        if parsed_args['transaction_time_end']:
            if len(parsed_args['transaction_time_end']) != 2:
                abort(400, code=1000, message={'transaction_time_end': 'The length must be 2'})
            option['transaction_time_end'] = parsed_args['transaction_time_end']

        if parsed_args['community_total_balance']:
            if len(parsed_args['community_total_balance']) != 3:
                abort(400, code=1000, message={'community_total_balance': 'The length must be 3'})
            option['community_total_balance'] = parsed_args['community_total_balance']

        if parsed_args['community_sponsor_cnt']:
            if len(parsed_args['community_sponsor_cnt']) != 3:
                abort(400, code=1000, message={'community_sponsor_cnt': 'The length must be 3'})
            option['community_sponsor_cnt'] = parsed_args['community_sponsor_cnt']

        setting.value = json.dumps(option)
        db.session.commit()
        return option
