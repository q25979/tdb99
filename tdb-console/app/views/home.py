# -*- coding: utf-8 -*-
import json
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

from app.views import Api, ApiError, AppError

home = Blueprint('home', __name__)


class LoginForm(Form):
    uid = StringField('uid', validators=[DataRequired(u'请输入用户名'),
                                         Regexp('^[A-Za-z0-9]+$', message=u'用户只能有数字、字母组成')])
    password = PasswordField('Password', validators=[DataRequired(u'请输入密码'),
                                                     Regexp('^[A-Za-z0-9]+$', message=u'密码只能有数字、字母组成')])
    captcha = StringField('Captcha', validators=[DataRequired(u'请输入验证码'),
                                                 Regexp('^[A-Za-z0-9]+$', message=u'验证码只能有数字、字母组成')])
    uuid = HiddenField('uuid', validators=[Length(min=36)])


class ChangePasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired(u'请输入原密码')])
    new_password = PasswordField('Password', validators=[DataRequired(u'请输入新密码')])
    confirm_new_password = PasswordField('Password', validators=[
        DataRequired(u'请输入确认新密码'), EqualTo('new_password', u'确认新密码错误')])


@home.route('/', methods=['GET'])
def index():
    if not session.get('token') or not session.get('role'):
        return redirect(url_for('home.login'))
    else:
        return render_template('layout/main.html', redirection=True)


@home.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if request.method == 'POST' and login_form.validate():
        try:
            data = Api.post('/admin/user/login', {
                'uid': login_form.uid.data,
                'password': login_form.password.data,
                'uuid': login_form.uuid.data,
                'pin_code': login_form.captcha.data
            })
            session['uid'] = login_form.uid.data
            session['token'] = data['token']
            session['role'] = data['role']
            session['permission'] = data['permission']

            return redirect(url_for('home.index'))
        except ApiError as e:
            if 'id' in e.message or 'password' in e.message:
                error = u'用户名或密码错误'
            elif 'uuid' in e.message or 'pin_code' in e.message:
                error = u'验证码错误'
            elif 'locked' in e.message:
                error = u'账号已被锁定'
            elif 'uid' in e.message:

                error = u'账号不存在'
            else:
                error = u'登录错误'
    login_form.captcha.data = None
    return render_template('login.html', form=login_form, login_error=error)


@home.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('home.login'))


@home.route('/captcha', methods=['GET'])
def captcha():
    if request.args.get('uuid', None):
        pin_code_uuid = request.args.get('uuid')
    else:
        pin_code_uuid = str(uuid.uuid4())
    data = Api.get('/captcha_pin_code', {
        'uuid': pin_code_uuid
    }, response_type='binary')
    session['login_captcha_uuid'] = pin_code_uuid
    response = make_response(data)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


# 修改密码
@home.route('/change_password', methods=['GET', 'POST'])
def change_password():
    change_password_form = ChangePasswordForm()
    if request.method == 'POST':
        if change_password_form.validate():
            params = change_password_form.data
            params.pop('confirm_new_password')
            return jsonify(Api.post('/admin/user/reset_password', params))
        else:
            raise AppError.invalid_request(change_password_form.errors)
    else:
        return render_template('change_password.html', change_password_form=change_password_form)
