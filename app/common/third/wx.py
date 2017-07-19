#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""wx 工具类"""

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of pythondemo (2017)."

from app.config import app
from app.config import BaseConfig
from datetime import datetime
from enum import Enum

import requests
import xmltodict
import json


class Action(Enum):
    token = 'token'
    user_get = 'user/get'
    user_info = 'user/info'
    shorturl = 'shorturl'


class MediaPlatform():
    def __init__(self, app_id=BaseConfig.WX_MP_APP_ID,
                 app_secret=BaseConfig.WX_MP_APP_SECRET):
        self.app_id = app_id
        self.app_secret = app_secret
        self.origin_url = 'https://api.weixin.qq.com/cgi-bin/{}'
        self.id = BaseConfig.WX_MP_ID

    def get_access_token(self):
        """获取access_token
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140183
        """
        return self._get(Action.token.value, grant_type='client_credential',
                         **self._auth_args())

    def get_users(self, access_token, next_openid=None):
        """
        公众号可通过本接口来获取帐号的关注者列表，关注者列表由一串OpenID
        （加密后的微信号，每个用户对每个公众号的OpenID是唯一的）组成。
        一次拉取调用最多拉取10000个关注者的OpenID，可以通过多次拉取的方式来满足需求。
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140840
        :param open_id:
        :param access_token:
        :return:
        """
        return self._get(Action.user_get.value, access_token=access_token,
                         next_openid=next_openid)

    def get_user_info(self, access_token, openid, lang=None):
        return self._get(Action.user_info.value, access_token=access_token,
                         openid=openid, lang=lang)

    def generator_short_url(self, access_token, long_url):
        """
        将一条长链接转成短链接。
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1443433600
        :param access_token:
        :param long_url:
        :return:
        """
        return self._post(Action.shorturl.value, action='long2short',
                          access_token=access_token, long_url=long_url)

    def _auth_args(self):
        return {'appid': self.app_id, 'secret': self.app_secret}

    def _get(self, _action, **kwargs):
        url = self.origin_url.format(_action)
        res = requests.get(url, params=kwargs)
        self._print_res(res.json())
        return res.json()

    def _post(self, _action, **kwargs):
        url = self.origin_url.format(_action)
        url = '{}?access_token={}'.format(url, kwargs.get('access_token'))
        print(url)
        kwargs.pop('access_token')
        res = requests.post(url, json=kwargs)
        self._print_res(res.json())
        return res.json()

    def _print_res(self, res):
        """打印结果"""
        if 'errcode' in res:
            app.logger.error(res)

    class Message():
        class MsgType(Enum):
            text = 'text'
            news = 'news'

        def __init__(self, xml_input):
            data = json.loads(json.dumps(xmltodict.parse(xml_input)))['xml']
            self.owner_id = data['ToUserName']
            self.sender_id = data['FromUserName']
            self.msg_type = data['MsgType']
            self.content = data['Content']
            self.msg_id = data['MsgId']

        def is_text(self):
            return self.msg_type == self.MsgType.text.value

        def reply_text(self, content):
            return self._generator_reply(content)

        def _generator_reply(self, *args, **kwargs):
            content = args[0] if args else kwargs.get('content')
            msg_type = kwargs.get('msg_type') or self.MsgType.text.value

            xml = dict(
                ToUserName=self.sender_id,
                FromUserName=self.owner_id,
                CreateTime=int(datetime.now().timestamp()),
                MsgType=msg_type
            )

            if msg_type == self.MsgType.text.value:
                xml['Content'] = content

            return xmltodict.unparse({"xml": xml})
