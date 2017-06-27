#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''配置信息'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from app.run import app
from app.views.article import article_bp
from app.views.video import video_bp


app.register_blueprint(article_bp)
app.register_blueprint(video_bp)
