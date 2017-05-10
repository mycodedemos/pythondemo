#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''支持接口'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys
import os

from app.common.base import BaseResponse

from flask import request
from flask import Blueprint
from flask import make_response
from flask import send_file

support_bp = Blueprint('support', __name__)


@support_bp.route('/test', methods=['GET', 'POST'])
def test():
    '''一级页面接口'''
    print(request.method)

    print(request.content_type)

    # application / x - www - form - urlencoded
    # application / x - www - form - urlencoded

    return BaseResponse.return_success(
        data={
            'form': request.form,
            'json': request.json
        }
    )
