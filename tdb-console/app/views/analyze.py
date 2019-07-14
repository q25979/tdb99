# -*- coding: utf-8 -*-
import time

import decimal
from flask import Blueprint
from flask import render_template
from flask import request
import flask_excel as excel
from flask_wtf import Form
from wtforms import StringField

from app.template_helpers.utils import format_currency
from app.views import Api
from app.views.admin import api_permission

analyze = Blueprint('analyze', __name__)
api_permission['analyze'] = ['/admin/wallet']


class FilterForm(Form):
    created_begin_timestamp = StringField('created_begin_timestamp')
    created_end_timestamp = StringField('created_end_timestamp')


def filter_params(filter_form):
    params = {}

    if request.args.get('created_begin_timestamp'):
        params['created_begin_timestamp'] = int(time.mktime(
            time.strptime(request.args.get('created_begin_timestamp'), u"%Y年%m月%d日")))
        filter_form.created_begin_timestamp.data = request.args.get('created_begin_timestamp')
    if request.args.get('created_end_timestamp'):
        params['created_end_timestamp'] = int(time.mktime(
            time.strptime(request.args.get('created_end_timestamp') + u' 23:59:59', u"%Y年%m月%d日 %H:%M:%S")))
        filter_form.created_end_timestamp.data = request.args.get('created_end_timestamp')

    return params


@analyze.route('/')
def index():
    filter_form = FilterForm()
    params = filter_params(filter_form)
    analysis_data = Api.get('/admin/wallet/day/statistics', params)

    data = [[k,
             format_currency(v.get('recharge', '0')),
             format_currency(v.get('deduction', '0')),
             format_currency(v.get('static_profit', '0')),
             format_currency(v.get('dynamic_profit', '0')),
             format_currency(v.get('node_profit', '0')),
             format_currency(v.get('free_coin', '0')),
             format_currency(v.get('transfer', '0')),
             format_currency(v.get('withdraw', '0')),
             format_currency(v.get('block_recharge', '0')),
             format_currency(v.get('buy_product', '0')),
             format_currency(v.get('reinvestment', '0')),
             format_currency(v.get('buy_order', '0')),
             format_currency(v.get('sell_order', '0')),
             ] for k, v in analysis_data.items()]
    day_data = sorted(data, key=lambda x: x[0])

    recharge = sum([decimal.Decimal(x[1]) for x in data])
    deduction = sum([decimal.Decimal(x[2]) for x in data])
    static_profit = sum([decimal.Decimal(x[3]) for x in data])
    dynamic_profit = sum([decimal.Decimal(x[4]) for x in data])
    node_profit = sum([decimal.Decimal(x[5]) for x in data])
    free_coin = sum([decimal.Decimal(x[6]) for x in data])
    transfer = sum([decimal.Decimal(x[7]) for x in data])
    withdraw = sum([decimal.Decimal(x[8]) for x in data])
    block_recharge = sum([decimal.Decimal(x[9]) for x in data])
    buy_product = sum([decimal.Decimal(x[10]) for x in data])
    reinvestment = sum([decimal.Decimal(x[11]) for x in data])
    buy_order = sum([decimal.Decimal(x[12]) for x in data])
    sell_order = sum([decimal.Decimal(x[13]) for x in data])

    data = {
        'recharge': format_currency(recharge),
        'deduction': format_currency(deduction),
        'static_profit': format_currency(static_profit),
        'dynamic_profit': format_currency(dynamic_profit),
        'node_profit': format_currency(node_profit),
        'free_coin': format_currency(free_coin),
        'transfer': format_currency(transfer),
        'withdraw': format_currency(withdraw),
        'block_recharge': format_currency(block_recharge),
        'buy_product': format_currency(buy_product),
        'reinvestment': format_currency(reinvestment),
        'buy_order': format_currency(buy_order),
        'sell_order': format_currency(sell_order),
    }

    return render_template('wallet/analyze.html',
                           filter_form=filter_form,
                           day_data=day_data,
                           data=data)


@analyze.route('/download')
def download():
    filter_form = FilterForm()
    params = filter_params(filter_form)
    analysis_data = Api.get('/admin/wallet/day/statistics', params)

    fields = [[u'时间',
               u'系统充值',
               u'系统扣减',
               u'静态收益',
               u'动态收益',
               u'节点收益',
               u'冻结释放',
               u'转账',
               u'提币',
               u'区块充值',
               u'购买商品',
               u'复投',
               u'交易(买单)',
               u'交易(卖单)']]

    data = [[k,
             format_currency(v.get('recharge', '0')),
             format_currency(v.get('deduction', '0')),
             format_currency(v.get('static_profit', '0')),
             format_currency(v.get('dynamic_profit', '0')),
             format_currency(v.get('node_profit', '0')),
             format_currency(v.get('free_coin', '0')),
             format_currency(v.get('transfer', '0')),
             format_currency(v.get('withdraw', '0')),
             format_currency(v.get('block_recharge', '0')),
             format_currency(v.get('buy_product', '0')),
             format_currency(v.get('reinvestment', '0')),
             format_currency(v.get('buy_order', '0')),
             format_currency(v.get('sell_order', '0')),
             ] for k, v in analysis_data.items()]
    day_data = sorted(data, key=lambda x: x[0])

    recharge = sum([decimal.Decimal(x[1]) for x in data])
    deduction = sum([decimal.Decimal(x[2]) for x in data])
    static_profit = sum([decimal.Decimal(x[3]) for x in data])
    dynamic_profit = sum([decimal.Decimal(x[4]) for x in data])
    node_profit = sum([decimal.Decimal(x[5]) for x in data])
    free_coin = sum([decimal.Decimal(x[6]) for x in data])
    transfer = sum([decimal.Decimal(x[7]) for x in data])
    withdraw = sum([decimal.Decimal(x[8]) for x in data])
    block_recharge = sum([decimal.Decimal(x[9]) for x in data])
    buy_product = sum([decimal.Decimal(x[10]) for x in data])
    reinvestment = sum([decimal.Decimal(x[11]) for x in data])
    buy_order = sum([decimal.Decimal(x[12]) for x in data])
    sell_order = sum([decimal.Decimal(x[13]) for x in data])

    total = [[u'合计',
              format_currency(recharge),
              format_currency(deduction),
              format_currency(static_profit),
              format_currency(dynamic_profit),
              format_currency(node_profit),
              format_currency(free_coin),
              format_currency(transfer),
              format_currency(withdraw),
              format_currency(block_recharge),
              format_currency(buy_product),
              format_currency(reinvestment),
              format_currency(buy_order),
              format_currency(sell_order)]]

    return excel.make_response_from_array(fields + day_data + total, "xls", file_name='财务统计')
