# -*- coding: utf-8 -*-
from app.engine import CommissionHandler, commission_handler_list
from app.model.schedule_task import RegisterScheduleTask


def update_user_left_right_id_handler(task):
    return task.user.update_left_right_id()


class RegisterCommissionHandler(CommissionHandler):
    def __init__(self):
        super(RegisterCommissionHandler, self).__init__(RegisterScheduleTask)

    def get_schedule_task_handlers(self):
        return [update_user_left_right_id_handler]


commission_handler_list.append(RegisterCommissionHandler())
