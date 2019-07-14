# -*- coding: utf-8 -*-
import logging


def create_app():
    from flask import Flask
    from configuration import load_config

    app = Flask(__name__, instance_relative_config=True)

    # Load config
    config = load_config()
    logging.basicConfig(level=config.LOG_LEVEL,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='[%Y-%m-%d %H:%M:%S]')
    app.config.from_object(config)
    app.config.from_pyfile("config.py", silent=True)

    # 注册蓝图
    from app.views.home import home
    app.register_blueprint(home)

    from app.views.setting import setting
    app.register_blueprint(setting, url_prefix='/setting')

    from app.views.setting_order import setting_order
    app.register_blueprint(setting_order, url_prefix='/setting_order')

    from app.views.admin import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from app.views.mall import mall
    app.register_blueprint(mall, url_prefix='/mall')

    from app.views.member import member
    app.register_blueprint(member, url_prefix='/member')

    from app.views.register import register
    app.register_blueprint(register, url_prefix='/register')

    from app.views.order import order
    app.register_blueprint(order, url_prefix='/order')

    from app.views.p2p_order import p2p_order
    app.register_blueprint(p2p_order, url_prefix='/p2p_order')

    from app.views.news import news
    app.register_blueprint(news, url_prefix='/news')

    from app.views.message import message
    app.register_blueprint(message, url_prefix='/message')

    from app.views.wallet import wallet
    app.register_blueprint(wallet, url_prefix='/wallet')

    from app.views.reseller import reseller
    app.register_blueprint(reseller, url_prefix='/reseller')

    from app.views.upload import upload
    app.register_blueprint(upload, url_prefix='/upload')

    from app.views.analyze import analyze
    app.register_blueprint(analyze, url_prefix='/analyze')

    # 注册过滤器
    from app import template_helpers
    template_helpers.init(app)

    return app
