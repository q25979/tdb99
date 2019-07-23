# -*- coding: utf-8 -*-
import os
import random
from io import BytesIO

from captcha.image import ImageCaptcha
from flask import Blueprint, make_response
from flask_restful import Api, Resource, reqparse, abort
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient

from app.api import AddResource
from app.api.utils import get_random_str
from app.model.pin_code import CaptchaPinCode, SmsPinCode
from app.model.user import User

pin_code_bp = Blueprint('pin_code', __name__)
pin_code_api = Api(pin_code_bp)
pin_code = AddResource(pin_code_api)


@pin_code.add_resource('/captcha_pin_code')
class PinCodeCaptcha(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str, required=True, location='args',
                            help="uuid cannot be blank!")
        parser_args = parser.parse_args()
        code = get_random_str()
        image = ImageCaptcha()
        data = image.generate_image(code)
        out = BytesIO()
        data.save(out, "jpeg", quality=75)

        pin_code = CaptchaPinCode.query.get(parser_args['uuid'])
        if pin_code is None:
            pin_code = CaptchaPinCode(id=parser_args['uuid'])
        code = code.lower()
        pin_code.generate_signature(code)

        response = make_response(out.getvalue())
        response.headers['Content-Type'] = 'image/jpeg'
        return response


@pin_code.add_resource('/sms_pin_code')
class PinCodeSms(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('country_code', type=str, location='json')
        parser.add_argument('mobile', required=True, type=str, location='json')
        parsed_args = parser.parse_args()

        # if not parsed_args['mobile']:  # 获取当前用户的手机号
        #     if parsed_args['token']:
        #         current_user = User.verify_auth_token(parsed_args['token'])
        #         if current_user is not None:
        #             parsed_args['mobile'] = current_user.mobile
        if not parsed_args['mobile']:
            abort(400, code=1000, message={'mobile': 'mobile is required'})

        country_code = parsed_args['country_code']
        if parsed_args['country_code']:
            if "+" not in parsed_args['country_code']:
                country_code = '+' + parsed_args['country_code']

        code = str(random.randint(100000, 999999))
        clnt = YunpianClient('71657fee075e49ecb6dea561fd321283')
        if not country_code or country_code == '+86':
            param = {YC.MOBILE: parsed_args['mobile'],
                     YC.TEXT: '【王文亮】您正在使用腾达，验证码：{}。请勿向任何人包括客服提供验证码。'.format(code)}

        else:
            param = {YC.MOBILE: country_code + parsed_args['mobile'],
                     YC.TEXT: "【USDTex】Your verification code is:{}. Please don't leak it to anyone else.".format(code)}
        result = clnt.sms().single_send(param)
        if result.code() != 0:
            abort(400, code=1004, message={'err': result._msg})

        pin_code = SmsPinCode.query.get(parsed_args['mobile'])
        if pin_code is None:
            pin_code = SmsPinCode(id=parsed_args['mobile'])
        pin_code.generate_signature(code)

        return {}
