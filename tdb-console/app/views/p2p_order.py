# -*- coding: utf-8 -*-
import urllib2
from decimal import Decimal
import flask_excel as excel

import time
from flask import Blueprint, render_template, request, jsonify
from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import NumberRange

from app.template_helpers.utils import timestamp_to_str, format_currency
from app.views import Api, ApiError, AppError
from app.views.admin import api_permission

p2p_order = Blueprint('p2p_order', __name__)
api_permission['p2p_order'] = ['/admin/order']

ORDER_STATUS_FLAG = [(2, u'匹配中'),
                     (4, u'已付款'),
                     (8, u'已确认')]

# ORDER_SIDE_FLAG = [(1, u'买单'),
#                    (2, u'卖单')]

CHOOSE_ALL = [('', u'全部')]


class OrderFilterForm(Form):
    created_begin_timestamp = StringField('created_begin_timestamp')
    created_end_timestamp = StringField('created_end_timestamp')
    # side = SelectField('side', choices=CHOOSE_ALL + ORDER_SIDE_FLAG)
    # name = StringField('name')
    number = StringField('number')
    buy_number = StringField('buy_number')
    mobile = StringField('mobile')
    buy_mobile = StringField('buy_mobile')
    status = SelectField('status', choices=CHOOSE_ALL + ORDER_STATUS_FLAG, default=2)
    # match_name = StringField('match_name')


class PendingFilterForm(Form):
    created_begin_timestamp = StringField('created_begin_timestamp')
    created_end_timestamp = StringField('created_end_timestamp')
    status = IntegerField('status', default=1)
    side = IntegerField('side')
    name = StringField('name')
    mobile = StringField('mobile')
    number = StringField('number')


class MatchOrderForm(Form):
    order_cnt = IntegerField('order_cnt',
                             validators=[NumberRange(min=0, message=u'请填写正确内容')])


@p2p_order.route('/')
def index():
    filter_form = OrderFilterForm()
    return render_template('p2p_order/list.html',
                           # ORDER_SIDE_FLAG=dict(ORDER_SIDE_FLAG),
                           filter_form=filter_form)


@p2p_order.route('/statistics')
def statistics():
    sell_pending_cnt = Api.get('/admin/order/sell_pending_cnt')['cnt']
    buy_pending_cnt = Api.get('/admin/order/buy_pending_cnt')['cnt']
    match_cnt = Api.get('/admin/order/match_cnt')['cnt']
    confirmed_cnt = Api.get('/admin/order/confirmed_cnt')['cnt']
    register_cnt = Api.get('/admin/order/register_cnt')['cnt']
    active_cnt = Api.get('/admin/order/active_cnt')['cnt']
    match_form = MatchOrderForm()
    return render_template('p2p_order/statistics.html',
                           match_form=match_form,
                           sell_pending_cnt=sell_pending_cnt,
                           buy_pending_cnt=buy_pending_cnt,
                           match_cnt=match_cnt,
                           confirmed_cnt=confirmed_cnt,
                           register_cnt=register_cnt,
                           active_cnt=active_cnt)


@p2p_order.route('/ajax/match_task', methods=['POST'])
def ajax_match_task():
    match_form = MatchOrderForm()
    if match_form.validate():
        data = Api.post('/admin/order/start_match', match_form.data)
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, match_form.errors)


@p2p_order.route('/ajax/match_list', methods=['POST'])
def ajax_match_list():
    params = request.get_json()
    if params['query'].get('created_begin_timestamp'):
        params['query']['created_begin_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_begin_timestamp'], u"%Y年%m月%d日")))
    if params['query'].get('created_end_timestamp'):
        params['query']['created_end_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_end_timestamp'] + u' 23:59:59', u"%Y年%m月%d日 %H:%M:%S")))
    data = Api.get('/admin/order/match_order', params['query'])
    total_records = data['total_count']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['objects']
    }
    return jsonify(return_dict)


