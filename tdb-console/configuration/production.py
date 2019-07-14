# -*- coding: utf-8 -*-
from default import Config


class ProductionConfig(Config):
    DEBUG = False
    # API = 'http://localhost:5000'
    API = 'http://api.tdb99.com/'
    
