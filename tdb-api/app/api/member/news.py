# -*- coding: utf-8 -*-
import requests
from flask_restful import fields, Resource, marshal_with, abort, reqparse, Api

from app.model.news import News
from app.api import pagination_query, AddResource
from flask.blueprints import Blueprint
from app.model import Datetime2Timestamp

news_bp = Blueprint('news_bp', __name__)
news_api = AddResource(Api(news_bp))

news_fields = {
    'id': fields.String,
    'created_at': Datetime2Timestamp,
    'title': fields.String,
    'details': fields.String,
}

news_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(news_fields))
}


# 新闻为公告，可以不用户认证。

@news_api.add_resource()
class NewsList(Resource):
    @marshal_with(news_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parsed_args = parser.parse_args()

        news = News.query
        news = news.order_by(News.created_at.desc())

        return pagination_query(parsed_args['per_page'], parsed_args['page'], news)


@news_api.add_resource('/detail/<string:news_id>')
class NewsDetail(Resource):
    @marshal_with(news_fields)
    def get(self, news_id):
        news = News.query.get(news_id)
        if news is None:
            abort(400, code=1001, message={'news_id': 'news id does not exist'})
        return news
