# -*- coding: utf-8 -*-
import datetime
import decimal
import random
import time
import uuid

from flask import current_app
from flask_restful import fields
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autoflush": False})


class Datetime2Timestamp(fields.Raw):
    def __init__(self, **kwargs):
        super(Datetime2Timestamp, self).__init__(default=0, **kwargs)

    def format(self, value):
        return datetime_to_timestamp(value)


def generate_timestamp_id():
    return str(int(time.time()) * 1000000 + random.randint(100000, 999999))


# 当前时间戳
def current_timestamp():
    return int(time.time())


# 当天起始、结束时间
def day_datetime(date_time):
    begin = datetime.datetime(year=date_time.year,
                              month=date_time.month,
                              day=date_time.day)
    end = begin + datetime.timedelta(days=1)
    return begin, end


# 时间转换为时间戳
def datetime_to_timestamp(date_time):
    return date_time.timestamp()


# 时间戳转换为时间
def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


class DecimalToString(fields.Raw):
    def format(self, value):
        return '{0:.8f}'.format(decimal.Decimal(value))


def is_dev_and_test():
    is_dev_env = current_app.config['SQLALCHEMY_DATABASE_URI'] == current_app.config['DEV_ENV_DATABASE_URI']
    is_test_env = current_app.config['SQLALCHEMY_DATABASE_URI'] == current_app.config['TEST_ENV_DATABASE_URI']
    return is_dev_env or is_test_env


def is_current_product_supported(supported_product_list):
    product_name = current_app.config['PRODUCT_NAME']
    for supported_product in supported_product_list:
        if supported_product in product_name:
            return True
    return False


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now,
                           nullable=False)

    @property
    def created_timestamp(self):
        return datetime_to_timestamp(self.created_at)

    @property
    def updated_timestamp(self):
        return datetime_to_timestamp(self.updated_at)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return {}


class UuidBase(BaseModel):
    __abstract__ = True

    id = db.Column(db.String(36), default=uuid.uuid4, primary_key=True)


class AutoIncrementBase(BaseModel):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
