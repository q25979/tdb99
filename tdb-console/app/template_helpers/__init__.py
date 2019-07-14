# -*- coding: utf-8 -*-


def init(app):
    register_filters(app)
    register_globals(app)


def register_globals(app):
    from . import functions

    functions.register(app)


def register_filters(app):
    from . import converters, utils
    filters = app.jinja_env.filters
    converters.register(app, filters)
    utils.register(app, filters)
