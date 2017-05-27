#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from app.common.base import BaseModel
from app.common.security import Md5
from app.api.image.models import Image

import requests

if __name__ == '__main__':
    item = Image.query_item(id='A37286179892101129')
    print(item)
    pass
