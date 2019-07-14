# -*- coding: utf-8 -*-
import time

import jinja2


def register(app, filters):
    filters['timestamp_to_str'] = timestamp_to_str
    filters['html_attr'] = html_attribute
    filters['has_flag'] = has_flag
    filters['currency'] = format_currency


def has_flag(value, flag):
    return (value & flag) == flag


def timestamp_to_str(value):
    if value:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))
    else:
        return u'无'


def html_attribute(html_attribute_string):
    data = []
    for char in html_attribute_string:
        if char == '"':
            data.append('&quot;')
        else:
            data.append(char)
    return jinja2.Markup(''.join(data))


def format_currency(amount, currency=u''):
    if not (amount is None):
        # if float(amount).is_integer():
        #     return u"{}{}".format(currency, int(float(amount)))
        # else:
        return u"{}{:.8f}".format(currency, float(amount))
    else:
        return ''
