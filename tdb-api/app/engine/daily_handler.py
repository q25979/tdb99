# -*- coding: utf-8 -*-
from app.engine import commission_handler_list, CommissionHandler
from app.model.schedule_task import DailyScheduleTask
from app.model.daily_settlement import DailySettlement


def expired_handler(task):
    DailySettlement.settlement_handler()
    return False


class DailyCommissionHandler(CommissionHandler):
    def __init__(self):
        super(DailyCommissionHandler, self).__init__(DailyScheduleTask)

    def get_schedule_task_handlers(self):
        return [expired_handler]


commission_handler_list.append(DailyCommissionHandler())
