# -*- coding: utf-8 -*-
from default import Config


class DevelopmentConfig(Config):
    LOG_LEVEL = 'DEBUG'
    # Devekioment
    # API = 'http://localhost:5000'
    API = 'http://api.tdb99.com'
