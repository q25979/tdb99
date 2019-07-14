# -*- coding: utf-8 -*-
from app.model import AutoIncrementBase, db, generate_timestamp_id
from app.model.user import User, g_user_transaction_level
from app.type.typedef_const import TypedefConst

g_buy_order_status = TypedefConst()

g_buy_order_status.UNPROCESSED = 0  # 未处理
g_buy_order_status.PROCESSED = 1  # 处理成功
g_buy_order_status.FAILED = 2  # 处理失败


class BuyOrder(AutoIncrementBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)  # 用户
    side = db.Column(db.SmallInteger, default=1, nullable=False)  # 单类型 参见 g_order_side
    number = db.Column(db.String(16), default=generate_timestamp_id, unique=True, nullable=False)

    amount = db.Column(db.Numeric(24, 8), nullable=False)  # 数量

    status = db.Column(db.SmallInteger, default=g_buy_order_status.UNPROCESSED)  # 状态参见 g_buy_order_status

    details = db.Column(db.String(255), default='{}', nullable=True)  # 失败备注

    user = db.relationship(User, foreign_keys=[user_id])

    @staticmethod
    def order_create(user, amount):
        if user.transaction_level != g_user_transaction_level.ULTIMATE:
            order = BuyOrder.query.filter(BuyOrder.user_id == user.id,
                                          BuyOrder.status == g_buy_order_status.UNPROCESSED).first()
            if order is not None:
                return False, dict(code=1006, message={'user': 'user have order does not finish'})

        order = BuyOrder(user_id=user.id, amount=amount)
        return True, order
