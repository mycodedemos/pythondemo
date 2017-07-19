#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''views'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of pythondemo (2017)."

from app.config import app
from app.common.base import BaseResponse
from flask import Blueprint
from flask import request

wx_bp = Blueprint('wx', __name__)


@wx_bp.route('/wx/mp_callback')
def mp_callback():
    '''公众号回调地址'''
    app.logger.debug(request.remote_addr)
    app.logger.debug(request.method)
    app.logger.debug(request.args)
    app.logger.debug(request.json)
    app.logger.debug(request.form)
    app.logger.debug(request.data)
    if request.method == 'GET':
        return request.args.get('echostr', "success")

    return BaseResponse.return_success()
