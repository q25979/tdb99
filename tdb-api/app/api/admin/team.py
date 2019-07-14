# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import abort, fields, marshal_with, Resource, Api, reqparse

from app.api import AddResource
from app.api.admin import admin_login_required
from app.model import DecimalToString
from app.model.user import User

team_bp = Blueprint('admin_team_bp', __name__)
team_api = AddResource(Api(team_bp))

admin_member_downline_fields = {
    'id': fields.String,
    'name': fields.String,
    'mobile': fields.String,
    'uid': fields.String,
    'sponsor_id': fields.String,
}


# 推荐网络图
@team_api.add_resource('/sponsor_downline')
class AdminMemberSponsorDownlineApi(Resource):
    decorators = [admin_login_required]

    @marshal_with(admin_member_downline_fields, envelope='objects')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('unique_id', type=str, required=True, nullable=False, location='args')
        parsed_args = parser.parse_args()

        parent = User.get_user(parsed_args['unique_id'])
        if parent is None:
            abort(400, code=1001, message={'parent': 'parent does not exist'})
        user_list = User.query.filter(User.sponsor_id == parent.id,
                                      User.locked != 2).all()
        return user_list
