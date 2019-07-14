# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, render_template, request
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

from app.views import Api, AppError
from app.views.admin import api_permission

setting_order = Blueprint('setting_order', __name__)
api_permission['setting_order'] = ['/admin/setting']


class OrderSettingForm(Form):
    order_sell_rate = StringField('order_sell_rate', validators=[DataRequired(u'请填写内容')])
    order_amount_min = StringField('order_amount_min', validators=[DataRequired(u'请填写内容')])
    order_amount_max = StringField('order_amount_max', validators=[DataRequired(u'请填写内容')])
    order_fee_rate = StringField('order_fee_rate', validators=[DataRequired(u'请填写内容')])
    order_price_min = StringField('order_price_min', validators=[DataRequired(u'请填写内容')])
    order_price_max = StringField('order_price_max', validators=[DataRequired(u'请填写内容')])
    order_cancel_time = StringField('order_cancel_time', validators=[DataRequired(u'请填写内容')])
    order_auto_cancel_time = StringField('order_auto_cancel_time', validators=[DataRequired(u'请填写内容')])


@setting_order.route('/order', methods=['GET', 'POST'])
def order():
    setting_form = OrderSettingForm()
    if request.method == 'POST':
        print setting_form.data
        if setting_form.validate():
            params = setting_form.data

            params['order_sell_rate'] = str(params['order_sell_rate'] if params['order_sell_rate'] else 0)
            params['order_amount_min'] = str(params['order_amount_min'] if params['order_amount_min'] else 0)
            params['order_amount_max'] = str(params['order_amount_max'] if params['order_amount_max'] else 0)
            params['order_fee_rate'] = str(params['order_fee_rate'] if params['order_fee_rate'] else 0)
            params['order_price_min'] = str(params['order_price_min'] if params['order_price_min'] else 0)
            params['order_price_max'] = str(params['order_price_max'] if params['order_price_max'] else 0)

            print params
            return jsonify(Api.put('/admin/setting/sys', params))
        else:
            raise AppError.invalid_request(setting_form.errors)
    else:
        data = Api.get('/admin/setting/sys')['value']

        setting_form.process(data=data)
        return render_template('setting/order.html', setting_form=setting_form)
