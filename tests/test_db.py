#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from app.common.base import BaseModel
from app.common.base import BaseDict
from app.common.security import Md5
from app.api.image.models import Image
from app.api.task.models import Task
from app.api.task.models import TaskDaily

import requests

if __name__ == '__main__':
    #
    # Task.create(
    #     id=Task.generate_id(),
    #     end_day='2017-05-05'
    # )

    item = TaskDaily.query_item(id=1)
    print(item.to_dict(rel=True).filter('id','create_ts'))
    pass
