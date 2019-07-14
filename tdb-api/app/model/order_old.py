# -*- coding: utf-8 -*-
import datetime
import logging
import time
import json
import decimal
from app.model import AutoIncrementBase, db, generate_timestamp_id
from app.model.user import User, g_user_transaction_level
from app.model.payment import Payment
from app.model.setting import Setting
from app.model.currency import Currency
from app.model.assets import Assets, g_assets_record_type
from app.type.typedef_const import TypedefConst

g_order_old_status = TypedefConst()

g_order_old_status.PENDING = 1  # 挂单中
g_order_old_status.MATCH = 2  # 匹配中
g_order_old_status.PAID = 4  # 已付款
g_order_old_status.CONFIRMED = 8  # 已确认
g_order_old_status.CANCELLED = 16  # 已取消


class OrderOld(AutoIncrementBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)  # 卖方用户
    match_user_id = db.Column(db.String(36), db.ForeignKey('user.id'))  # 买方用户
    # side = db.Column(db.SmallInteger, nullable=False)  # 1 买单  2 卖单
    number = db.Column(db.String(16), default=generate_timestamp_id, unique=True, nullable=False)
    # price = db.Column(db.Numeric(24, 8), nullable=False)  # 单价
    amount = db.Column(db.Numeric(24, 8), nullable=False)  # 售卖数量
    hold_amount = db.Column(db.Numeric(24, 8), nullable=False)  # 冻结数量
    fee = db.Column(db.Numeric(24, 8), nullable=False)  # 手续费
    status = db.Column(db.SmallInteger, default=g_order_old_status.PENDING, nullable=False)  # 订单状态参见 g_order_status

    payment_amount = db.Column(db.Numeric(24, 8), default=0, nullable=False)  # 对应支付方式，支付数量

    match_at = db.Column(db.DateTime)

    proof_img = db.Column(db.Text, default='[]')  # 转账凭证

    current_price = db.Column(db.Numeric(24, 8), nullable=False)  # 冻结数量
    payment_id = db.Column(db.String(36), db.ForeignKey('payment.id'))  # 卖方收款方式

    details = db.Column(db.String(255), default='', nullable=True)  # 备注

    user = db.relationship(User, foreign_keys=[user_id])
    match_user = db.relationship(User, foreign_keys=[match_user_id])
    payment = db.relationship(Payment, foreign_keys=[payment_id])
