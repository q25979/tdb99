# -*- coding: utf-8 -*-
import hashlib
import urlparse
from flask import current_app
from flask import url_for


def md5hex(data):
    if type(data) is unicode:
        data = data.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


def combine_flags(flags):
    value = 0
    for flag in flags:
        value |= flag
    return value


def split_flags(flag_value, all_flags):
    return [flag[0] for flag in all_flags if (flag[0] & flag_value) == flag[0]]


def extract_oss_key(image_url):
    cdn_url = urlparse.urlparse(current_app.config['OSS_CDN_URL'])
    url = urlparse.urlparse(image_url)
    if url.netloc == cdn_url.netloc or url.netloc == 'cdn.shidaiwl.cn':
        return url.path[1:]
    else:
        return image_url


def build_oss_url(image_key, schema=None):
    if not image_key:
        return image_key
    url = urlparse.urlparse(image_key)
    if url.netloc:
        return image_key
    else:
        url_str = urlparse.urljoin(current_app.config['OSS_CDN_URL'], image_key)
        if schema:
            parts = list(urlparse.urlsplit(url_str))
            parts[0] = schema
            url_str = urlparse.urlunsplit(parts)
        return url_str


def build_local_url(image_key):
    view_url = url_for('game.private_file', path='', file_name='')
    url_str = view_url[:view_url.rfind('/', 1) - 1] + image_key[image_key.find('/', 1):]
    return url_str


def extract_all_oss_key(target_dict, keys):
    for key in keys:
        field_value = target_dict.get(key)
        if not field_value:
            continue
        if isinstance(field_value, str) or isinstance(field_value, unicode):
            target_dict[key] = extract_oss_key(field_value)
        elif isinstance(field_value, list):
            target_dict[key] = [extract_oss_key(url) for url in field_value]
