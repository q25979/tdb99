# -*- coding: utf-8 -*-
import app.model.admin_user
import app.model.assets
import app.model.buy_order
import app.model.confirm_order
import app.model.currency
import app.model.daily_settlement
import app.model.match_order
import app.model.order
import app.model.order_old
import app.model.payment
import app.model.pin_code
import app.model.schedule_task
import app.model.sell_order
import app.model.setting
import app.model.user

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_api
from app.model import db

app = create_api()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def db_initialize():
    from app.model.currency import Currency
    Currency.initialize()

    from app.model.admin_user import AdminUser
    AdminUser.initialize()

    from app.model.user import User
    User.initialize()

    from app.model.currency import CryptoCurrency, FiatCurrency
    CryptoCurrency.initialize()
    FiatCurrency.initialize()


@manager.command
def update_setting():
    from app.model.setting import Setting
    Setting.update_default_options()


@manager.command
def db_restore():
    import logging
    import time
    from app.model.order_old import OrderOld, g_order_old_status
    from app.model.order import Order, g_order_side, g_order_status
    from app.model.sell_order import SellOrder, g_sell_order_status
    from app.model.buy_order import BuyOrder, g_buy_order_status
    from app.model.match_order import MatchOrder
    from app.model.payment import Payment, g_payment_type
    from app.model.assets import Assets, g_assets_record_type

    start_time = time.time()

    order_old_q = OrderOld.query.all()

    for old in order_old_q:

        logging.info('id={}'.format(old.id))

        if old.status == g_order_old_status.PENDING:
            detail = {'message': '后台取消挂单'}
            old.status = g_order_status.CANCELLED
            assets = Assets.get_assets(old.user_id)
            assets.update_community_balance(old.amount, g_assets_record_type.SELL, detail)
            db.session.flush()

        sell_order = SellOrder(created_at=old.created_at, updated_at=old.updated_at, user_id=old.user_id,
                               number=old.number, amount=old.amount, status=g_sell_order_status.PROCESSED)
        if sell_order is None:
            logging.info('sell order is None, id={}'.format(old.id))
            continue

        db.session.add(sell_order)

        s_order = Order(created_at=old.created_at, updated_at=old.updated_at, user_id=old.user_id,
                        side=g_order_side.SELL, number=old.number, amount=old.amount, status=old.status)
        if s_order is None:
            logging.info('s order is None, id={}'.format(old.id))
            continue

        db.session.add(s_order)

        if old.match_user_id is not None:
            buy_order = BuyOrder(created_at=old.created_at, updated_at=old.updated_at, user_id=old.match_user_id,
                                 number=old.number, amount=old.amount, status=g_buy_order_status.PROCESSED)
            if buy_order is None:
                logging.info('buy order is None, id={}'.format(old.id))
                continue

            db.session.add(buy_order)

            b_order = Order(created_at=old.created_at, updated_at=old.updated_at, user_id=old.match_user_id,
                            side=g_order_side.BUY, number=old.number, amount=old.amount, status=old.status)
            if b_order is None:
                logging.info('b order is None, id={}'.format(old.id))
                continue

            db.session.add(b_order)
            db.session.flush()

            payment_amount = None
            payment_amount_usdt = None
            if old.payment.type == g_payment_type.USDT:
                payment_amount_usdt = old.payment_amount
            else:
                payment_amount = old.payment_amount
            match_order = MatchOrder(created_at=old.match_at, updated_at=old.updated_at, sell_user_id=old.user_id,
                                     buy_user_id=old.match_user_id, sell_order_id=s_order.id, buy_order_id=b_order.id,
                                     sell_number=old.number, buy_number=old.number, payment_amount=payment_amount,
                                     payment_amount_usdt=payment_amount_usdt, proof_img=old.proof_img,
                                     current_price=old.current_price, payment_id=old.payment_id)
            if match_order is None:
                logging.info('match order is None, id={}'.format(old.id))
                continue

            db.session.add(match_order)
            db.session.flush()

            s_order.match_order_id = match_order.id
            b_order.match_order_id = match_order.id
            db.session.flush()

    Assets.query.filter(Assets.community_balance > 0).update(
        dict(grand_total_balance=Assets.grand_total_balance + Assets.community_balance * 3,
             total_balance=Assets.total_balance + Assets.community_balance * 3))

    Assets.query.filter(Assets.community_balance > 0).update(dict(community_balance=0))

    crl_time = time.time() - start_time
    logging.info('db_restore_time:{}'.format(crl_time))
    db.session.commit()


""" 使用说明
1. initialize
  python manage.py db init

2. migrate
  python manage.py db migrate
  python manage.py db upgrade

positional arguments:
  {upgrade,migrate,current,stamp,init,downgrade,history,revision}
    upgrade             Upgrade to a later version
    migrate             Alias for 'revision --autogenerate'
    current             Display the current revision for each database.
    stamp               'stamp' the revision table with the given revision;
                        dont run any migrations
    init                Generates a new migration
    downgrade           Revert to a previous version
    history             List changeset scripts in chronological order.
    revision            Create a new revision file.
"""

if __name__ == '__main__':
    manager.run()
