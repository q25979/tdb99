# -*- coding: utf-8 -*-
from configuration.development import DevelopmentConfig


class ProductionConfig(DevelopmentConfig):
    DEBUG = False

    LOG_LEVEL = 'INFO'

    PRODUCT_NAME = 'lebo-api-online'

    SQLALCHEMY_ECHO = False
    # SQLALCHEMY_DATABASE_URI = 'mysql://lb2019:tymmgg89+@rm-j6crvg40ux505prbu.mysql.rds.aliyuncs.com/new-lebo2019?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = 'mysql://tdb99:Aa123123@rm-bp111a14j448rfky7wo.mysql.rds.aliyuncs.com/tdb99?charset=utf8mb4'

    SQLALCHEMY_POOL_SIZE = 100
