# -*- coding: utf-8 -*-
from app.engine import CommissionHandler, commission_handler_list
from app.model.schedule_task import RecommendScheduleTask


def update_recommend_reward(task):
    return task.user.update_recommend_reward()


class RecommendCommissionHandler(CommissionHandler):
    def __init__(self):
        super(RecommendCommissionHandler, self).__init__(RecommendScheduleTask)

    def get_schedule_task_handlers(self):
        return [update_recommend_reward]


commission_handler_list.append(RecommendCommissionHandler())
