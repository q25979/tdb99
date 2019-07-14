# -*- coding: utf-8 -*-
import decimal
from flask import Blueprint, jsonify, render_template, request
from flask_wtf import Form
from wtforms import FloatField, RadioField, StringField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange

from app.views import Api, AppError, ApiError
from app.views.admin import api_permission

setting = Blueprint('setting', __name__)
api_permission['setting'] = ['/admin/setting']


class SettingForm(Form):
    # 直推奖励
    recommend_reward_amount_1 = FloatField('recommend_reward_amount_1',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    recommend_reward_amount_2 = FloatField('recommend_reward_amount_2',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    recommend_reward_amount_3 = FloatField('recommend_reward_amount_3',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    recommend_reward_amount_4 = FloatField('recommend_reward_amount_4',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    recommend_reward_amount_5 = FloatField('recommend_reward_amount_5',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    recommend_reward_amount_6 = FloatField('recommend_reward_amount_6',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    recommend_reward_amount_7 = FloatField('recommend_reward_amount_7',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    recommend_reward_amount_8 = FloatField('recommend_reward_amount_8',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    recommend_reward_amount_9 = FloatField('recommend_reward_amount_9',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    recommend_reward_amount_10 = FloatField('recommend_reward_amount_10',
                                            validators=[NumberRange(min=0, message=u'请填写正确内容')])

    evaluation_reward_amount = IntegerField('evaluation_reward_amount',
                                            validators=[NumberRange(min=0, message=u'请填写正确内容')])

    buy_count = IntegerField('buy_count', validators=[NumberRange(min=0, message=u'请填写正确内容')])
    sell_count = IntegerField('sell_count', validators=[NumberRange(min=0, message=u'请填写正确内容')])
    sell_people = IntegerField('sell_people', validators=[NumberRange(min=0, message=u'请填写正确内容')])
    buy_people = IntegerField('buy_people', validators=[NumberRange(min=0, message=u'请填写正确内容')])
    lebo_change_price_cnt = IntegerField('lebo_change_price_cnt', validators=[NumberRange(min=0, message=u'请填写正确内容')])
    lebo_price_step = FloatField('lebo_price_step', validators=[NumberRange(min=0, message=u'请填写正确内容')])
    community_dividend_rate = FloatField('community_dividend_rate', validators=[NumberRange(min=0, message=u'请填写正确内容')])
    exchange_amount_max = IntegerField('exchange_amount_max', validators=[NumberRange(min=0, message=u'请填写正确内容')])

    transaction_time_begin_1 = StringField('transaction_time_begin_1', validators=[DataRequired()])
    transaction_time_begin_2 = StringField('transaction_time_begin_2', validators=[DataRequired()])

    transaction_time_end_1 = StringField('transaction_time_end_1', validators=[DataRequired()])
    transaction_time_end_2 = StringField('transaction_time_end_2', validators=[DataRequired()])

    # 允许交易数量
    transaction_allow_amount = IntegerField('transaction_allow_amount',
                                            validators=[NumberRange(min=0, message=u'请填写正确内容')])
    # 释放手续费率
    buy_sell_rate = FloatField('buy_sell_rate',
                               validators=[NumberRange(min=0, message=u'请填写正确内容')])
    # 普通会员加速释放
    transaction_free_amount = IntegerField('transaction_free_amount',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    # 社区节点加速释放
    community_free_amount = IntegerField('transaction_free_amount',
                                         validators=[NumberRange(min=0, message=u'请填写正确内容')])
    # 社区节点转账手续费
    community_transaction_fee_rate = FloatField('community_transaction_fee_rate',
                                                validators=[NumberRange(min=0, message=u'请填写正确内容')])
    # 节点条件
    community_transaction_day_cnt = IntegerField('community_transaction_day_cnt',
                                                 validators=[NumberRange(min=0, message=u'请填写正确内容')])
    # 总资产钱包累计达到
    community_total_balance_1 = IntegerField('community_total_balance_1',
                                             validators=[NumberRange(min=0, message=u'请填写正确内容')])
    community_total_balance_2 = IntegerField('community_total_balance_2',
                                             validators=[NumberRange(min=0, message=u'请填写正确内容')])
    community_total_balance_3 = IntegerField('community_total_balance_3',
                                             validators=[NumberRange(min=0, message=u'请填写正确内容')])
    # 合格用户
    community_sponsor_cnt_1 = IntegerField('community_sponsor_cnt_1',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    community_sponsor_cnt_2 = IntegerField('community_sponsor_cnt_2',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])
    community_sponsor_cnt_3 = IntegerField('community_sponsor_cnt_3',
                                           validators=[NumberRange(min=0, message=u'请填写正确内容')])

    # 关于我们
    contact_us = StringField('contact_us')

    # # 节点算力
    # node_rate = StringField('node_rate', validators=[DataRequired(u'请填写内容')])
    # max_investment = StringField('max_investment', validators=[DataRequired(u'请填写内容')])

    # # 订单
    # order_sell_rate = StringField('order_sell_rate', validators=[DataRequired(u'请填写内容')])
    # order_amount_min = StringField('order_amount_min', validators=[DataRequired(u'请填写内容')])
    # order_amount_max = StringField('order_amount_max', validators=[DataRequired(u'请填写内容')])
    # order_fee_rate = StringField('order_fee_rate', validators=[DataRequired(u'请填写内容')])
    # order_price_min = StringField('order_price_min', validators=[DataRequired(u'请填写内容')])
    # order_price_max = StringField('order_price_max', validators=[DataRequired(u'请填写内容')])
    # order_cancel_time = StringField('order_cancel_time', validators=[DataRequired(u'请填写内容')])


class OrderSettingForm(Form):
    order_sell_rate = StringField('order_sell_rate', validators=[DataRequired(u'请填写内容')])
    order_amount_min = StringField('order_amount_min', validators=[DataRequired(u'请填写内容')])
    order_amount_max = StringField('order_amount_max', validators=[DataRequired(u'请填写内容')])
    order_fee_rate = StringField('order_fee_rate', validators=[DataRequired(u'请填写内容')])
    order_price_min = StringField('order_price_min', validators=[DataRequired(u'请填写内容')])
    order_price_max = StringField('order_price_max', validators=[DataRequired(u'请填写内容')])
    order_cancel_time = StringField('order_cancel_time', validators=[DataRequired(u'请填写内容')])


class RegisterForm(Form):
    mobile = StringField('mobile', validators=[DataRequired(u'请填写手机号')])
    sponsor = StringField('sponsor', validators=[DataRequired(u'请填写推荐人')])
    placement = StringField('placement', validators=[DataRequired(u'请填写安置上线')])
    position = SelectField('position', choices=[(0, u'左'), (1, u'右')], coerce=int)
    # rate_level = SelectField('rate_level', choices=RATE_LEVEL_FLAG)
    password = StringField('password', validators=[DataRequired(u'请填写密码')])


@setting.route('/', methods=['GET', 'POST'])
def index():
    setting_form = SettingForm()
    if request.method == 'POST':
        print setting_form.data
        if setting_form.validate():
            params = setting_form.data

            recommend_reward_amount = []
            for i in range(10):
                if params['recommend_reward_amount_' + str(i + 1)]:
                    recommend_reward_amount.append(str(params['recommend_reward_amount_' + str(i + 1)]))
                params.pop('recommend_reward_amount_' + str(i + 1))
            params['recommend_reward_amount'] = recommend_reward_amount

            transaction_time_begin = []
            for i in range(2):
                if params['transaction_time_begin_' + str(i + 1)]:
                    transaction_time_begin.append(str(params['transaction_time_begin_' + str(i + 1)]))
                params.pop('transaction_time_begin_' + str(i + 1))
            params['transaction_time_begin'] = transaction_time_begin

            transaction_time_end = []
            for i in range(2):
                if params['transaction_time_end_' + str(i + 1)]:
                    transaction_time_end.append(str(params['transaction_time_end_' + str(i + 1)]))
                params.pop('transaction_time_end_' + str(i + 1))
            params['transaction_time_end'] = transaction_time_end

            community_total_balance = []
            for i in range(3):
                if params['community_total_balance_' + str(i + 1)]:
                    community_total_balance.append(int(params['community_total_balance_' + str(i + 1)]))
                params.pop('community_total_balance_' + str(i + 1))
            params['community_total_balance'] = community_total_balance

            community_sponsor_cnt = []
            for i in range(3):
                if params['community_sponsor_cnt_' + str(i + 1)]:
                    community_sponsor_cnt.append(int(params['community_sponsor_cnt_' + str(i + 1)]))
                params.pop('community_sponsor_cnt_' + str(i + 1))
            params['community_sponsor_cnt'] = community_sponsor_cnt

            params['lebo_price_step'] = str(params['lebo_price_step'])
            params['community_transaction_fee_rate'] = str(params['community_transaction_fee_rate'])
            params['community_dividend_rate'] = str(params['community_dividend_rate'])

            print params
            return jsonify(Api.put('/admin/setting/general_option', params))
        else:
            raise AppError.invalid_request(setting_form.errors)
    else:
        data = Api.get('/admin/setting/general_option')['value']

        for i in range(10):
            data['recommend_reward_amount_' + str(i + 1)] = \
                data['recommend_reward_amount'][i]

        for i in range(2):
            data['transaction_time_begin_' + str(i + 1)] = data['transaction_time_begin'][i]

        for i in range(2):
            data['transaction_time_end_' + str(i + 1)] = data['transaction_time_end'][i]

        for i in range(3):
            data['community_total_balance_' + str(i + 1)] = data['community_total_balance'][i]
        for i in range(3):
            data['community_sponsor_cnt_' + str(i + 1)] = data['community_sponsor_cnt'][i]

        data['lebo_price_step'] = str(data['lebo_price_step'] if data['lebo_price_step'] else 0)
        data['community_transaction_fee_rate'] = str(
            data['community_transaction_fee_rate'] if data['community_transaction_fee_rate'] else 0)
        data['community_dividend_rate'] = str(
            data['community_dividend_rate'] if data['evaluation_reward_amount'] else 0)

        setting_form.process(data=data)
        return render_template('setting/sys.html', setting_form=setting_form)


# @setting.route('/order', methods=['GET', 'POST'])
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
