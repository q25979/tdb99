# -*- coding: utf-8 -*-

import time
import decimal
import urllib2

import flask_excel as excel
from flask import Blueprint, render_template, request, jsonify
from flask_wtf import Form
from wtforms import StringField, SelectField

from app.template_helpers.utils import timestamp_to_str, format_currency
from app.views import Api
from app.views.admin import api_permission

wallet = Blueprint('wallet', __name__)
api_permission['wallet'] = ['/admin/withdraw', '/admin/wallet']

CHOOSE_ALL = [('', u'全部')]

WALLET_TYPE_FLAG = [('1', u'总资产钱包'),
                    ('2', u'社区钱包'),
                    ('4', u'交易钱包')]

AMOUNT_TYPE = [('0', u'全部'),
               ('1', u'>=0'),
               ('2', u'<0')]

TYPE_FLAG = [(1, u'测评奖励'),
             (2, u'充值'),
             (4, u'买'),
             (8, u'卖'),
             (16, u'推荐奖励'),
             (32, u'买卖释放'),
             (64, u'加速释放'),
             (128, u'兑换'),
             (256, u'转账'),
             (512, u'分红')
             ]

STATUS_FLAG = [(1, u'申请'),
               (2, u'完成'),
               (4, u'驳回')]


class FilterForm(Form):
    created_begin_timestamp = StringField('created_begin_timestamp')
    created_end_timestamp = StringField('created_end_timestamp')
    record_type = SelectField('record_type', choices=CHOOSE_ALL + TYPE_FLAG)
    amount_type = SelectField('amount_type', choices=AMOUNT_TYPE)
    assets_type = SelectField('assets_type', choices=CHOOSE_ALL + WALLET_TYPE_FLAG)
    mobile = StringField('mobile')


class WithdrawForm(Form):
    created_begin_timestamp = StringField('created_begin_timestamp')
    created_end_timestamp = StringField('created_end_timestamp')
    currency_code = SelectField('currency_code', choices=CHOOSE_ALL + WALLET_TYPE_FLAG)
    status = SelectField('status', choices=CHOOSE_ALL + STATUS_FLAG)


class AssetsForm(Form):
    currency_code = SelectField('currency_code', choices=CHOOSE_ALL + WALLET_TYPE_FLAG)
    assets_type = SelectField('assets_type', choices=CHOOSE_ALL + WALLET_TYPE_FLAG)
    address = StringField('address')
    uid = StringField('uid')
    mobile = StringField('mobile')


@wallet.route('/')
def index():
    filter_form = FilterForm()
    return render_template('wallet/wallet.html', filter_form=filter_form, TYPE_FLAG=dict(TYPE_FLAG),
                           WALLET_TYPE_FLAG=dict(WALLET_TYPE_FLAG))


@wallet.route('/assets')
def assets():
    filter_form = AssetsForm()
    return render_template('wallet/assets.html', filter_form=filter_form)


@wallet.route('/withdraw')
def withdraw():
    filter_form = WithdrawForm()
    return render_template('wallet/withdraw.html',
                           filter_form=filter_form,
                           STATUS_FLAG=dict(STATUS_FLAG))


@wallet.route('/ajax/list', methods=['POST'])
def ajax_list():
    params = request.get_json()
    if params['query'].get('created_begin_timestamp'):
        params['query']['created_begin_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_begin_timestamp'], u"%Y年%m月%d日")))
    if params['query'].get('created_end_timestamp'):
        params['query']['created_end_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_end_timestamp'] + u' 23:59:59', u"%Y年%m月%d日 %H:%M:%S")))
    data = Api.get('/admin/assets/record', params['query'])
    total_records = data['total_count']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['objects']
    }
    return jsonify(return_dict)


