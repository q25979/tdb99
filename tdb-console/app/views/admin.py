# -*- coding: utf-8 -*-
import uuid
import urllib2

from flask import Blueprint, render_template, request, session, jsonify
from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

from app.views import Api, ApiError, AppError

admin = Blueprint('admin', __name__)

ROLE_FLAG = [(1, u'超级管理员'),
             (2, u'系统管理员')]

api_permission = {}

PERMISSION_FLAG = [('member', u'会员管理'),
                   ('wallet', u'财务管理'),
                   ('news', u'新闻管理'),
                   ('p2p_order', u'交易订单'),
                   ('register', u'会员注册'),
                   ('setting', u'系统设置')]


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddUserForm(Form):
    id = HiddenField('id')
    uid = StringField('uid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('password', validators=[
        DataRequired(u'请再次输入密码'), EqualTo('password', u'两次输入的密码不正确')])
    # role = SelectField('role', choices=ROLE_FLAG, coerce=int)
    permission = MultiCheckboxField('permission', choices=PERMISSION_FLAG, coerce=str)


class ChangePasswordForm(Form):
    id = HiddenField('id')
    password = PasswordField('password', validators=[DataRequired()])
    confirm_new_password = PasswordField('password', validators=[
        DataRequired(u'请再次输入新密码'), EqualTo('password', u'两次输入的密码不正确')])


class ChangeRoleForm(Form):
    user_id = HiddenField('user_id')
    role = SelectField('role', choices=ROLE_FLAG, coerce=int)


@admin.route('/')
def index():
    change_password_form = ChangePasswordForm()
    change_role_form = ChangeRoleForm()
    return render_template('admin/list.html', change_password_form=change_password_form,
                           change_role_form=change_role_form)


@admin.route('/edit_user')
@admin.route('/edit_user/<string:user_id>')
def add_user(user_id=None):
    add_user_form = AddUserForm()
    if user_id:
        user = Api.get('/admin/user/' + urllib2.quote(user_id))
        add_user_form.process(data=user)
        permission_list = []
        for key, value in user['permission'].items():
            permission_list.append(key)
        add_user_form.permission.data = permission_list

    return render_template('admin/add_user.html', add_user_form=add_user_form)


@admin.route('/ajax/list', methods=['POST'])
def ajax_list():
    params = request.get_json()
    data = Api.get('/admin/user', params['query'])
    total_records = data['total_count']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['objects']
    }
    return jsonify(return_dict)


@admin.route('/ajax/lock', methods=['POST'])
def ajax_lock():
    params = request.get_json()
    user_id = params.pop('id')
    data = Api.put('/admin/user/' + urllib2.quote(user_id), params)
    return jsonify(data)


@admin.route('/ajax/change_password', methods=['POST'])
def ajax_change_password():
    change_password_form = ChangePasswordForm()
    if change_password_form.validate():
        data = Api.put('/admin/user/' + urllib2.quote(change_password_form.id.data), {
            'password': change_password_form.password.data
        })
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, change_password_form.errors)


@admin.route('/ajax/change_role', methods=['POST'])
def ajax_change_role():
    change_role_form = ChangeRoleForm()
    if change_role_form.validate():
        data = Api.put('/admin/user/' + urllib2.quote(change_role_form.user_id.data), {
            'role': change_role_form.role.data
        })
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, change_role_form.errors)


@admin.route('/ajax/add_user', methods=['POST'])
def ajax_add_user():
    add_user_form = AddUserForm()
    if add_user_form.data['id']:
        add_user_form.password.validators = []
        add_user_form.confirm_password.validators = []
    if add_user_form.validate():
        permission = {}
        for item in add_user_form.permission.data:
            permission[item] = api_permission[item]
        if add_user_form.data['id']:
            data = Api.put('/admin/user/' + urllib2.quote(add_user_form.id.data), {
                'uid': add_user_form.uid.data,
                'password': add_user_form.password.data,
                'permission': permission
            })
        else:
            data = Api.post('/admin/user', {
                'uid': add_user_form.uid.data,
                'password': add_user_form.password.data,
                'permission': permission
            })
        return jsonify(data)
    else:
        raise ApiError(AppError.INVALID_REQUEST, add_user_form.errors)
