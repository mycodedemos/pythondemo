#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''views'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of pythondemo (2017)."

from app.config import app
from app.common.base import BaseResponse
from flask import Blueprint
from flask import request
import hashlib

wx_bp = Blueprint('wx', __name__)


@wx_bp.route('/wx/mp_callback')
def mp_callback():
    '''公众号回调地址'''

    # ([('signature', '9d22b7bfcc46bceb77e362eba295ab79355cf139'),
    #   ('timestamp', '1500452603'), ('echostr', '12831846290135416827'),
    #   ('nonce', '3889653278')])

    if request.method == 'GET':
        return request.args.get('echostr')
    app.logger.debug(request.args)
    app.logger.debug(request.json)
    app.logger.debug(request.form)

    timestamp = '1500452603'
    echostr = '12831846290135416827'
    signature = '9d22b7bfcc46bceb77e362eba295ab79355cf139'
    nonce = '3889653278'
    token = 'F3uIXPvYZ8nmpPVhazFkert'
    list = [token, timestamp, nonce,'F3uIXPvYZ8nmpPVhazFkertj25fry8OcINM87xRe4kg']
    list.sort()

    sha1 = hashlib.sha1()
    # map(sha1.update, list)
    sha1.update("".join(list))
    hashcode = sha1.hexdigest()
    app.logger.debug(hashcode)

    return ''
