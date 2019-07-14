# -*- coding: utf-8 -*-
from app.model import db, AutoIncrementBase


class News(AutoIncrementBase):
    title = db.Column(db.String(128), nullable=False)  # 新闻名称
    details = db.Column(db.Text, nullable=False)  # 新闻内容
