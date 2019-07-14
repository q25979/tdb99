# -*- coding: utf-8 -*-
import decimal
import datetime
from datetime import timedelta
from app.model import db, AutoIncrementBase
from app.model.setting import Setting


# 加密货币
class Currency(AutoIncrementBase):
    CURRENCY_ROOT_ID = 1

    usd_price = db.Column(db.Numeric(24, 8), nullable=False)  # LEBO 美元价格

    transaction_cnt = db.Column(db.Integer, default=0)  # 交易笔数

    today_transaction_amount = db.Column(db.Integer, default=0)  # 今日交易额

    # def update_price(self, delta_amount):
    #     delta_amount = decimal.Decimal(delta_amount)
    #     rows_changed = Currency.query.filter(Currency.id == self.id, Currency.usd_price >= -delta_amount).update(
    #         dict(usd_price=Currency.usd_price + delta_amount))
    #     if rows_changed == 1:
    #         return True
    #     return False

    def update_transaction_cnt(self):
        option = Setting.get_json('general_option')
        lebo_change_price_cnt = option['lebo_change_price_cnt']
        lebo_price_step = decimal.Decimal(option['lebo_price_step'])
        sell_amount = option['sell_amount']

        Currency.query.filter(Currency.id == self.id).update(
            dict(transaction_cnt=Currency.transaction_cnt + 1,
                 today_transaction_amount=Currency.today_transaction_amount + sell_amount))

        rows_changed = Currency.query.filter(
            Currency.id == self.id, Currency.transaction_cnt >= lebo_change_price_cnt).update(
            dict(usd_price=Currency.usd_price + lebo_price_step, transaction_cnt=0))
        if rows_changed:
            record = CurrencyPriceRecord(current_price=self.usd_price, delta_price=lebo_price_step,
                                         transaction_cnt=lebo_change_price_cnt)
            db.session.add(record)
            db.session.flush()
        return True

    def clear_today_transaction_amount(self):
        Currency.query.filter(Currency.id == self.id).update(dict(today_transaction_amount=0))

    @staticmethod
    def get_price():
        currency = Currency.query.get(Currency.CURRENCY_ROOT_ID)
        if currency is not None:
            return currency.usd_price
        else:
            return 0

    @staticmethod
    def get_currency():
        currency = Currency.query.get(Currency.CURRENCY_ROOT_ID)
        return currency

    @staticmethod
    def initialize():
        currency = Currency.query.filter(Currency.id == Currency.CURRENCY_ROOT_ID,
                                         Currency.usd_price.isnot(None)).first()
        if currency is None:
            option = Setting.get_json('general_option')
            lebo_price = decimal.Decimal(option['lebo_price'])
            currency = Currency(usd_price=lebo_price)
            db.session.add(currency)
            db.session.flush()

            for i in range(7, 0, -1):
                record = CurrencyPriceRecord(current_price=lebo_price, delta_price=0, transaction_cnt=0,
                                             created_at=datetime.datetime.now() - timedelta(days=i))
                db.session.add(record)
                db.session.flush()

            db.session.commit()


# 资产余额记录
class CurrencyPriceRecord(AutoIncrementBase):
    current_price = db.Column(db.Numeric(24, 8), nullable=False)  # 当前价格
    delta_price = db.Column(db.Numeric(24, 8), nullable=False)  # 变化价格
    transaction_cnt = db.Column(db.Integer, default=0)  # 交易笔数


# 法币
class FiatCurrency(AutoIncrementBase):
    country = db.Column(db.String(60), nullable=False)  # 国家名称
    country_code = db.Column(db.String(20), nullable=False)  # 国家编码
    currency = db.Column(db.String(60), nullable=False)  # 货币名称
    currency_code = db.Column(db.String(20), nullable=False)  # 货币编码
    usd_rate = db.Column(db.Numeric(24, 8), nullable=False)  # 美元汇率
    sequence = db.Column(db.SmallInteger, nullable=False)  # 排序

    __table_args__ = (db.UniqueConstraint('country_code', 'currency_code'),)

    @staticmethod
    def initialize():
        fiat_currency_list = (
            ('中华人民共和国', 'CN', 'CNY', '人民币元'),
            ('中国香港', 'HK', 'HKD', '港元'),
            ('中国台湾', 'TW', 'TWD', '台湾元'),
            ('英国', 'GB', 'GBP', '英镑'),
            ('美国', 'US', 'USD', '美元'),
            ('法国', 'FR', 'EUR', '欧元'),
            ('德国', 'DE', 'EUR', '欧元'),
            ('日本', 'JP', 'JPY', '日元'),
            ('阿拉伯联合酋长国', 'AE', 'AED', '阿联酋 迪拉姆'),
            ('泰国', 'TH', 'THB', '泰铢'),
            ('俄罗斯', 'RU', 'RUB', '俄罗斯卢布'),
            ('加拿大', 'CA', 'CAD', '加拿大元'),
            ('韩国', 'KR', 'KRW', '韩元'),
            ('马来西亚', 'MY', 'MYR', '马来西亚林吉特'),
            ('新加坡', 'SG', 'SGD', '新加坡元')

        )
        for fiat_currency in fiat_currency_list:
            currency = FiatCurrency.query.filter_by(country_code=fiat_currency[1],
                                                    currency_code=fiat_currency[2]).first()
            if currency is None:
                currency = FiatCurrency(country=fiat_currency[0],
                                        country_code=fiat_currency[1],
                                        currency=fiat_currency[3],
                                        currency_code=fiat_currency[2],
                                        usd_rate=0,
                                        sequence=0)
                db.session.add(currency)
        db.session.commit()


# 加密货币
class CryptoCurrency(AutoIncrementBase):
    currency_code = db.Column(db.String(20), nullable=False)  # 货币编码
    erc20_token = db.Column(db.SmallInteger, nullable=False)  # 代币: 0 不是  1 是
    usd_price = db.Column(db.Numeric(24, 8), nullable=False)  # 美元价格
    sequence = db.Column(db.SmallInteger, nullable=False)  # 排序
    init_block_number = db.Column(db.Integer, default=0, nullable=False)  # 初始索引块数
    indexed_block_number = db.Column(db.Integer, default=0, nullable=False)  # 已索引块数
    start_price = db.Column(db.Numeric(24, 8), nullable=False)  # 0 点时价格 用于计算涨幅
    percent_change_1h = db.Column(db.Numeric(24, 8), default=0, nullable=False)
    percent_change_24h = db.Column(db.Numeric(24, 8), default=0, nullable=False)
    percent_change_7d = db.Column(db.Numeric(24, 8), default=0, nullable=False)

    __table_args__ = (db.UniqueConstraint('currency_code', 'erc20_token'),)

    @property
    def percent_change(self):
        if self.start_price:
            return (self.usd_price - self.start_price) / self.start_price * 100
        else:
            return 0

    @staticmethod
    def initialize():

        crypto_currency_list = ['BTC', 'USDT', 'ETH', 'LTC', 'EOS', 'ETC', 'DASH', 'BSV', 'XRP', 'DOGE']
        for crypto_currency in crypto_currency_list:
            currency = CryptoCurrency.query.filter_by(currency_code=crypto_currency,
                                                      erc20_token=0).first()
            if currency is None:
                currency = CryptoCurrency(currency_code=crypto_currency,
                                          erc20_token=0,
                                          usd_price=0,
                                          start_price=0,
                                          sequence=0)

                db.session.add(currency)

        db.session.commit()
