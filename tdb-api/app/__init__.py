# -*- coding: utf-8 -*-
import logging

from app.model import db
from configuration import load_config


def create_api():
    from flask import Flask
    app = Flask(__name__)
    config = load_config()
    logging.basicConfig(level=config.LOG_LEVEL,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='[%Y-%m-%d %H:%M:%S]')

    app.config.from_object(config)
    db.init_app(app)

    # 管理端
    from app.api.admin.assets import assets_bp
    app.register_blueprint(assets_bp, url_prefix='/admin/assets')

    from app.api.admin.currency import currency_bp
    app.register_blueprint(currency_bp, url_prefix='/admin/currency')

    from app.api.admin.member import member_bp
    app.register_blueprint(member_bp, url_prefix='/admin/member')

    from app.api.admin.order import order_bp
    app.register_blueprint(order_bp, url_prefix='/admin/order')

    from app.api.admin.payment import payment_bp
    app.register_blueprint(payment_bp, url_prefix='/admin/payment')

    from app.api.admin.setting import setting_bp
    app.register_blueprint(setting_bp, url_prefix='/admin/setting')

    from app.api.admin.team import team_bp
    app.register_blueprint(team_bp, url_prefix='/admin/team')

    from app.api.admin.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/admin/user')

    from app.api.admin.news import news_bp
    app.register_blueprint(news_bp, url_prefix='/admin/news')

    # 会员端
    from app.api.member.assets import assets_bp
    app.register_blueprint(assets_bp, url_prefix='/member/assets')

    from app.api.member.currency import currency_bp
    app.register_blueprint(currency_bp, url_prefix='/member/currency')

    from app.api.member.order import order_bp
    app.register_blueprint(order_bp, url_prefix='/member/order')

    from app.api.member.payment import payment_bp
    app.register_blueprint(payment_bp, url_prefix='/member/payment')

    from app.api.member.setting import setting_bp
    app.register_blueprint(setting_bp, url_prefix='/member/setting')

    from app.api.member.team import team_bp
    app.register_blueprint(team_bp, url_prefix='/member/team')

    from app.api.member.news import news_bp
    app.register_blueprint(news_bp, url_prefix='/member/news')

    from app.api.member.upload import upload_bp
    app.register_blueprint(upload_bp, url_prefix='/member/upload')

    from app.api.member.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/member/user')

    # 测试用
    from app.api.test import test
    app.register_blueprint(test)

    from app.api.pin_code import pin_code_bp
    app.register_blueprint(pin_code_bp)

    from app.api.qr_code import qr_code_bp
    app.register_blueprint(qr_code_bp)

    return app
