# -*- coding: utf-8 -*-
import time
import uuid
import urllib2

from flask import Blueprint, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

from app.views import Api, ApiError, AppError
from app.views.admin import api_permission

order = Blueprint('order', __name__)
api_permission['order'] = ['/admin/mall']

ORDER_STATUS_FLAG = [(4, u'待发货'),
                     (8, u'待收货'),
                     (16, u'已收货'),
                     (32, u'取消')]

CHOOSE_ALL = [('', u'全部')]


class ChangeStatusForm(Form):
    id = HiddenField('id')
    status = SelectField('status', choices=ORDER_STATUS_FLAG, coerce=int)
    express_company = StringField('express_company')
    express_code = StringField('express_code')


class OrderFilterForm(Form):
    uid = StringField('uid')
    number = StringField('number')
    mobile = StringField('mobile')
    created_begin_timestamp = StringField('created_begin_timestamp')
    created_end_timestamp = StringField('created_end_timestamp')


@order.route('/')
def index():
    filter_form = OrderFilterForm()
    return render_template('order/list.html', filter_form=filter_form)


@order.route('/ajax/list', methods=['POST'])
def ajax_list():
    params = request.get_json()
    if params['query'].get('created_begin_timestamp'):
        params['query']['created_begin_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_begin_timestamp'], u"%Y年%m月%d日")))
    if params['query'].get('created_end_timestamp'):
        params['query']['created_end_timestamp'] = int(time.mktime(
            time.strptime(params['query']['created_end_timestamp'] + u' 23:59:59', u"%Y年%m月%d日 %H:%M:%S")))
    data = Api.get('/admin/mall/order', params['query'])
    total_records = data['total_count']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['objects']
    }
    return jsonify(return_dict)


@order.route('/details/<string:id>')
def details(id):
    change_status_form = ChangeStatusForm()
    data = Api.get('/admin/mall/order/' + urllib2.quote(id))
    change_status_form.id.data = data['id']
    change_status_form.status.data = data['status']
    product = Api.get('/admin/mall/' + urllib2.quote(data['product_id']))
    return render_template('order/details.html', data=data, product=product, change_status_form=change_status_form)


@order.route('/ajax/change_status', methods=['POST'])
def ajax_change_status():
    change_status_form = ChangeStatusForm()
    if change_status_form.validate():
        data = Api.put('/admin/mall/order/' + urllib2.quote(change_status_form.id.data), {
            'express_company': change_status_form.express_company.data,
            'express_code': change_status_form.express_code.data,
            'status': change_status_form.status.data
        })
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, change_status_form.errors)
