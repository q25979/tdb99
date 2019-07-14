# -*- coding: utf-8 -*-
import urllib2
import flask_excel as excel

import time
from flask import Blueprint, render_template, request, jsonify, current_app
from flask import session
from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField, FloatField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo

from app.template_helpers.utils import timestamp_to_str, format_currency
from app.views import Api, ApiError, AppError

# LEVEL_FLAG = [(0, u'无矿机'),
#               (1, u'铁矿机'),
#               (2, u'铜矿机'),
#               (3, u'银矿机'),
#               (4, u'金矿机'),
#               (5, u'钻矿机')]
from app.views.admin import api_permission

WALLET_TYPE_FLAG = [(1, u'总资产钱包'),
                    (2, u'社区钱包'),
                    (4, u'交易钱包')]
STATE_TYPE_FLAG = [('0', u'未完善资料'),
                   ('1', u'未通过测评'),
                   ('2', u'通过测评')]
MEMBER_LEVEL = [('0', u'普通会员'),
                ('1', u'节点会员')]

member = Blueprint('member', __name__)

api_permission['member'] = ['/admin/member', '/admin/wallet', '/admin/team']


class MemberFilterForm(Form):
    created_begin_timestamp = StringField('created_begin_timestamp')
    created_end_timestamp = StringField('created_end_timestamp')
    mobile = StringField('mobile')
    name = StringField('name')
    sponsor = StringField('sponsor')
    state = SelectField('state', choices=[('', u'全部')] + STATE_TYPE_FLAG, coerce=str)
    locked = SelectField('locked', choices=[('', u'全部'), ('1', u'锁定'), ('0', u'正常')])
    is_community_node = SelectField('is_community_node', choices=[('', u'全部')] + MEMBER_LEVEL, coerce=str)


class ChangePasswordForm(Form):
    password_id = HiddenField('password_id')
    password = PasswordField('password', validators=[DataRequired(u'请输入新的登录密码')])
    confirm_new_password = PasswordField('password', validators=[
        DataRequired(u'请再次输入新密码'), EqualTo('password', u'两次输入的密码不正确')])


class ChangeSecurityForm(Form):
    security_id = HiddenField('security_id')
    security_password = PasswordField('security_password', validators=[DataRequired(u'请输入新的安全密码')])
    confirm_new_password = PasswordField('security_password', validators=[
        DataRequired(u'请再次输入新密码'), EqualTo('security_password', u'两次输入的密码不正确')])


class ChangeProfileForm(Form):
    id = HiddenField('id')
    mobile = StringField('mobile')
    name = StringField('name')
    wechat = StringField('wechat')


class DepositForm(Form):
    id = HiddenField('id')
    assets_type = SelectField('assets_type', choices=WALLET_TYPE_FLAG, coerce=int)
    amount = FloatField('amount', validators=[DataRequired(u'请输入充值数额')])


class PaymentForm(Form):
    user_id = HiddenField('user_id')
    type = IntegerField('type')
    name = StringField('name')
    bank = StringField('bank')
    card_number = StringField('card_number')
    wechat = StringField('wechat')
    wechat_image = StringField('wechat_image')
    alipay = StringField('alipay')
    alipay_image = StringField('alipay_image')
    address = StringField('address')
    remark = StringField('remark')


@member.route('/')
def index():
    filter_form = MemberFilterForm()
    return render_template('member/list.html',
                           STATE_TYPE_FLAG=dict(STATE_TYPE_FLAG),
                           MEMBER_LEVEL=dict(MEMBER_LEVEL),
                           filter_form=filter_form)


@member.route('/details/<string:member_id>')
def details(member_id):
    deposit_form = DepositForm()
    change_password_form = ChangePasswordForm()
    change_security_form = ChangeSecurityForm()
    change_profile_form = ChangeProfileForm()
    payment_form = PaymentForm()
    data = Api.get('/admin/member/detail/' + urllib2.quote(member_id))
    change_security_form.security_id.data = data['id']
    change_password_form.password_id.data = data['id']
    change_profile_form.id.data = data['id']
    deposit_form.id.data = data['assets']['id']
    payment_form.user_id.data = data['id']
    change_profile_form.mobile.data = data['mobile']
    change_profile_form.name.data = data['name']
    change_profile_form.wechat.data = data['wechat']
    payment_list = Api.get('/admin/payment/list', {'user_id': data['id']})['objects']

    payment_dic = {}
    payment_flag = ['bank_payment', 'wechat_payment', 'alipay_payment', 'usdt_payment']
    for item in payment_list:
        payment_dic[payment_flag[item['type']]] = item

    return render_template('member/details.html', data=data,
                           payment_dic=payment_dic, payment_form=payment_form,
                           change_password_form=change_password_form, change_profile_form=change_profile_form,
                           change_security_form=change_security_form, deposit_form=deposit_form)


