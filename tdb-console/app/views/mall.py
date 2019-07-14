# -*- coding: utf-8 -*-
import uuid
import urllib2

from flask import Blueprint, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

from app.views import Api, ApiError, AppError
from app.views.admin import api_permission

mall = Blueprint('mall', __name__)

api_permission['mall'] = ['/admin/mall']

PRODUCT_STATUS_FLAG = [(1, u'待发布'),
                       (2, u'上架'),
                       (4, u'下架'),
                       (8, u'回收站')]

CHOOSE_ALL = [('', u'全部')]


class ProductForm(Form):
    id = HiddenField('id')
    front_cover = StringField('front_cover', validators=[DataRequired(u'请上传商品图')])
    detail_cover_0 = StringField('detail_cover_0')
    detail_cover_1 = StringField('detail_cover_1')
    detail_cover_2 = StringField('detail_cover_2')
    category = StringField('category', validators=[DataRequired(u'请填写商品类别')])
    description = StringField('decription', validators=[DataRequired(u'请填写商品描述')])
    name = StringField('name', validators=[DataRequired(u'请填写商品名称')])
    sequence = IntegerField('sequence', validators=[DataRequired(u'请填写商品排序')])
    status = SelectField('status', choices=PRODUCT_STATUS_FLAG, coerce=int)
    price = FloatField('price', validators=[DataRequired(u'请填写商品价格')])


class ProductFilterForm(Form):
    name = StringField('name')
    status = SelectField('status', choices=CHOOSE_ALL + PRODUCT_STATUS_FLAG)


@mall.route('/')
def index():
    filter_form = ProductFilterForm()
    return render_template('mall/list.html', filter_form=filter_form)


@mall.route('/ajax/list', methods=['POST'])
def ajax_list():
    params = request.get_json()
    data = Api.get('/admin/mall', params['query'])
    total_records = data['total']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['items']
    }
    return jsonify(return_dict)


@mall.route('/details', methods=['GET'])
@mall.route('/details/<string:product_id>')
def details(product_id=None):
    product_form = ProductForm()
    if product_id:
        data = Api.get('/admin/mall/' + urllib2.quote(product_id))
        product_form.process(data=data)
    return render_template('mall/details.html', product_form=product_form)


@mall.route('/ajax/product_modify', methods=['POST'])
def ajax_product_modify():
    product_form = ProductForm()
    if product_form.validate():
        params = {
            'name': product_form.name.data,
            'front_cover': product_form.front_cover.data,
            'category': product_form.category.data,
            'detail_cover_0': product_form.detail_cover_0.data,
            'detail_cover_1': product_form.detail_cover_1.data,
            'detail_cover_2': product_form.detail_cover_2.data,
            'description': product_form.description.data,
            'price': product_form.price.data,
            'sequence': product_form.sequence.data,
            'status': product_form.status.data
        }
        if product_form.id.data:
            data = Api.put('/admin/mall/' + urllib2.quote(product_form.id.data), params)
        else:
            data = Api.post('/admin/mall/product_add', params)
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, product_form.errors)
