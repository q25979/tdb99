# -*- coding: utf-8 -*-
import logging
import time
import traceback

from app.model.order import Order


class Engine(object):
    @staticmethod
    def run():
        while True:
            try:
                Order.confirm_order_process()
            except Exception as e:
                logging.error(traceback.format_exc())
                db.session.rollback()
                logging.error('Engine.run error exception: {}'.format(e))

            db.session.close()
            time.sleep(1)


if __name__ == '__main__':
    from app import create_api, db

    app = create_api()

    with app.app_context():
        Engine.run()
