#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from flask import g
from flask import request

from app.config import app
from app.config import BaseConfig
from app.common.base import UserSecurity
from app.api.support.views import support_bp


@app.before_request
def before_request():
    g.request_start_time = time.time()
    app.logger.debug(
        '{} {}\nargs:{}\nheaders:{}'.format(
            request.method, request.url, request.args, request.headers
        )
    )

    g.user_id = get_login_user_id()
    g.user = None


@app.after_request
def after_request(response):
    if not hasattr(g, 'request_start_time'):
        return response
    elapsed = time.time() - g.request_start_time
    elapsed = int(round(1000 * elapsed))
    req_info = str(
        g.request_start_time) + "_" + request.method + "_" + request.url
    app.logger.debug(req_info + ":" + str(elapsed))

    return response


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


URL_PREFIX = BaseConfig.APPLICATION_ROOT
app.register_blueprint(support_bp)
