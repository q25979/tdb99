# -*- coding: utf-8 -*-
from configuration.development import DevelopmentConfig


class StagingConfig(DevelopmentConfig):
    DEBUG = False

    LOG_LEVEL = 'DEBUG'

    PRODUCT_NAME = 'lebo-api-staging'

    SQLALCHEMY_ECHO = False
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@47.75.207.244/test?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = 'mysql://tdb99:@rm-bp111a14j448rfky7wo.mysql.rds.aliyuncs.com/tdb99?charset=utf8mb4'
