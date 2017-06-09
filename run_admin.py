#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''配置信息'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from app.api.image.views import image_bp
from app.api.support.views import support_bp
from app.api.task.views import task_bp
from app.common.base import BaseRequest
from app.common.base import BaseResponse
from app.common.base import UserSecurity
from app.config import BaseConfig
from app.run import app
from app.views.admin import index_bp
from flask import g
from flask import request
import time


@app.before_request
def before_request():
    g.request_start_time = time.time()
    app.logger.debug(
        '{} {}\nargs:{}\nheaders:{}'.format(
            request.method, request.url, BaseRequest.get_args(), request.headers
        )
    )

    g.user_id = get_login_user_id()
    g.user = None

    # ip
    g.ip = request.remote_addr


@app.after_request
def after_request(response):
    if not hasattr(g, 'request_start_time'):
        return response
    elapsed = time.time() - g.request_start_time
    # elapsed = int(round(1000 * elapsed))
    app.logger.debug('{} begin request {} {} cast {} s'.format(
        g.request_start_time, request.method, request.url, elapsed
    ))

    return response


@app.errorhandler(Exception)
def app_error_handler(e):
    app.logger.error(e)
    return BaseResponse.return_internal_server_error(str(e))


def get_login_user_id():
    '''从request中过去user_id'''
    headers = request.headers

    callback = request.args.get('callback', False)
    if callback:
        headers = request.cookies

    token = headers.get(BaseConfig.HEAD_AUTHORIZATION)
    if not token:
        return None
    # 获取用户id
    return UserSecurity.get_user_id(token)
# api
URL_PREFIX = BaseConfig.APPLICATION_ROOT
app.register_blueprint(support_bp)
app.register_blueprint(image_bp, url_prefix=URL_PREFIX)
app.register_blueprint(task_bp, url_prefix=URL_PREFIX)

# admin
URL_PREFIX = BaseConfig.APPLICATION_ROOT_ADMIN
app.register_blueprint(index_bp)
