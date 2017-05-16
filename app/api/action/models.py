#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''image models'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from datetime import datetime

from app.config import db
from app.config import BaseConfig
from app.common.base import BaseModel


class Action(BaseModel, db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.VARCHAR, default="")
    ip = db.Column(db.VARCHAR, default="")
    action_type = db.Column(db.INT, default=BaseConfig.TYPE_ACTION_VIEW)
    item_id = db.Column(db.VARCHAR)
    item_type = db.Column(db.INT)
    is_del = db.Column(db.INT, default=0)
    create_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())

