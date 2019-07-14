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

register = Blueprint('register', __name__)
api_permission['register'] = ['/admin/member']


class RegisterForm(Form):
    mobile = StringField('mobile', validators=[DataRequired(u'请填写手机号')])
    sponsor = StringField('sponsor', validators=[DataRequired(u'请填写推荐人')])
    password = StringField('password', validators=[DataRequired(u'请填写密码')])
    security_password = StringField('security_password', validators=[DataRequired(u'请填写密码')])


@register.route('/register/member')
def register_member():
    form = RegisterForm()
    return render_template('member/register.html', form=form)


@register.route('/ajax/register_member', methods=['POST'])
def ajax_register_member():
    form = RegisterForm()
    if form.validate():
        data = form.data
        return jsonify(Api.post('/admin/member', data))
    else:
        raise ApiError(AppError.INVALID_REQUEST, form.errors)
