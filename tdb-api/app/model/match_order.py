# -*- coding: utf-8 -*-
import datetime
import json
import decimal
from app.model import AutoIncrementBase, db, generate_timestamp_id
from app.model.user import User
from app.model.payment import Payment
from app.type.typedef_const import TypedefConst


class MatchOrder(AutoIncrementBase):
    sell_user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)  # 卖方用户
    buy_user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)  # 买方用户

    sell_order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)  # 卖方订单
    buy_order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)  # 买方订单

    sell_number = db.Column(db.String(16), unique=True, nullable=False)
    buy_number = db.Column(db.String(16), unique=True, nullable=False)

    payment_amount = db.Column(db.Numeric(24, 8), default=0, nullable=False)  # 对应支付方式，支付金额 人民币
    payment_amount_usdt = db.Column(db.Numeric(24, 8), default=0, nullable=False)  # 对应支付方式，支付数量 USDT

    proof_img = db.Column(db.Text, default='[]')  # 转账凭证

    current_price = db.Column(db.Numeric(24, 8), nullable=False)  # 当前价格
    payment_id = db.Column(db.String(36), db.ForeignKey('payment.id'))  # 卖方收款方式

    sell_user = db.relationship(User, foreign_keys=[sell_user_id])
    buy_user = db.relationship(User, foreign_keys=[buy_user_id])
    sell_order = db.relationship('Order', foreign_keys=[sell_order_id])
    buy_order = db.relationship('Order', foreign_keys=[buy_order_id])
    payment = db.relationship(Payment, foreign_keys=[payment_id])


g_match_order_task_status = TypedefConst()

g_match_order_task_status.UNPROCESSED = 0  # 未处理
g_match_order_task_status.PROCESSED = 1  # 处理成功


class MatchOrderTask(AutoIncrementBase):

    # 状态参见 g_match_order_task_status
    status = db.Column(db.SmallInteger, default=g_match_order_task_status.UNPROCESSED)

    order_cnt = db.Column(db.Integer, nullable=False)  # 需要匹配的单数

