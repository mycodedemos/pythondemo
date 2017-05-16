#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from app.common.base import BaseModel
from app.common.security import Md5

import requests

if __name__ == '__main__':
    # for i in range(0, 10):
    #     print(BaseModel.generate_id())

    # res = requests.get(
    #     'http://juheimg.oss-cn-hangzhou.aliyuncs.com/joke/201608/12/96684803CA746F454BBF3509C8FF5FBF.gif')
    # print(type(res.rea))

    print(Md5.encrypt_by_url(
        'http://juheimg.oss-cn-hangzhou.aliyuncs.com/joke/201608/12/96684803CA746F454BBF3509C8FF5FBF.gif'))
    print(
        Md5.encrypt_by_file('/Users/wxnacy/PycharmProjects/pythondemo/run.py'))
    pass
