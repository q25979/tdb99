# -*- coding: utf-8 -*-
from flask import Blueprint, g
from flask_restful import abort, fields, marshal_with, Resource, Api, reqparse

from app.api import AddResource
from app.api.member import member_login_required
from app.model import DecimalToString, Datetime2Timestamp
from app.model.user import User

team_bp = Blueprint('member_team_bp', __name__)
team_api = AddResource(Api(team_bp))

member_downline_fields = {
    'id': fields.String,
    'nickname': fields.String,
    'name': fields.String,
    'mobile': fields.String,
    'uid': fields.String,
    'created_at': Datetime2Timestamp
}


# 推荐网络图
@team_api.add_resource('/sponsor_downline')
class MemberSponsorDownlineApi(Resource):
    decorators = [member_login_required]

    @marshal_with(member_downline_fields, envelope='objects')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('depth', type=int, default=1, location='args')
        parsed_args = parser.parse_args()
        user_list_id = [g.current_user.id]
        user_list = []
        for i in range(parsed_args['depth']):
            user_list = User.query.filter(User.sponsor_id.in_(user_list_id),
                                          User.locked != 2).all()
            if not user_list:
                break
            user_list_id = [x.id for x in user_list]

        return user_list
