# -*- coding: utf-8 -*-
import datetime
from app.model import db
from app.model.schedule_task import ScheduleTaskBase


class CommissionHandler(object):
    def __init__(self, schedule_task_class):
        assert issubclass(schedule_task_class, ScheduleTaskBase)
        self.model_class = schedule_task_class

    def get_schedule_task_handlers(self):
        raise NotImplemented("Must implement it")

    def process(self):  # 返回 True 表示继续执行; 返回 False 表示暂停执行
        task = self.model_class.peek()
        if not task:
            return False
        handlers = self.get_schedule_task_handlers()
        keep_run = False
        for handler in handlers:
            result = handler(task)
            keep_run = keep_run or result
        task.done(datetime.datetime.utcnow())
        db.session.commit()
        return keep_run


commission_handler_list = []

import app.engine.daily_handler
import app.engine.register_handler
import app.engine.recommend_handler
