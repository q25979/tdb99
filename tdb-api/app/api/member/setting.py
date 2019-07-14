# -*- coding: utf-8 -*-
import json

from flask import Blueprint
from flask_restful import Api, Resource, marshal_with, fields

from app.api import AddResource
from app.api.member import member_login_required
from app.model.setting import Setting

setting_bp = Blueprint('member_setting_bp', __name__)
setting_api = AddResource(Api(setting_bp))

admin_settings_fields = {
    "name": fields.String,
    "title": fields.String,
    "value": fields.Raw(attribute=lambda x: json.loads(x.value)),
    "description": fields.Raw(attribute=lambda x: json.loads(x.description))
}


@setting_api.add_resource()
class AdminSetting(Resource):
    decorators = [member_login_required]

    @marshal_with(admin_settings_fields)
    def get(self):
        return Setting.query.get('general_option')
