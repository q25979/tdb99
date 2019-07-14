# -*- coding: utf-8 -*-
from flask import redirect, session, url_for, request, jsonify
from app import create_app
from app.views import ApiError

app = create_app()

without_auth_endpoint = ['home.login', 'static', 'home.captcha', 'home.index', 'upload.product_image']


@app.before_request
def make_session_permanent():
    session.permanent = True
    if request.endpoint in without_auth_endpoint or session.get('role') == 1:
        return
    elif not session.get('token') or request.blueprint not in session['permission']:
        return redirect(url_for('home.login'))


@app.errorhandler(401)
def unauthorized(error):
    session.pop('access_function', None)
    session.pop('token', None)
    session.pop('id', None)
    if is_ajax_request():
        return jsonify({
            'redirect': url_for('home.login'),
        }), 401
    return redirect(url_for('home.login'))


def is_ajax_request():
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


@app.errorhandler(ApiError)
def api_error(error):
    if is_ajax_request():
        return error.to_json(), 400
    raise error


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5006)
