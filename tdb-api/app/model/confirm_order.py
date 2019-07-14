# -*- coding: utf-8 -*-
import datetime
import json
import decimal
from app.model import AutoIncrementBase, db, generate_timestamp_id
from app.model.user import User
from app.type.typedef_const import TypedefConst

g_confirm_order_status = TypedefConst()

g_confirm_order_status.UNPROCESSED = 0  # 未处理
g_confirm_order_status.PROCESSED = 1  # 处理成功


class ConfirmOrder(AutoIncrementBase):
    sell_user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)  # 卖方用户
    buy_user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)  # 买方用户

    amount = db.Column(db.Numeric(24, 8), nullable=False)  # 数量

    status = db.Column(db.SmallInteger, default=g_confirm_order_status.UNPROCESSED)  # 状态参见 g_confirm_order_status

    sell_user = db.relationship(User, foreign_keys=[sell_user_id])
    buy_user = db.relationship(User, foreign_keys=[buy_user_id])

