# -*- coding: utf-8 -*-
import urllib2

from flask import Blueprint, jsonify
from flask import render_template
from flask import request
from wtforms import HiddenField, StringField, IntegerField, SelectField
from wtforms.validators import DataRequired

from app.views import Api, ApiError, AppError
from app.views.admin import api_permission
from flask_wtf import Form

reseller = Blueprint('reseller', __name__)

api_permission['reseller'] = ['/admin/reseller']

STATUS_FLAG = [(2, u'上架'),
               (4, u'下架')]

CHOOSE_ALL = [('', u'全部')]


class ResellerForm(Form):
    id = HiddenField('id')
    name = StringField('name', validators=[DataRequired(u'请填写商家名称')])
    code = StringField('code', validators=[DataRequired(u'请填写商家名称')])
    front_cover = StringField('front_cover', validators=[DataRequired(u'请上传商家图片')])
    detail_cover_0 = StringField('detail_cover_0')
    detail_cover_1 = StringField('detail_cover_1')
    detail_cover_2 = StringField('detail_cover_2')
    category = StringField('category', validators=[DataRequired(u'请填写商家类别')])
    description = StringField('decription', validators=[DataRequired(u'请填写商家描述')])
    sequence = IntegerField('sequence', validators=[DataRequired(u'请填写商家排序')])
    status = SelectField('status', choices=STATUS_FLAG, coerce=int)
    mobile = StringField('mobile', validators=[DataRequired(u'请填写商家电话')])
    address = StringField('address', validators=[DataRequired(u'请填写商家地址')])
    linkman_name = StringField('linkman_name', validators=[DataRequired(u'请填写联系人姓名')])
    linkman_mobile = StringField('linkman_mobile', validators=[DataRequired(u'请填写联系人手机')])
    user_uid = StringField('user_uid', validators=[DataRequired(u'请填写收款会员编号')])


class ResellerFilterForm(Form):
    name = StringField('name')
    status = SelectField('status', choices=CHOOSE_ALL + STATUS_FLAG)


@reseller.route('/')
def index():
    filter_form = ResellerFilterForm()
    return render_template('reseller/list.html', filter_form=filter_form)


@reseller.route('/ajax/list', methods=['POST'])
def ajax_list():
    params = request.get_json()
    data = Api.get('/admin/reseller', params['query'])
    total_records = data['total']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['items']
    }
    return jsonify(return_dict)


@reseller.route('/details', methods=['GET'])
@reseller.route('/details/<string:reseller_id>')
def details(reseller_id=None):
    reseller_form = ResellerForm()
    if reseller_id:
        data = Api.get('/admin/reseller/' + urllib2.quote(reseller_id))
        reseller_form.process(data=data)
        reseller_form.user_uid.data = data['user']['uid']
    return render_template('reseller/details.html', reseller_form=reseller_form)


@reseller.route('/ajax/product_modify', methods=['POST'])
def ajax_product_modify():
    product_form = ResellerForm()
    if product_form.validate():
        params = product_form.data
        if product_form.id.data:
            data = Api.put('/admin/reseller/' + urllib2.quote(product_form.id.data), params)
        else:
            data = Api.post('/admin/reseller', params)
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, product_form.errors)
