# -*- coding: utf-8 -*-
import StringIO
import hashlib

import oss2 as oss2
from PIL import Image
from flask import Blueprint, jsonify, request, current_app

from app.views import utils

upload = Blueprint('upload', __name__)


@upload.route('/image/<path>', methods=['POST'])
@upload.route('/product/image', methods=['POST'])
def product_image(path=None):
    if path is None:
        path = 'game'
    resp = {'success': False, 'message': 'no image'}
    if 'image' in request.files:
        resp = __upload_image(request.files['image'], path)
    return jsonify(resp)


def __upload_image(image_file, path, private=False):
    resp = {'success': False}
    temp_buffer = StringIO.StringIO()
    try:
        image_format = __convert_image(image_file, temp_buffer)
        image_bytes = temp_buffer.getvalue()
        md5 = hashlib.md5()
        md5.update(image_bytes)
        image_hash = md5.hexdigest()
        filename = '%s.%s' % (image_hash, image_format)
        if path[-1] == '/':
            path += filename
        else:
            path += '/' + filename
        if private:
            resp['url'] = utils.build_local_url(put_oss(path, image_bytes, True))
        else:
            resp['url'] = utils.build_oss_url(put_oss(path, image_bytes), 'http')
        resp['success'] = True
    except (KeyError, IOError):
        resp['message'] = 'process image error'
    finally:
        temp_buffer.close()
    return resp


def put_oss(path, data, private=False):
    auth = oss2.Auth(current_app.config['ALIYUN_ACCESS_KEY_ID'], current_app.config['ALIYUN_ACCESS_KEY_SECRET'])
    bucket = oss2.Bucket(auth, current_app.config['OSS_ENDPOINT'], current_app.config['OSS_BUCKET'])
    root_path = current_app.config['OSS_ROOT']
    if private:
        bucket = oss2.Bucket(auth, current_app.config['OSS_ENDPOINT'], current_app.config['OSS_BUCKET_PRIVATE'])
        root_path = current_app.config['OSS_ROOT_PRIVATE']
    if root_path[:1] == '/':
        root_path = root_path[1:]
    if root_path[-1] == '/':
        root_path = root_path[0:len(root_path) - 1]
    path = root_path + (path if path[:1] == '/' else '/' + path)
    result = bucket.put_object(path, data)
    if result.status != 200:
        raise IOError(result.details['Message'])
    return path


def get_oss(path, file_name, private=False):
    auth = oss2.Auth(current_app.config['ALIYUN_ACCESS_KEY_ID'], current_app.config['ALIYUN_ACCESS_KEY_SECRET'])
    bucket = oss2.Bucket(auth, current_app.config['OSS_ENDPOINT'], current_app.config['OSS_BUCKET'])
    root_path = current_app.config['OSS_ROOT']
    if private:
        bucket = oss2.Bucket(auth, current_app.config['OSS_ENDPOINT'], current_app.config['OSS_BUCKET_PRIVATE'])
        root_path = current_app.config['OSS_ROOT_PRIVATE']
    if root_path[:1] == '/':
        root_path = root_path[1:]
    if root_path[-1] == '/':
        root_path = root_path[0:len(root_path) - 1]

    path = root_path + (path if path[:1] == '/' else '/' + path) + (
        file_name if file_name[:1] == '/' else '/' + file_name)

    result = bucket.get_object(path)
    if result.status != 200:
        raise IOError(result.details['Message'])
    return result.read()


def __convert_image(input_stream, output_stream):
    image = Image.open(input_stream)
    try:
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            image.save(output_stream, 'PNG')
            return 'png'
        elif image.format == 'GIF':
            image.save(output_stream, 'GIF')
            return 'gif'
        else:
            image.save(output_stream, 'JPEG')
            return 'jpg'
    finally:
        image.close()
