#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''支持接口'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys
import os

from app.common.base import BaseResponse
from app.common.decorator import args_required
from app.common.decorator import headers_required

from flask import request
from flask import Blueprint
from flask import make_response
from flask import send_file
from flask import render_template

support_bp = Blueprint('support', __name__)


@support_bp.route('/test.html')
def test():
    md = """
    ```
<dependency>
	<groupId>net.easyjava</groupId>
	<artifactId>easyjava-tools</artifactId>
	<version>[1.0.0,2.0.0]</version>
</dependency>
```
    """
    return render_template('test.html', md=md)


@support_bp.route('/download', methods=['GET'])
def down():
    '''下载'''
    res = make_response(send_file('/static/apple-app-site-association'))
    return res
