#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''image models'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from datetime import datetime

from app.config import db
from app.common.base import BaseModel


class Image(BaseModel, db.Model):
    id = db.Column(db.VARCHAR, primary_key=True)
    third_id = db.Column(db.VARCHAR, default="")
    source = db.Column(db.VARCHAR, default="juhe")
    content = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    length = db.Column(db.BIGINT, default=0)
    md5 = db.Column(db.VARCHAR, default="")
    publish_ts = db.Column(db.BIGINT, default=0)
    is_del = db.Column(db.INT, default=0)
    create_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())
    update_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())

    @classmethod
    def update_by_id(cls, id, **params):
        item = cls.query.filter_by(id=id, is_del=0).first()
        item.md5 = params.get('md5', item.md5)
        item.is_del = params.get('is_del', item.is_del)
        item.length = params.get('length', item.length)
        db.session.commit()
        return item
