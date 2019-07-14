# -*- coding: utf-8 -*-
import os
import uuid

from flask import Blueprint
from flask import current_app
from flask_restful import Api, Resource, abort
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage

from app.api import AddResource, oss_proof_img_key, oss_bucket
from app.api.member import member_login_required

upload_bp = Blueprint('upload_bp', __name__)
upload_api = AddResource(Api(upload_bp))


@upload_api.add_resource('/image')
class MemberUploadProofImgApi(Resource):
    # decorators = [member_login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('attachment', type=FileStorage, required=True, nullable=False, location='files')
        parsed_args = parser.parse_args()
        attachment = parsed_args['attachment']
        if not attachment.content_type.startswith('image'):
            abort(400, code=1003, message={'attachment': 'attachment must be image'})

        file_extension = os.path.splitext(attachment.filename)[1]
        key = oss_proof_img_key('{}{}'.format(uuid.uuid4(), file_extension))
        bucket = oss_bucket()
        headers = {'Content-Type': attachment.content_type}
        result = bucket.put_object(key, attachment, headers=headers)
        if result.status != 200:
            abort(400, code=1012, message={'result': result.status})
        return {'key': current_app.config['OSS_CDN_URL'] + '/' + key}
