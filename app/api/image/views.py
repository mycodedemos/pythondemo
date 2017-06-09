#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''支持接口'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."


from app.config import app
from app.config import BaseConfig
from app.common.base import BaseResponse
from app.common.base import BaseRequest
from app.common.decorator import jsonp
from app.models import Image
from app.models import Action

from flask import request
from flask import Blueprint
from flask import g

image_bp = Blueprint('image', __name__)


@image_bp.route('/image', methods=['GET'])
@jsonp
def image_list():
    '''图片列表'''
    args = request.args
    page = BaseRequest.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = BaseRequest.get_param_int(args, 'per_page',
                                         BaseConfig.DEFAULT_PER_PAGE)
    paginate = Image.query_paginate(
        page=page,
        per_page=per_page
    )

    items = [item.to_dict() for item in paginate.items]

    try:
        for item in items:
            Action.create(
                ip=g.ip,
                item_id=item['id'],
                item_type=BaseConfig.TYPE_ITEM_IMAGE
            )
    except BaseException as e:
        app.logger.error(e)
    res = BaseResponse.make_paginate(items, paginate.total, page, per_page)

    return BaseResponse.return_success(res)
