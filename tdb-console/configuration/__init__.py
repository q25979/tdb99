# -*- coding: utf-8 -*-
import os


def load_config():
    mode = os.environ.get('MODE')
    if mode == 'PRODUCTION':
        from configuration.production import ProductionConfig
        return ProductionConfig
    else:
        from configuration.development import DevelopmentConfig
        return DevelopmentConfig
