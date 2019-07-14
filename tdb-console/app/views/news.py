# -*- coding: utf-8 -*-
import urllib2

import requests
from flask import Blueprint, jsonify
from flask import render_template
from flask import request
from flask_wtf import Form
from wtforms import HiddenField, StringField, TextAreaField
from wtforms.validators import DataRequired

from app.views import Api, ApiError, AppError
from app.views import upload
from app.views import utils
from app.views.admin import api_permission

news = Blueprint('news', __name__)
api_permission['news'] = ['/admin/news']


class NewsForm(Form):
    id = HiddenField('Id')
    title = StringField('title', validators=[DataRequired()])
    details = TextAreaField('details', validators=[DataRequired()])


@news.route('/')
def index():
    return render_template('news/news_list.html')


@news.route('/ajax/list', methods=['POST'])
def ajax_list():
    params = request.get_json()
    data = Api.get('/admin/news', params['query'])
    total_records = data['total_count']
    return_dict = {
        'draw': params['draw'],
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data['objects']
    }
    return jsonify(return_dict)


@news.route('/details', methods=['GET'])
@news.route('/details/<string:news_id>')
def details(news_id=None):
    form = NewsForm()
    if news_id:
        news_detail = Api.get('/admin/news/details/' + urllib2.quote(news_id))
        # if news_detail['details']:
        #     detail_url = news_detail['details']
        #     response = requests.get(utils.build_oss_url(detail_url, 'http'), timeout=(9, 9))
        #     response.encoding = 'utf-8'
        #     news_detail['details'] = response.text
        form.process(data=news_detail)
    return render_template('news/detail.html', form=form)


@news.route('/ajax/save', methods=['POST'])
def ajax_save():
    form = NewsForm()
    if form.validate():
        data = form.data
        news_id = data.pop('id')
        # detail_data = data['details']
        # details_hash = utils.md5hex(detail_data)
        # data['details'] = upload.put_oss('news/%s.html' % details_hash, detail_data)
        if news_id:
            result = Api.put('/admin/news/details/' + urllib2.quote(news_id), data)
        else:
            result = Api.post('/admin/news', data)
        return jsonify(result)
    else:
        raise ApiError(AppError.INVALID_REQUEST, form.errors)


@news.route('/<news_id>', methods=['DELETE'])
def news_delete(news_id):
    result = Api.delete('/admin/news/details/' + urllib2.quote(news_id))
    return jsonify(result)
