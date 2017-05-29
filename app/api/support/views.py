#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''支持接口'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys
import os

from app.common.base import BaseResponse
from app.common.decorator import args_required
from app.common.decorator import headers_required

from flask import request
from flask import Blueprint
from flask import make_response
from flask import send_file

support_bp = Blueprint('support', __name__)


@support_bp.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
@args_required('id', 'name')
@headers_required('version')
def test():
    '''一级页面接口'''
    print(request.method)

    print(request.content_type)

    # application / x - www - form - urlencoded
    # application / x - www - form - urlencoded
    res = {
        'form': request.form,
        'json': request.json
    }
    return BaseResponse.return_success(res)


@support_bp.route('/download', methods=['GET'])
def down():
    '''下载'''
    res = make_response(send_file('/static/apple-app-site-association'))
    return res
