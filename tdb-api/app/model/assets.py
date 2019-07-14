# -*- coding: utf-8 -*-
import decimal
import json

from app.model import UuidBase, AutoIncrementBase, db

from app.model.setting import Setting
from app.type.typedef_const import TypedefConst

g_assets_type = TypedefConst()

g_assets_type.TOTAL = 1  # 总资产钱包 冻结
g_assets_type.COMMUNITY = 2  # 社区钱包 用于交易
g_assets_type.TRANSACTION = 4  # 交易钱包 用于冻结释放

g_assets_record_type = TypedefConst()

g_assets_record_type.EVALUATION = 1  # 测评奖励
g_assets_record_type.RECHARGE = 2  # 充值
g_assets_record_type.BUY = 4  # 买
g_assets_record_type.SELL = 8  # 卖
g_assets_record_type.SPONSOR = 16  # 推荐奖励
g_assets_record_type.BUY_SELL_FREE = 32  # 买卖释放
g_assets_record_type.ACCELERATE_FREE = 64  # 加速释放
g_assets_record_type.EXCHANGE = 128  # 兑换
g_assets_record_type.TRANSACTION = 256  # 转账
g_assets_record_type.DIVIDEND = 512  # 分红


class Assets(UuidBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    total_balance = db.Column(db.Numeric(24, 8), default=0, nullable=False)  # 总资产钱包 冻结
    community_balance = db.Column(db.Numeric(24, 8), default=0, nullable=False)  # 社区钱包 用于交易
    community_today_balance = db.Column(db.Numeric(24, 8), default=0, nullable=False)  # 社区钱包 今日买入的冻结值 用于交易
    transaction_balance = db.Column(db.Numeric(24, 8), default=0, nullable=False)  # 交易钱包 用于冻结释放

    grand_total_balance = db.Column(db.Numeric(24, 8), default=0, nullable=False)  # 累计总资产钱包

    # relationship
    user = db.relationship('User', foreign_keys=[user_id])

    @staticmethod
    def get_assets(user_id):
        return Assets.query.filter_by(user_id=user_id).first()

    def update_grand_total_balance(self, delta_amount):
        delta_amount = decimal.Decimal(delta_amount)
        if delta_amount > 0:
            Assets.query.filter(
                Assets.id == self.id,
                Assets.grand_total_balance >= -delta_amount).update(
                dict(grand_total_balance=Assets.grand_total_balance + delta_amount))
            return True
        return False

    def update_total_balance(self, delta_amount, record_type, details):
        delta_amount = decimal.Decimal(delta_amount)
        rows_changed = Assets.query.filter(
            Assets.id == self.id,
            Assets.total_balance >= -delta_amount).update(
            dict(total_balance=Assets.total_balance + delta_amount))
        if rows_changed == 1:
            option = Setting.get_json('general_option')
            transaction_allow_amount = option['transaction_allow_amount']
            if self.total_balance >= transaction_allow_amount:
                self.user.allow_transaction = 1

            self.update_grand_total_balance(delta_amount)

            record = AssetsBalanceRecord(user_id=self.user_id,
                                         current_amount=self.total_balance,
                                         delta_amount=delta_amount,
                                         assets_type=g_assets_type.TOTAL,
                                         record_type=record_type,
                                         details=json.dumps(details))
            db.session.add(record)
            db.session.flush()
            return True
        return False

    def update_community_balance(self, delta_amount, record_type, details):
        delta_amount = decimal.Decimal(delta_amount)
        rows_changed = Assets.query.filter(
            Assets.id == self.id,
            Assets.community_balance >= -delta_amount).update(
            dict(community_balance=Assets.community_balance + delta_amount))
        if rows_changed == 1:
            record = AssetsBalanceRecord(user_id=self.user_id,
                                         current_amount=self.community_balance + self.community_today_balance,
                                         delta_amount=delta_amount,
                                         assets_type=g_assets_type.COMMUNITY,
                                         record_type=record_type,
                                         details=json.dumps(details))
            db.session.add(record)
            db.session.flush()
            return True
        return False

    def update_community_today_balance(self, delta_amount, record_type, details):
        delta_amount = decimal.Decimal(delta_amount)
        rows_changed = Assets.query.filter(
            Assets.id == self.id,
            Assets.community_today_balance >= -delta_amount).update(
            dict(community_today_balance=Assets.community_today_balance + delta_amount))
        if rows_changed == 1:
            record = AssetsBalanceRecord(user_id=self.user_id,
                                         current_amount=self.community_today_balance + self.community_balance,
                                         delta_amount=delta_amount,
                                         assets_type=g_assets_type.COMMUNITY,
                                         record_type=record_type,
                                         details=json.dumps(details))
            db.session.add(record)
            db.session.flush()
            return True
        return False

    def update_transaction_balance(self, delta_amount, record_type, details):
        delta_amount = decimal.Decimal(delta_amount)
        rows_changed = Assets.query.filter(
            Assets.id == self.id,
            Assets.transaction_balance >= -delta_amount).update(
            dict(transaction_balance=Assets.transaction_balance + delta_amount))
        if rows_changed == 1:
            record = AssetsBalanceRecord(user_id=self.user_id,
                                         current_amount=self.transaction_balance,
                                         delta_amount=delta_amount,
                                         assets_type=g_assets_type.TRANSACTION,
                                         record_type=record_type,
                                         details=json.dumps(details))
            db.session.add(record)
            db.session.flush()
            return True
        return False

    @property
    def community_frozen_balance(self):
        from app.model.order import g_order_side
        from app.model.order import Order, g_order_status
        amount = db.session.query(db.func.sum(Order.amount)).filter(
            Order.user_id == self.user_id,
            Order.side == g_order_side.SELL,
            Order.status.op('&')(g_order_status.CONFIRMED | g_order_status.CANCELLED) == 0).first()[0]
        return amount if amount else 0


# 资产余额记录
class AssetsBalanceRecord(AutoIncrementBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    current_amount = db.Column(db.Numeric(24, 8), nullable=False)  # 当前量
    delta_amount = db.Column(db.Numeric(24, 8), nullable=False)  # 变化量
    assets_type = db.Column(db.SmallInteger, nullable=False)  # 钱包类型 g_assets_type
    record_type = db.Column(db.Integer, nullable=False)  # 记录类型 g_assets_record_type
    details = db.Column(db.Text, nullable=False)  # 详情

    user = db.relationship('User', foreign_keys=[user_id])
