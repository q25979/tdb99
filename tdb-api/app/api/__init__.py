# -*- coding: utf-8 -*-
import oss2
from flask import request, current_app
from flask_restful import Api, abort, reqparse, fields
from werkzeug import exceptions
import math

restful_api = Api()


class AddResource:
    def __init__(self, restful_api):
        self.restful_api = restful_api

    def add_resource(self, url=''):
        def wrap(cls):
            self.restful_api.add_resource(cls, url)
            return cls

        return wrap


def patch_requests_response(r):
    if r.encoding is None or r.encoding == 'ISO-8859-1':
        r.encoding = 'UTF-8'


def pagination_calc_page(per_page, page, count):
    if per_page <= 0:
        abort(400, code=1000, message={'per_page': 'per_page must greater than 0'})
    record_count = count
    if record_count == 0:
        record_count = 1
    total_pages = int(math.ceil(record_count / float(per_page)))
    if page <= 0:
        page = total_pages
    return page, total_pages


def pagination_query(per_page, page, query):
    """
    转换为分页结果
    :param per_page: per page count
    :param page: page index
    :param query: query
    :return:
    """
    count = query.count()
    page, total_pages = pagination_calc_page(per_page, page, count)
    pagination = query.paginate(page, per_page, False)
    return {
        'total_pages': total_pages,
        'page': page,
        'per_page': per_page,
        'total_count': pagination.total,
        'objects': pagination.items
    }


class CustomRequestParser(reqparse.RequestParser):
    def parse_args(self, req=None, strict=False):
        """Parse all arguments from the provided request and return the results
        as a Namespace

        :param strict: if req includes args not in parser, throw 400 BadRequest exception
        """
        if req is None:
            req = request

        namespace = self.namespace_class()

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                namespace[arg.dest or arg.name] = value
        if errors:
            abort(400, code=1000, message=errors)

        if strict and req.unparsed_arguments:
            raise exceptions.BadRequest('Unknown arguments: %s'
                                        % ', '.join(req.unparsed_arguments.keys()))

        return namespace


class FakeRequest(dict):
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)


class UrlNormalize(fields.Raw):
    def format(self, value):
        if not value:
            return ''
        elif value.startswith('http://'):
            return value
        else:
            return current_app.config['OSS_BUCKET_CDN'] + value


def oss_bucket(create=False):
    auth = oss2.Auth(current_app.config['ALIYUN_ACCESS_KEY_ID'], current_app.config['ALIYUN_ACCESS_KEY_SECRET'])
    bucket = oss2.Bucket(auth, current_app.config['OSS_ENDPOINT'], current_app.config['OSS_BUCKET'])
    if create:
        bucket.create_bucket(oss2.models.BUCKET_ACL_PUBLIC_READ)
    return bucket


def oss_proof_img_key(name):
    return current_app.config['OSS_ROOT'] + 'image/' + name
