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
        if msg.is_text():
            if msg.content == '1':
                return msg.reply_text('1')
            elif msg.content == '2':
                n1 = msg.New('t1',
                             'http://vegoplus.s3-website-us-west-2.amazonaws.com/B321/0.jpg',
                             'http://baidu.com')
                return msg.reply_news(news=[n1,n1])
        return msg.reply_text('hahah')
    return ""
