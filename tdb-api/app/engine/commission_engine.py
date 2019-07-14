# -*- coding: utf-8 -*-
import datetime
import logging
import time
import traceback

from app.engine import commission_handler_list
from app.model import db


class Engine(object):
    @staticmethod
    def run():
        while True:
            from app.model.schedule_task import DailyScheduleTask
            DailyScheduleTask.generate_daily_schedule_task(datetime.datetime.now())
            keep_run = False
            try:
                for commission_handler in commission_handler_list:
                    result = commission_handler.process()
                    keep_run = keep_run or result
            except Exception as e:
                logging.error(traceback.format_exc())
                db.session.rollback()
                logging.error('Engine.run error exception: {}'.format(e))

            db.session.commit()
            if not keep_run:
                time.sleep(5)


if __name__ == '__main__':
    from app import create_api

    app = create_api()

    with app.app_context():
        Engine.run()
