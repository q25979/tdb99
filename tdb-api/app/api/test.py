# -*- coding: utf-8 -*-
import datetime
import decimal
import time
import logging
from flask import Blueprint

from app import db
from app.model.assets import Assets, g_assets_record_type
from app.model.order import Order, g_order_status
from app.model.payment import Payment
from app.model.setting import Setting
from app.model.user import User

test = Blueprint('test', __name__)


@test.route('/')
def api_test():
    # start_time = time.time()
    # str_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # # order_people = Order.query.filter(Order.created_at >= str_time,
    # #                                   Order.status != g_order_status.CANCELLED,
    # #                                   ).group_by(Order.user_id).all()
    # order_people = db.session.query(Order.user_id).filter(Order.created_at >= str_time,
    #                                                       Order.status != g_order_status.CANCELLED,
    #                                                       ).group_by(Order.user_id).count()
    # # order_people_id = [x.user_id for x in order_people]
    # logging.info('test_time:{}'.format(time.time() - start_time))

    # user_list = User.query.filter(
    #     User.mobile.in_(['15091423454', '13720512067', '13553399417', '15002274995', '16637144591']))
    # option = Setting.get_json('general_option')
    # buy_sell_free_amount = option['buy_sell_free_amount']
    # buy_sell_rate = decimal.Decimal(option['buy_sell_rate'])
    # for user in user_list:
    #     fee = 500 * buy_sell_rate
    #     amount = buy_sell_free_amount - fee
    #     detail = {
    #         'message': '成功买卖各一单，释放数量：{}， 单数量：{}， 扣除手续费：{}'.format(
    #             buy_sell_free_amount, 500, fee)
    #     }
    #     assets = Assets.get_assets(user.id)
    #     if assets.update_total_balance(-buy_sell_free_amount, g_assets_record_type.BUY_SELL_FREE, detail):
    #         assets.update_transaction_balance(amount, g_assets_record_type.BUY_SELL_FREE, detail)
    #
    #     sell_user = user
    #     sell_user.update_today_have_transaction()
    #     sell_user.update_transaction_free()
    #
    # db.session.commit()

    return 'lebo-api v1.0'
