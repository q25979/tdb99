# -*- coding: utf-8 -*-
import datetime
import decimal
import logging
import time
import traceback
from bs4 import BeautifulSoup

import requests

from app.model import db
from app.model.currency import CryptoCurrency, FiatCurrency


# 从 https://coinmarketcap.com/ 爬取加密货币的美元价格, 30秒取一次
def crypto_currency_usd_price_crawler():
    crypto_currency_usd_price = []

    # url = 'https://www.hbg.com/-/x/general/exchange_rate/list'
    # resp = requests.get(url, timeout=15)
    # usdt_usd = 0
    # if resp.status_code == requests.codes.ok:
    #     data = resp.json()
    #     usd_cny = 0
    #     usdt_cny = 0
    #     for item in data['data']:
    #         if item['name'] == 'usd_cny':
    #             usd_cny = decimal.Decimal(str(item['rate']))
    #         if item['name'] == 'usdt_cny':
    #             usdt_cny = decimal.Decimal(str(item['rate']))
    #     usdt_usd = usdt_cny / usd_cny
    #     crypto_currency_usd_price.append(['USDT', usdt_usd])
    #
    # crypto_currency_code = ['BTC', 'ETH', 'LTC', 'EOS', 'ETC', 'DASH', 'BSV', 'XRP']
    # url = 'https://api.huobi.pro/market/detail/merged'
    # for item in crypto_currency_code:
    #     resp = requests.get(url, params={'symbol': item.lower() + 'usdt'}, timeout=15)
    #     data = resp.json()
    #     price = decimal.Decimal(str(data['tick']['close']))
    #     crypto_currency_usd_price.append([item, price])

    url = 'https://coinmarketcap.com'
    resp = requests.get(url, timeout=15)

    if resp.status_code == requests.codes.ok:
        soup = BeautifulSoup(resp.content, 'lxml')
        rows = soup.select('#currencies tbody tr')
        for row in rows:
            currency = row.select('.currency-symbol')[0].text
            price = row.select('.price')[0].attrs['data-usd']
            percent_change = row.select('.percent-change')[0].attrs['data-percentusd']
            crypto_currency_usd_price.append([currency, price])

    for item in crypto_currency_usd_price:
        CryptoCurrency.query.filter_by(currency_code=item[0]).update(dict(usd_price=item[1]))

    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0 and now.second / 10 < 1:
        for item in crypto_currency_usd_price:
            CryptoCurrency.query.filter_by(currency_code=item[0]).update(dict(start_price=item[1]))

    db.session.commit()


fiat_currency_usd_rate_crawler_timestamp = 0


# 从 http://www.apilayer.net/ 爬取相对美元的法币汇率, 1小时取一次
# https://currencylayer.com/dashboard 账号: wlwlxj@gmail.com
def fiat_currency_usd_rate_crawler():
    global fiat_currency_usd_rate_crawler_timestamp
    timestamp = int(time.time())
    if timestamp - fiat_currency_usd_rate_crawler_timestamp < 60 * 60:
        return False
    fiat_currency_usd_rate_crawler_timestamp = timestamp

    url = 'https://www.hbg.com/-/x/general/exchange_rate/list'

    resp = requests.get(url, timeout=15)
    if resp.status_code == requests.codes.ok:
        data = resp.json()
        for fiat_currency in FiatCurrency.query.all():
            for item in data['data']:
                if item['name'] == 'usd_' + fiat_currency.currency_code.lower():
                    usd_rate = decimal.Decimal(str(item['rate']))
                    FiatCurrency.query.filter_by(currency_code=fiat_currency.currency_code).update(
                        dict(usd_rate=usd_rate))

        db.session.commit()


class Engine(object):
    @staticmethod
    def run():
        while True:
            try:
                crypto_currency_usd_price_crawler()
                fiat_currency_usd_rate_crawler()
            except Exception as e:
                logging.error(traceback.format_exc())
                db.session.rollback()
                logging.error('Engine.run error exception: {}'.format(e))

            time.sleep(5)


if __name__ == '__main__':
    from app import create_api

    app = create_api()

    with app.app_context():
        Engine.run()
