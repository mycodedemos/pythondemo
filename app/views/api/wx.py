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
                return msg.reply_news(news=[n1.to_dict(), n1.to_dict()])
        elif msg.is_event():
            if msg.event == msg.Event.subscribe.value:
                return msg.reply_text('等你好久了~\n\n“我们”【好看】【好玩】\n'
                                      '“你们”【好吃】！\n\n“美未智能屏”期待着'
                                      '您的了解与加入！\n快来吧~(づ￣ 3￣)づ\n\n'
                                      '详情点击：<a href="http://uu3ann.epub360.cn/v2/manage/book/y1b3je/">致海外餐厅老板</a>')
        return msg.reply_text('hahah')
    return ""
