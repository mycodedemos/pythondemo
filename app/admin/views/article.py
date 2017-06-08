#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''article views'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from flask import Blueprint
from flask import render_template

article_admin_bp = Blueprint('article', __name__)


@article_admin_bp.route('/article', methods=['GET'])
def article():
    '''生成任务'''
    return render_template('index.html')
