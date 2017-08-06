#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''views'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of pythondemo (2017)."

from app.common.base import BaseResponse
from app.common.decorator import cross_domain
from flask import Blueprint
from flask import request

user_bp = Blueprint('user', __name__)


@user_bp.route('/user', methods=['POST'])
@cross_domain('*')
def user_create():
    print(request.remote_addr)
    return BaseResponse.return_success()
