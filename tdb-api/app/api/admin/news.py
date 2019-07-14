# -*- coding: utf-8 -*-
from flask_restful import Resource, marshal_with, abort, reqparse, Api, fields
from app.model.news import News
from app.api import pagination_query, AddResource
from flask.blueprints import Blueprint
from app.api.admin import admin_login_required
from app.model import Datetime2Timestamp, db

news_bp = Blueprint('admin_news_bp', __name__)
news_api = AddResource(Api(news_bp))

news_fields = {
    'id': fields.String,
    'created_timestamp': fields.Integer,
    'title': fields.String,
    'details': fields.String
}

news_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(news_fields))
}


@news_api.add_resource()
class NewsListApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(news_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parsed_args = parser.parse_args()

        news = News.query

        news = news.order_by(News.created_at.desc())

        return pagination_query(parsed_args['per_page'], parsed_args['page'], news)

    @marshal_with(news_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, nullable=False, location='json')
        parser.add_argument('details', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        # 新闻标题有可能不唯一
        news = News.query.filter(News.title == parsed_args['title'],
                                 News.details == parsed_args['details']).first()
        if news:
            abort(400, code=1006, message={'title&details': 'news title&details does exist'})

        news = News(title=parsed_args['title'], details=parsed_args['details'])

        db.session.add(news)
        db.session.commit()
        return news


@news_api.add_resource('/details/<string:news_id>')
class NewsDetailApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(news_fields)
    def get(self, news_id):
        news = News.query.get(news_id)
        if news is None:
            abort(400, code=1001, message={'news_id': 'news id does not exist'})
        return news

    @marshal_with(news_fields)
    def put(self, news_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, nullable=False, location='json')
        parser.add_argument('details', type=str, nullable=False, location='json')
        parsed_args = parser.parse_args()

        news = News.query.get(news_id)

        if news is None:
            abort(400, code=1001, message={'news_id': 'news_id does not exist'})

        if parsed_args['title']:
            news.title = parsed_args['title']
        if parsed_args['details']:
            news.details = parsed_args['details']

        db.session.commit()
        return news

    def delete(self, news_id):
        news = News.query.get(news_id)

        if news is None:
            abort(400, code=1001, message={'news_id': 'news_id does not exist'})

        db.session.delete(news)
        db.session.commit()
        return {}
