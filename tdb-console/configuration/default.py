# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    API = 'http://api.tdb99.com'
    # API = 'http://127.0.0.1:5000/'

    SECRET_KEY = '\x84m\xb1`\x94N\xe9\xb6\xa1\xb4\xf8\xd8\xe0s\xd3\xc4\xe8\xad\x1a\x84xx\x11\xc4'
    DEFAULT_VARIANT_OPTION = 'cc0a5136-89ee-4aaf-ad54-86a7884339bc'

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    LOG_LEVEL = 'DEBUG'

    ALIYUN_ACCESS_KEY_ID = 'LTAIAcbhNn2UEmwN'
    ALIYUN_ACCESS_KEY_SECRET = '2eUtOlKOeYhESzJFUR2XQgaItCSOQQ'

    OSS_REGION = 'oss-cn-beijing'
    OSS_CDN_URL = '//tdb99.oss-cn-beijing.aliyuncs.com'
    OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
    OSS_BUCKET = 'tdb99'
    OSS_ROOT = '/tdb-console/'

    FRONT_URL = 'http://127.0.0.1:8089/redirect_index'