@wallet.route('/ajax/withdraw_list', methods=['POST'])
def ajax_withdraw_list():
    params = request.get_json()
    if params['query'].get('created_begin_timestamp'):
        params['query']['created_begin_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_begin_timestamp'], u"%Y年%m月%d日")))
    if params['query'].get('created_end_timestamp'):
        params['query']['created_end_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_end_timestamp'] + u' 23:59:59', u"%Y年%m月%d日 %H:%M:%S")))
    data = Api.get('/admin/order', params['query'])
    total_records = data['total_count']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['objects']
    }
    return jsonify(return_dict)


@wallet.route('/ajax/assets_list', methods=['POST'])
def assets_ajax_list():
    params = request.get_json()

    data = Api.get('/admin/assets', params['query'])
    total_records = data['total_count']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['objects']
    }
    return jsonify(return_dict)


@wallet.route('/ajax/withdraw/confirm', methods=['POST'])
def ajax_withdraw_confirm():
    params = request.get_json()
    result = Api.post('/admin/order/withdraw/confirm/' + urllib2.quote(str(params['number'])), {})
    return jsonify(result)


@wallet.route('/ajax/withdraw/cancel', methods=['POST'])
def ajax_withdraw_cancel():
    params = request.get_json()
    result = Api.post('/admin/order/withdraw/cancel/' + urllib2.quote(str(params['number'])), {})
    return jsonify(result)


@wallet.route('/ajax/recharge', methods=['POST'])
def ajax_recharge():
    params = request.get_json()
    result = Api.post('/admin/assets/recharge', params)
    return jsonify(result)


@wallet.route('/withdraw/download')
def withdraw_download():
    params = {}
    for key, value in request.args.items():
        if value != '':
            params[key] = value

    params['per_page'] = 10000
    if params.get('created_begin_timestamp'):
        params['created_begin_timestamp'] = int(time.mktime(
            time.strptime(params['created_begin_timestamp'], u"%Y年%m月%d日")))
    if params.get('created_end_timestamp'):
        params['created_end_timestamp'] = int(time.mktime(
            time.strptime(params['created_end_timestamp'] + u' 23:59:59', u"%Y年%m月%d日 %H:%M:%S")))

    params['per_page'] = 10000
    member_data = Api.get('/admin/withdraw', params)
    status = dict(STATUS_FLAG)
    fields = [[u'时间',
               u'用户编号',
               u'提现数量',
               u'手续费',
               u'提现地址',
               u'交易哈希',
               u'状态']]

    data = [[timestamp_to_str(y['created_timestamp']),
             y['user']['uid'],
             format_currency(y['amount']),
             format_currency(y['fee']),
             y['address'],
             y['txid'],
             status[y['status']]]
            for y in member_data['items']]

    return excel.make_response_from_array(fields + data, "xls", file_name='提现')


@wallet.route('/record/download')
def record_download():
    params = {}
    for key, value in request.args.items():
        if value != '':
            params[key] = value

    params['per_page'] = 10000
    if params.get('created_begin_timestamp'):
        params['created_begin_timestamp'] = int(time.mktime(
            time.strptime(params['created_begin_timestamp'], u"%Y年%m月%d日")))
    if params.get('created_end_timestamp'):
        params['created_end_timestamp'] = int(time.mktime(
            time.strptime(params['created_end_timestamp'] + u' 23:59:59', u"%Y年%m月%d日 %H:%M:%S")))

    params['per_page'] = 10000
    member_data = Api.get('/admin/wallet/record', params)
    wallet_type = dict(WALLET_TYPE_FLAG)
    type_flag = dict(TYPE_FLAG)

    fields = [[u'创建时间',
               u'用户编号',
               u'变化后余额',
               u'变化量',
               u'钱包类型',
               u'来源',
               u'详情信息']]

    data = [[timestamp_to_str(y['created_timestamp']),
             y['user']['uid'],
             format_currency(y['current_amount']),
             format_currency(y['delta_amount']),
             wallet_type[y['wallet_type']],
             type_flag[y['type']],
             y['details']['message']]
            for y in member_data['items']]

    return excel.make_response_from_array(fields + data, "xls", file_name='钱包记录')


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


@wallet.route('/analyze')
def analyze():
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
