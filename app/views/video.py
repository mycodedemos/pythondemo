#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''views'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from app.common.security import AESecurity
from app.models import VideoSource as VS
from app.models import Video
from flask import Blueprint
from flask import render_template
from flask import url_for

video_bp = Blueprint('video', __name__)

KEY = 'ab60373552d9daa6'


@video_bp.route('/')
def index():
    '''首页'''
    return render_template('www/index.html',
                           tags=[url_for('video.video_list')],
                           default_tag=url_for('video.video_list'))


@video_bp.route('/video/list.html')
def video_list():
    '''首页'''
    return render_template('www/video/list.html', items=Video.query_items())


@video_bp.route('/video/<string:id_secret>.html')
def video_detail(id_secret):
    '''视频详情'''
    print(id_secret)
    return render_template('www/video/detail.html')
