#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from app.models import TaskDaily
from app.models import Video
from app.models import VideoSource

import requests

if __name__ == '__main__':
    Video.create(id=Video.generate_id(), name='越狱 第二季')
    Video.create(id=Video.generate_id(), name='楚乔传')
    pass
