#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from app.common.base import BaseModel

if __name__ == '__main__':
    for i in range(0, 10):
        print(BaseModel.generate_id())
    pass
