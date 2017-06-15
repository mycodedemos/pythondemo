#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from app.models import TaskDaily
from app.common.base import BaseObject


class Person(BaseObject):
    id = 0
    name = ""


if __name__ == '__main__':

    p = Person(id=3)
    print(p.id)
    pass
