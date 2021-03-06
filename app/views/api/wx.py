#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''views'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of pythondemo (2017)."

from app.config import app
from app.common.third.wx import MediaPlatform
from app.common.decorator import response_xml
from app.models import Config
from app.models import User
from app.models import UserThird
from app.models import Event
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

        # 记录用户行为
        third = UserThird.create_if_not_exist(id=msg.sender_id)
        print('sss')
        if not third.user_id:
            user = User.create(id=User.generate_id())
            third.user_id = user.id
            third.update_self()

        Event.create(user_id=third.user_id, ext=msg.msg)

        if msg.is_text():
            if msg.content == '1':
                return msg.reply_text(
                    Config.query_item(name='wx_reply').ext['subscribe']['zh'])
            elif msg.content == '2':
                n1 = msg.New('t1',
                             'http://vegoplus.s3-website-us-west-2.amazonaws.com/B321/0.jpg',
                             'http://baidu.com')
                return msg.reply_news(news=[n1.to_dict(), n1.to_dict()])
        elif msg.is_event():
            if msg.event == msg.Event.subscribe.value:
                return msg.reply_text(
                    Config.query_item(name='wx_reply').ext['subscribe']['zh'])
        return msg.reply_text('hahah')
    return ""
