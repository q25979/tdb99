# -*- coding: utf-8 -*-
from app.model import db, AutoIncrementBase, day_datetime
from app.model.user import User
from app.model.order import Order


class ScheduleTaskBase(AutoIncrementBase):
    __abstract__ = True

    status = db.Column(db.SmallInteger, default=0)  # 0 未处理  1 已处理
    processed_at = db.Column(db.DateTime)

    def done(self, processed_at):
        self.status = 1
        self.processed_at = processed_at

    @classmethod
    def peek(cls):
        return cls.query.filter_by(status=0).order_by(cls.id).first()


class DailyScheduleTask(ScheduleTaskBase):
    timestamp = db.Column(db.Integer, nullable=False, unique=True)

    @staticmethod
    def generate_daily_schedule_task(now):
        begin, end = day_datetime(now)
        timestamp = begin.timestamp()
        if DailyScheduleTask.query.filter_by(timestamp=timestamp).first():
            return
        task = DailyScheduleTask(timestamp=timestamp)
        db.session.add(task)
        db.session.commit()


class RegisterScheduleTask(ScheduleTaskBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False, unique=True)

    user = db.relationship(User)


class RecommendScheduleTask(ScheduleTaskBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False, unique=True)

    user = db.relationship(User)


class CheckOrderStatusTask(ScheduleTaskBase):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    # relationship
    order = db.relationship(Order)
