# -*- coding: utf-8 -*-
import json
from app.model import db


class Setting(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    GENERAL_OPTION = {
        'evaluation_reward_amount': 200,
        'lebo_price': '0.2',
        'lebo_change_price_cnt': 2500,
        'lebo_price_step': '0.001',
        'recommend_reward_amount': [200, 150, 100, 50, 30, 25, 20, 15, 10, 5],
        'transaction_allow_amount': 3000,
        'sell_amount': 300,
        'sell_people': 300,
        'buy_people': 300,
        'buy_count': 3,
        'sell_count': 3,
        'order_fee_rate': '0.0',
        'contact_us': '1234567890',
        'buy_sell_free_amount': 100,
        'buy_sell_rate': '0.03',
        'transaction_free_generation': 3,
        'transaction_free_amount': 5,
        'transaction_time_begin': ['09:00', '14:00'],
        'transaction_time_end': ['12:00', '18:00'],
        'exchange_amount_min': 300,
        'exchange_amount_max': 5000,
        'community_node_cnt': [314, 400, 600],
        'community_total_balance': [100000, 200000, 300000],
        'community_transaction_day_cnt': 10,
        'community_sponsor_cnt': [10, 20, 30],
        'community_line_cnt': [2, 3, 4],
        'community_line_people_cnt': 100,
        'qr_host': 'http://qr.99lebo.com',
        'community_dividend_rate': '0.01',
        'community_transaction_fee_rate': '0.05',
        'community_free_amount': 5,
        'community_free_generation': 10,
        'order_status_change_time': 2,
        'match_order_cnt': 0,
        'dollar2rmb': '7.0'
    }
    GENERAL_OPTION_DESCRIPTION = {
        'evaluation_reward_amount': u'测评奖励（美元）',
        'lebo_price': u'乐宝初始价格（美元）',
        'lebo_change_price_cnt': u'乐宝价格变化的交易笔数（笔）',
        'lebo_price_step': u'乐宝价格变化步进（美元）',
        'recommend_reward_amount': u'每代推荐人获得奖励（个）',
        'transaction_allow_amount': u'达到该个数允许交易（个）',
        'sell_amount': u'一次的卖单数量（个）',
        'sell_people': u'一天可挂卖单人数（人）',
        'buy_people': u'一天可挂买单人数（人）',
        'buy_count': u'一人一天最多的买入单数（单）',
        'sell_count': u'一人一天最多的卖出单数（单）',
        'order_fee_rate': u'订单手续费率',
        'contact_us': u'联系我们',
        'buy_sell_free_amount': u'买卖各一单时释放个数',
        'buy_sell_rate': u'买卖各一单时的手续费率',
        'transaction_free_generation': u'交易加速释放代数',
        'transaction_free_amount': u'交易加速释放数量',
        'transaction_time_begin': u'交易开始时间',
        'transaction_time_end': u'交易结束时间',
        'exchange_amount_min': u'兑换的最小数量',
        'exchange_amount_max': u'兑换的最大数量',
        'community_node_cnt': u'社区节点阶段对应数量',
        'community_total_balance': u'社区节点阶段对应总资产',
        'community_transaction_day_cnt': u'社区节点连续交易天数',
        'community_sponsor_cnt': u'社区节点阶段对应所需直推用户数',
        'community_line_cnt': u'社区节点阶段对应所需线数',
        'community_line_people_cnt': u'社区节点线对应用户数',
        'qr_host': u'推荐注册地址',
        'community_dividend_rate': u'社区节点分红比率',
        'community_transaction_fee_rate': u'社区节点转账手续费',
        'community_free_amount': u'社区节点交易加速释放个数',
        'community_free_generation': u'社区节点交易加速释放代数',
        'order_status_change_time': u'订单状态变化时间(h)',
        'match_order_cnt': u'订单匹配数量',
        'dollar2rmb': u'美元兑人民币汇率'
    }

    DEFAULT_OPTIONS = (
        ('general_option',
         json.dumps(GENERAL_OPTION),
         u'常规选项',
         json.dumps(GENERAL_OPTION_DESCRIPTION)),
    )

    @staticmethod
    def update_default_options():
        for name, value, title, description in Setting.DEFAULT_OPTIONS:
            setting = Setting.query.get(name)
            if setting:
                setting.title = title
                setting.description = description
                runtime_json = json.loads(setting.value)
                default_json = json.loads(value)
                for k, v in default_json.items():
                    if k not in runtime_json:
                        runtime_json[k] = v
                setting.value = json.dumps(runtime_json)
            else:
                setting = Setting(name=name, value=value, title=title, description=description)
                db.session.add(setting)
        db.session.commit()

    @staticmethod
    def get_json(name):
        return json.loads(Setting.query.get(name).value)