@p2p_order.route('/sell')
def sell_pending():
    filter_form = PendingFilterForm()
    filter_form.side.data = 2
    return render_template('p2p_order/pending_list.html',
                           # ORDER_SIDE_FLAG=dict(ORDER_SIDE_FLAG),
                           title=u'挂卖单',
                           filter_form=filter_form)


@p2p_order.route('/buy')
def buy_pending():
    filter_form = PendingFilterForm()
    filter_form.side.data = 1
    return render_template('p2p_order/pending_list.html',
                           # ORDER_SIDE_FLAG=dict(ORDER_SIDE_FLAG),
                           title=u'挂买单',
                           filter_form=filter_form)


@p2p_order.route('/cancel')
def cancel():
    filter_form = PendingFilterForm()
    filter_form.status.data = 16

    return render_template('p2p_order/cancel_list.html',
                           # ORDER_SIDE_FLAG=dict(ORDER_SIDE_FLAG),
                           title=u'取消订单',
                           filter_form=filter_form)


@p2p_order.route('/ajax/list', methods=['POST'])
def ajax_list():
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


@p2p_order.route('/details/<string:id>')
def details(id):
    data = Api.get('/admin/order/sell/detail/' + urllib2.quote(id))
    sell_user = data['user']
    buy_user = data['match_order']['buy_user']
    payment_dic = {}
    payment_flag = ['bank_payment', 'wechat_payment', 'alipay_payment', 'usdt_payment']
    for item in data['all_payment']:
        payment_dic[payment_flag[item['type']]] = item
    return render_template('p2p_order/details.html',
                           data=data,
                           payment_dic=payment_dic,
                           sell_user=sell_user,
                           buy_user=buy_user,
                           ORDER_STATUS_FLAG=dict(ORDER_STATUS_FLAG))


@p2p_order.route('/ajax/modify_order', methods=['POST'])
def ajax_modify_order():
    params = request.get_json()
    number = str(params.pop('number'))
    data = Api.put('/admin/order/detail/' + urllib2.quote(number), params)
    return jsonify(data)


@p2p_order.route('/ajax/priority_order', methods=['POST'])
def ajax_priority_order():
    params = request.get_json()
    number = str(params.pop('number'))
    data = Api.put('/admin/order/priority/' + urllib2.quote(number), params)
    return jsonify(data)
#
# @p2p_order.route('/order/download')
# def order_download():
#     params = {}
#     for key, value in request.args.items():
#         if value != '':
#             params[key] = value
#
#     params['per_page'] = 10000
#     # if params.get('created_begin_timestamp'):
#     #     params['created_begin_timestamp'] = int(time.mktime(
#     #         time.strptime(params['created_begin_timestamp'], u"%Y年%m月%d日")))
#     # if params.get('created_end_timestamp'):
#     #     params['created_end_timestamp'] = int(time.mktime(
#     #         time.strptime(params['created_end_timestamp'] + u' 23:59:59', u"%Y年%m月%d日 %H:%M:%S")))
#
#     params['per_page'] = 10000
#     data = Api.get('/admin/order', params)
#     order_side = dict(ORDER_SIDE_FLAG)
#     order_status = dict(ORDER_STATUS_FLAG)
#
#     fields = [[u'时间',
#                u'订单号',
#                u'用户名',
#                u'匹配的用户',
#                u'售卖数量',
#                u'冻结数量',
#                u'单价',
#                u'总价',
#                u'类型',
#                u'状态']]
#
#     data = [[timestamp_to_str(y['created_timestamp']),
#              y['number'],
#              y['user']['uid'],
#              y['match_user']['uid'],
#              format_currency(y['amount']),
#              format_currency(y['hold_amount']),
#              format_currency(y['price']),
#              format_currency(Decimal(y['amount']) * Decimal(y['price'])),
#              order_side[y['side']],
#              order_status[y['status']]]
#             for y in data['items']]
#
#     return excel.make_response_from_array(fields + data, "xls", file_name='交易订单')
