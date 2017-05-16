#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''配置信息'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import os
import time
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string
from werkzeug.contrib.fixers import ProxyFix

from app.common.id import Snowflake

CONFIG_NAME_MAPPER = {
    'local': 'app.local_config.LocalConfig',
    'product': 'app.local_config.ProductionConfig',
    'dev': 'app.local_config.DevelopmentConfig',
    'test': 'app.local_config.TestingConfig'
}


class BaseConfig(object):
    DEBUG = False

    ES_INDEX = 'hopapapa'

    ES_TYPE_USER = 'user'
    ES_TYPE_VIDEO = 'video'
    ES_TYPE_ARTICLE = 'article'
    ES_TYPE_AUDIO = 'audio'
    ES_TYPE_COLLECTION = 'collection'

    ES_PARAMS_WEIGHT = 'es_weight'

    ES_WEIGHT_USER = 10000
    ES_WEIGHT_COLLECTION = 9000
    ES_WEIGHT_VIDEO = 8000
    ES_WEIGHT_AUDIO = 8000
    ES_WEIGHT_ARTICLE = 7000

    TYPE_ITEM_USER = 1
    TYPE_ITEM_IMAGE = 2
    TYPE_ACTION_VIEW = 21

    TYPE_DEL = 1
    TYPE_UNDEL = 0

    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 10
    DEFAULT_NO_PAGINATE_PER_PAGE = 10000
    DEFAULT_AGE = 18
    DEFAULT_GENDER = 0
    DEFAULT_IS_DEL = 0
    DEFAULT_PORTRAIT = 'http://pic.hopapapa.com/static/Mask@2x.png'

    ARTICLE_HTML_URL_FORMAT = 'http://www.hopapapa.com/fabu/news.html?id={}'

    MAX_START = 4638873600

    HEAD_AUTHORIZATION = 'authorization'

    TIMESTAMP_FORMAT_SQL = "%Y-%m-%dT%H:%M:%S"

    ALIYUN_APP_KEY = 'LTAIju7LLMDLbHFx'
    ALIYUN_APP_SECRET = 't4KwSvtg3Wzg9r1HuCpRZkzplGOshD'
    ALIYUN_BUCKET_FILE = 'file-hopapapa-com'
    ALIYUN_BUCKET_IMG = 'img-hopapapa-com'
    ALIYUN_BUCKET_PIC = 'pic-hopapapa-com'

    ALIYUN_IMAGE_SUFFIX_X400PX = '?x-oss-process=image/resize,m_lfit,w_400,limit_0/auto-orient,0/quality,q_90'
    ALIYUN_IMAGE_SUFFIX_X100PX = '?x-oss-process=image/resize,m_lfit,w_100,limit_0/auto-orient,0/quality,q_90'

    CODE_TEMPLATE_ID1 = '3061150'  # 您的验证码为：%s，10分钟有效，打死都不要告诉别人哦。

    # 输出日志文件
    METRICS_LOG_FILE = './metrics.flask.log'
    # 地址前缀
    APPLICATION_ROOT = '/api/v1'
    APPLICATION_ROOT_ADMIN = '/admin/v1'

    LETV_USER_UNIQUE = 'n219pmijzi'
    LETV_KEY_SECRET = '903a9e5bb69205153cab2d5648ceb151'
    LETV_VIDEO_API_URL = 'http://api.letvcloud.com/open.php'

    BAIDU_MAP_AK = 'yeFdiSFZ0fm9CS7iTfEcbHkcBLVhSgRE'

    UMENG_KEY = '58fc8647c62dca72ec001abe'
    UMENG_SECRET = '8gvb4jjymhe9gvpsrppk8a1rpaiz4qps'
    # UMENG_KEY = '58fc7ea94544cb4e4200099d'
    # UMENG_SECRET = 'pnbiq4kukmhadesq052tdi7zjfeeu1xw'

    WANGYI_APP_KEY = '7111da94518f669569422abc553bcd6e'
    WANGYI_APP_SECRET = 'ce35762de9ce'


    # 401   没有权限
    # 403   无法执行操作


def create_app(flask_config_name=None):
    """
    创建配置
    :return:
    """
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    env_flask_config_name = os.getenv('FLASK_CONFIG')
    config_mapper_name = flask_config_name or env_flask_config_name or 'local'
    config_name = CONFIG_NAME_MAPPER[config_mapper_name]
    app.config.from_object(config_name)
    print('-------------------------init app-------------------------')
    logging.basicConfig(filename=app.config['METRICS_LOG_FILE'],
                        level=logging.ERROR)
    return app


app = create_app()
db = SQLAlchemy(app)
snowflake = Snowflake(0)
