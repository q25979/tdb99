# -*- coding: utf-8 -*-
from app.model import UuidBase, db
from app.type.typedef_const import TypedefConst

g_payment_type = TypedefConst()

g_payment_type.BANK = 0  # 银行卡
g_payment_type.WECHAT = 1  # 微信
g_payment_type.ALIPAY = 2   # 支付宝
g_payment_type.USDT = 3   # USDT


class Payment(UuidBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    type = db.Column(db.SmallInteger, nullable=False)  # 收款类型 g_payment_type

    name = db.Column(db.String(64))  # 姓名
    bank = db.Column(db.String(128))  # 开户行
    card_number = db.Column(db.String(64))  # 卡号
    wechat = db.Column(db.String(64))  # 微信
    wechat_image = db.Column(db.String(512), default='')  # 微信二维码
    alipay = db.Column(db.String(64))  # 支付宝
    alipay_image = db.Column(db.String(512), default='')  # 支付宝二维码
    address = db.Column(db.String(64))  # usdt 地址
    remark  = db.Column(db.String(64), default='')  # 备注

    invalid = db.Column(db.SmallInteger, default=0)  # 收款方式是否有效 0 有效  1 无效

    # relationship
    user = db.relationship('User', foreign_keys=[user_id])

    @staticmethod
    def get_payment(user_id, type):
        return Payment.query.filter_by(user_id=user_id, type=type, invalid=0).first()

    @staticmethod
    def get_all_payment(user_id):
        return Payment.query.filter_by(user_id=user_id, invalid=0).all()

