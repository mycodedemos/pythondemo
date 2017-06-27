#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''views'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of pythondemo (2017)."

from app.models import Task
from app.models import Article
from app.common.base import BaseResponse
from app.common.base import BaseRequest
from flask import Blueprint
from flask import render_template

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    '''首页'''
    return render_template('admin/index.html',
                           task=Task.query_item(id='A547908256530434'),
                           tasks=Task.query_items())


@index_bp.route('/article/edit.html')
def article_edit_html():
    '''文章修改页面'''
    id = BaseRequest.get_args().get('id')
    print(id)
    return render_template('admin/pages/article/edit.html',
                           item=Article.query_item(id=id))


@index_bp.route('/article/list.html')
def article_list_html():
    '''文章列表'''
    return render_template('admin/pages/article/list.html')


@index_bp.route('/article/edit.json', methods=['post'])
def article_edit_json():
    '''修改接口'''
    args = BaseRequest.get_args()
    print(args)

    if 'id' in args:
        Article.update_by_id(**args)
    else:
        args['id'] = Article.generate_id()
        Article.create(**args)

    return BaseResponse.return_success()


@index_bp.route('/article/list.json', methods=['get'])
def article_list_json():
    '''文章列表接口'''
    args = BaseRequest.get_args()
    page = args.get('page', 1, int)
    per_page = args.get('per_page', 10, int)

    paginate = Article.query_paginate(page, per_page)
    res = BaseResponse.make_paginate(
        [item.to_dict() for item in paginate.items], paginate.total, page,
        per_page)

    return BaseResponse.return_success(res)

