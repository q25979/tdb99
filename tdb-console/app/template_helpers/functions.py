# -*- coding: utf-8 -*-
import jinja2
from flask import current_app, request
from flask import session


def register(app):
    jinja_globals = app.jinja_env.globals
    jinja_globals['include_file'] = include_file(app.jinja_env)
    jinja_globals['has_permission'] = has_permission
    jinja_globals['format_sku'] = format_sku


def include_file(env):
    loader = env.loader

    def func(name):
        return jinja2.Markup(loader.get_source(env, name)[0])

    return func


def has_permission(code):
    access_function = session.get('access_function')
    if not access_function:
        return False
    return code in access_function.get(request.blueprint)


def format_sku(sku_id, sku_items, sku_meta):
    sku_descriptions = []
    default_variant_option = current_app.config['DEFAULT_VARIANT_OPTION']
    for item in sku_items:
        if sku_id == item['id']:
            sku_meta_dict = {}
            for meta in sku_meta:
                for option in meta['options']:
                    sku_meta_dict[option['id']] = option['description'] or ''
            sku_descriptions = [sku_meta_dict[option_id]
                                for option_id in item['variant_options'] if option_id != default_variant_option]
        return u','.join(sku_descriptions)
