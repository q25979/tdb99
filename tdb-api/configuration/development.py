# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig(object):
    DEBUG = True
    SECRET_KEY = 'e2G6RaumKIv5iHPnYrFDLIiURrY1jjU9jkkrkySTCh79sL7D5q8mC26JaotUofHH'

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    LOG_LEVEL = 'DEBUG'

    BUNDLE_ERRORS = True

    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1:3306/test?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql://tdb99:Aa123123@rm-bp111a14j448rfky7wo.mysql.rds.aliyuncs.com/tdb99?charset=utf8mb4'

    TIMEZONE = 'Asia/Shanghai'

    PRODUCT_NAME = 'lebo-api'

    ALIYUN_ACCESS_KEY_ID = 'LTAId5JGkZzEFYSw'
    ALIYUN_ACCESS_KEY_SECRET = 'y9DCNzafnatLMxE1s7IxqvI5NlQe0M'

    OSS_REGION = 'oss-ap-southeast-1'
    OSS_CDN_URL = 'http://xiaoyu168.oss-ap-southeast-1.aliyuncs.com'
    OSS_ENDPOINT = 'oss-ap-southeast-1.aliyuncs.com'
    OSS_BUCKET = 'xiaoyu168'
    OSS_ROOT = 'lebo-app/'
