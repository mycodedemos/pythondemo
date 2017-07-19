#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''views'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of pythondemo (2017)."

from app.config import app
from app.common.third.wx import MediaPlatform
from app.common.decorator import response_xml
from flask import Blueprint
from flask import request
from flask import make_response
import xmltodict
import json

wx_bp = Blueprint('wx', __name__)
mp = MediaPlatform()


@wx_bp.route('/wx/mp_callback', methods=['GET', 'POST'])
@response_xml
def mp_callback():
    '''公众号回调地址'''
    app.logger.debug(request.remote_addr)
    if request.method == 'GET':
        return request.args.get('echostr', "success")

    if request.method == 'POST':
        msg = mp.Message(request.data)

        return msg.reply_text('hahah')
    return ""
