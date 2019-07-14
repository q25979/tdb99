# -*- coding: utf-8 -*-
import urllib2

from flask import Blueprint, jsonify
from flask import render_template
from flask import request
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired

from app.views import Api, ApiError, AppError
from app.views.admin import api_permission

message = Blueprint('message', __name__)
api_permission['message'] = ['/admin/message', '/admin/member']

# 1 管理员端未读 2 管理员已读并忽略  4 管理员已读并回复  8 会员端已读回复

STATUS_FLAG = [(1, u'未读 '),
               (2, u'已读'),
               (4, u'已回复'),
               (8, u'会员已读回复')]


class FilterForm(Form):
    title = StringField('title')
    status = SelectField('status', choices=[(0, u'全部')] + STATUS_FLAG, coerce=int)
    uid = StringField('uid')


class MessageForm(Form):
    id = HiddenField('id')
    answer = TextAreaField('answer', validators=[DataRequired(message='请填写回复内容')])


class RegisterForm(Form):
    uid = StringField('uid', validators=[DataRequired(u'请填写编号')])
    mobile = StringField('mobile', validators=[DataRequired(u'请填写手机号')])
    sponsor = StringField('sponsor', validators=[DataRequired(u'请填写推荐人')])
    placement = StringField('placement', validators=[DataRequired(u'请填写安置上线')])
    position = SelectField('position', choices=[(0, u'左'), (1, u'右')], coerce=int)
    # rate_level = SelectField('rate_level', choices=RATE_LEVEL_FLAG)
    password = StringField('password', validators=[DataRequired(u'请填写密码')])
    security_password = StringField('security_password', validators=[DataRequired(u'请填写密码')])


@message.route('/')
def index():
    filter_form = FilterForm()
    return render_template('message/index.html',
                           filter_form=filter_form,
                           STATUS_FLAG=dict(STATUS_FLAG))


@message.route('/ajax/list', methods=['POST'])
def ajax_list():
    params = request.get_json()
    data = Api.get('/admin/message', params['query'])
    total_records = data['total']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['items']
    }
    return jsonify(return_dict)


@message.route('/details/<string:message_id>')
def details(message_id=None):
    form = MessageForm()
    message_detail = Api.get('/admin/message/detail/' + urllib2.quote(message_id))
    form.process(data=message_detail)
    return render_template('message/detail.html',
                           message_detail=message_detail,
                           form=form)


@message.route('/ajax/save', methods=['POST'])
def ajax_save():
    form = MessageForm()
    if form.validate():
        data = form.data
        message_id = data.pop('id')
        result = Api.put('/admin/message/detail/' + urllib2.quote(message_id), data)
        return jsonify(result)
    else:
        raise ApiError(AppError.INVALID_REQUEST, form.errors)


# @message.route('/register/member')
def register_member():
    form = RegisterForm()
    return render_template('member/register.html', form=form)


# @message.route('/ajax/register_member', methods=['POST'])
def ajax_register_member():
    form = RegisterForm()
    if form.validate():
        data = form.data
        return jsonify(Api.post('/admin/member', data))
    else:
        raise ApiError(AppError.INVALID_REQUEST, form.errors)
