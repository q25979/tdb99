# -*- coding: utf-8 -*-
import io
import qrcode
from flask import send_file, Blueprint
from flask_restful import Resource
from flask_restful import Api, Resource, reqparse, abort
from app.api import restful_api, AddResource


qr_code_bp = Blueprint('qr_code', __name__)
qr_code_api = Api(qr_code_bp)
qr_code = AddResource(qr_code_api)


# 二维码
@qr_code.add_resource('/address_qr_code/<string:address>')
class AddressQrCodeApi(Resource):
    def get(self, address):
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1)

        url = address
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image()

        byte_io = io.BytesIO()
        qr_img.save(byte_io, 'PNG')
        byte_io.seek(0)
        return send_file(byte_io, mimetype='image/png')