@member.route('/ajax/list', methods=['POST'])
def ajax_list():
    params = request.get_json()
    if params['query'].get('created_begin_timestamp'):
        params['query']['created_begin_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_begin_timestamp'], u"%Y年%m月%d日")))
    if params['query'].get('created_end_timestamp'):
        params['query']['created_end_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_end_timestamp'] + u' 23:59:59', u"%Y年%m月%d日 %H:%M:%S")))
    data = Api.get('/admin/member', params['query'])
    total_records = data['total_count']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['objects']
    }
    return jsonify(return_dict)


@member.route('/ajax/lock', methods=['POST'])
def ajax_lock():
    params = request.get_json()
    user_id = params.pop('id')
    data = Api.put('/admin/member/detail/' + urllib2.quote(user_id), params)
    return jsonify(data)


@member.route('/ajax/delete/payment', methods=['POST'])
def ajax_delete_payment():
    params = request.get_json()
    user_id = params.pop('id')
    data = Api.delete('/admin/payment/details/' + urllib2.quote(user_id))
    return jsonify(data)


@member.route('/ajax/change_password', methods=['POST'])
def ajax_change_password():
    change_password_form = ChangePasswordForm()
    if change_password_form.validate():
        data = Api.put('/admin/member/detail/' + urllib2.quote(change_password_form.password_id.data), {
            'password': change_password_form.password.data
        })
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, change_password_form.errors)


@member.route('/ajax/add_payment', methods=['POST'])
def ajax_add_payment():
    payment_form = PaymentForm()
    if payment_form.validate():
        data = Api.post('/admin/payment/list', payment_form.data)
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, payment_form.errors)


@member.route('/ajax/change_security', methods=['POST'])
def ajax_change_security():
    change_security_form = ChangeSecurityForm()
    if change_security_form.validate():
        data = Api.put('/admin/member/detail/' + urllib2.quote(change_security_form.security_id.data), {
            'security_password': change_security_form.security_password.data
        })
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, change_security_form.errors)


@member.route('/ajax/change_profile', methods=['POST'])
def ajax_change_profile():
    change_profile_form = ChangeProfileForm()
    if change_profile_form.validate():
        data = Api.put('/admin/member/detail/' + urllib2.quote(change_profile_form.id.data), change_profile_form.data)
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, change_profile_form.errors)


@member.route('/ajax/deposit', methods=['POST'])
def ajax_deposit():
    deposit_form = DepositForm()
    if deposit_form.validate():
        data = Api.post('/admin/assets/recharge', deposit_form.data)
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, deposit_form.errors)


@member.route('/sponsor')
def sponsor():
    return render_template('member/sponsor_tree.html')


@member.route('/ajax/sponsor/downline', methods=['POST'])
def ajax_sponsor_downline():
    params = request.json
    res = Api.get('/admin/team/sponsor_downline', {'unique_id': params['unique_id']})
    children = []
    for item in res['objects']:
        obj = {'id': item['mobile'], 'text': u'{} {}'.format(item['name'], item['mobile']), 'children': True,
               'icon': 'fa fa-user'}
        children.append(obj)
    result = {
        'id': params['unique_id'],
        'text': params['text'],
        'icon': 'fa fa-user',
        'children': children
    }
    return jsonify(result)


@member.route('/binary', methods=['GET'])
def binary():
    return render_template('member/binary_tree.html')


@member.route('/ajax/placement/downline', methods=['POST'])
def ajax_placement_downline():
    params = request.json
    res = Api.get('/admin/team/placement_downline', params)
    return jsonify(res)


@member.route('/data/download')
def data_download():
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
    member_data = Api.get('/admin/member', params)
    lock_status = {1: u'锁定', 0: u'未锁定'}
    fields = [[u'昵称',
               u'手机号',
               u'编号',
               u'推荐人',
               u'安置上线',
               u'零钱包',
               u'冷钱包',
               u'静态收益',
               u'动态收益',
               u'节点收益',
               u'总收益',
               u'银行',
               u'支行',
               u'持卡人',
               u'微信',
               u'支付宝',
               u'状态',
               u'注册时间']]

    data = [[y['nickname'],
             y['mobile'],
             y['uid'],
             y['sponsor']['uid'],
             y['placement']['uid'],
             format_currency(y['static_coin']),
             format_currency(y['frozen_coin']),
             format_currency(y['static_profit']),
             format_currency(y['dynamic_profit']),
             format_currency(y['node_profit']),
             format_currency(y['profit']),
             y['bank'],
             y['branch'],
             y['card_holder'],
             y['wechat'],
             y['alipay'],
             lock_status[y['locked']],
             timestamp_to_str(y['created_timestamp'])]
            for y in member_data['items']]

    return excel.make_response_from_array(fields + data, "xls", file_name='会员')
