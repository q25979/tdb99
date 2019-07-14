# -*- coding: utf-8 -*-
import datetime
import decimal
from app.model import db
from app.model.user import User
from app.model.currency import Currency
from app.model.assets import Assets, g_assets_record_type
from app.model.setting import Setting
from app.model.order import Order


class DailySettlement(object):

    @staticmethod
    def sponsor_reward_max_level_get(option):
        sponsor_reward_amount = option['sponsor_reward_amount']
        return len(sponsor_reward_amount)

    @staticmethod
    def community_check_user(user, total_balance, transaction_day_cnt, sponsor_cnt, line_cnt, line_people_cnt):
        assets = Assets.get_assets(user.id)
        if assets.grand_total_balance < total_balance:
            return False

        count = db.session.query(db.func.count(User.id)).filter(User.sponsor_id == user.id,
                                                                User.continuous_buy_cnt >= transaction_day_cnt,
                                                                User.active == 1).first()[0]

        if count < sponsor_cnt:
            return False

        q = User.query.filter(User.sponsor_id == user.id, User.active == 1).all()
        qualified_sum = 0
        for user in q:
            if user.team_qualified_cnt >= line_people_cnt:
                qualified_sum += 1

            if qualified_sum >= line_cnt:
                return True

        return False

    @staticmethod
    def settlement_handler():
        option = Setting.get_json('general_option')
        community_node_cnt = option['community_node_cnt']
        community_total_balance = option['community_total_balance']
        community_transaction_day_cnt = option['community_transaction_day_cnt']
        community_sponsor_cnt = option['community_sponsor_cnt']
        community_line_cnt = option['community_line_cnt']
        community_line_people_cnt = option['community_line_people_cnt']

        # 更新连续购买天数
        User.update_continuous_buy_cnt()
        User.query.update(dict(team_qualified_cnt=0))

        # TODO 测试是否可以写成一个update
        Assets.query.filter(Assets.community_today_balance > 0).update(
            dict(community_balance=Assets.community_balance + Assets.community_today_balance))
        Assets.query.update(dict(community_today_balance=0))

        # 筛选出合格用户，并更新每个团队合格用户人数
        q = User.query.filter(User.continuous_buy_cnt >= community_transaction_day_cnt, User.active == 1).all()
        for user in q:
            user.update_team_qualified_cnt()

        count = db.session.query(db.func.count(User.id)).filter(User.is_community_node == 1,
                                                                User.active == 1).first()[0]

        user_q = db.session.query(User).filter(User.id == Assets.user_id,
                                               Assets.grand_total_balance >= community_total_balance[0],
                                               User.is_community_node == 0).all()

        for user in user_q:
            ret = 0
            if count < community_node_cnt[0]:
                ret = DailySettlement.community_check_user(user, community_total_balance[0],
                                                           community_transaction_day_cnt,
                                                           community_sponsor_cnt[0], community_line_cnt[0],
                                                           community_line_people_cnt)
            elif count < community_node_cnt[1]:
                ret = DailySettlement.community_check_user(user, community_total_balance[1],
                                                           community_transaction_day_cnt,
                                                           community_sponsor_cnt[1], community_line_cnt[1],
                                                           community_line_people_cnt)
            elif count < community_node_cnt[2]:
                ret = DailySettlement.community_check_user(user, community_total_balance[2],
                                                           community_transaction_day_cnt,
                                                           community_sponsor_cnt[2], community_line_cnt[2],
                                                           community_line_people_cnt)
            else:
                pass

            if ret:
                user.update_is_community_node()
                count += 1

        if not count:
            return

        # 计算节点分红
        community_dividend_rate = decimal.Decimal(option['community_dividend_rate'])
        currency = Currency.get_currency()
        amount = currency.today_transaction_amount * community_dividend_rate / count
        q = User.query.filter(User.is_community_node == 1, User.active == 1).all()
        detail = {
            'message': '社区节点分红, 当天交易量:{}, 分红比例:{}, 社区节点数量:{}'.format(
                currency.today_transaction_amount, community_dividend_rate, count)
        }
        for user in q:
            assets = Assets.get_assets(user.id)
            assets.update_total_balance(amount, g_assets_record_type.DIVIDEND, detail)

        currency.clear_today_transaction_amount()
