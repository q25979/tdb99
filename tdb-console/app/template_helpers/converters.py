# -*- coding: utf-8 -*-
# from app.views.member import LEVEL_FLAG


def register(app, filters):
    filters['gender_to_str'] = gender_to_str
    filters['order_status_to_str'] = order_status_to_str
    # filters['level_to_str'] = level_to_str


def gender_to_str(gender):
    gender_str = {1: u'男', 2: u'女'}
    return gender_str.get(gender, u'未设置')


def order_status_to_str(status):
    order_status_str = {4: u'待发货', 8: u'待收货', 16: u'已收货', 32: u'已取消'}
    return order_status_str.get(status)


# def level_to_str(level):
#     return dict(LEVEL_FLAG)[level]
