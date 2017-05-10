#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from sqlalchemy.ext.declarative import DeclarativeMeta
from uuid import UUID
from datetime import datetime, date
from flask import make_response
from flask import jsonify

import json
import pymysql.cursors
import time

from app.config import app
from app.config import db
from app.config import env_config
from app.config import snowflake
from app.common.security import AESecurity
from urllib.parse import urlparse

URL_CONFIG = urlparse(env_config.SQLALCHEMY_DATABASE_URI)


class BaseModel(object):
    """
    SQLAlchemy JSON serialization
    """
    RELATIONSHIPS_TO_DICT = False
    __tablename__ = None

    def __iter__(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)
            if isinstance(x, date):
                return x.isoformat()

        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)

    @classmethod
    def generate_id(cls):
        """生成id"""
        table_name = cls.__tablename__
        return 'A{}'.format(snowflake.generate())

    @classmethod
    def create(cls, **params):
        item = cls(**params)
        db.session.add(item)
        db.session.commit()
        return item

    @classmethod
    def query_item(cls, **params):
        if not params:
            params = {}
        params['is_available'] = 1
        return cls.query.filter_by(**params).first()

    @classmethod
    def query_items(cls, **params):
        if not params:
            params = {}
        params['is_available'] = 1
        return cls.query.filter_by(**params).all()

    @classmethod
    def query_count(cls, **params):
        if not params:
            params = {}
        params['is_available'] = 1
        return cls.query.filter_by(**params).count()

    @classmethod
    def delete(cls, **params):
        if not params:
            params = {}
        params['is_available'] = 1
        item = cls.query.filter_by(**params).first()
        item.is_available = 0
        return item


class BaseDB():
    @classmethod
    def create_conn(cls):
        '''创建mysql链接'''
        return pymysql.connect(
            host=URL_CONFIG.hostname,
            port=URL_CONFIG.port,
            user=URL_CONFIG.username,
            password=URL_CONFIG.password,
            db=URL_CONFIG.path[1:],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    @classmethod
    def query(cls, sql, params):
        """
        查询操作
        :param sql:
        :param params:
        :return:
        """
        conn = cls.create_conn()
        try:
            cursor = conn.cursor()

            cursor.execute(sql, params)
            conn.commit()
            result = cursor.fetchall()
            cursor.close()
            return result
        except BaseException as e:
            app.logger.error(e)
            return []
        finally:
            conn.close()

    @classmethod
    def execute(cls, sql, params):
        """
        更新操作
        :param sql:
        :param params:
        :return:
        """
        conn = cls.create_conn()
        try:
            cursor = conn.cursor()

            result = cursor.execute(sql, params)
            conn.commit()
            cursor.close()
            return result
        except BaseException as e:
            app.logger.error(e)
            return False
        finally:
            conn.close()


class BaseResponse(BaseModel):
    data = {}
    status = 200
    message = ""
    version = 0

    def __init__(self, data={}, status=200, message=""):
        self.data = data
        self.status = status
        self.message = message,
        self.version = int(time.time())

    def to_dict(self, rel=None, backref=None):
        item = self.__dict__
        item['message'] = item['message'][0]
        return item

    @classmethod
    def return_response(cls, data={}, status=200, message="", headers={}):
        res = cls(
            data=data,
            status=status,
            message=message
        ).to_dict()
        return make_response(jsonify(res), status, headers)

    @classmethod
    def return_success(cls, data={}):
        return cls.return_response(data)

    @classmethod
    def return_error(cls, status, message):
        return cls.return_response(status=status, message=message)

    @classmethod
    def return_internal_server_error(cls, message='Internal Server Error'):
        return cls.return_response(status=500, message=message)

    @classmethod
    def return_unauthorized(cls, message='Unauthorized'):
        return cls.return_response(status=401, message=message)

    @classmethod
    def return_not_found(cls, message='Not Found'):
        return cls.return_response(status=404, message=message)

    @classmethod
    def return_forbidden(cls, message='Forbidden'):
        return cls.return_response(status=403, message=message)

    @classmethod
    def make_paginate(cls, data, total, page, per_page):
        """
        生成返回数据
        :param list:
        :param total_size:
        :param page:
        :param size:
        :return:
        """
        total_page = total / per_page
        yu = total % per_page
        if yu > 0:
            total_page += 1

        res = {
            "items": data,
            "page": int(page),
            "total": total,
            "total_pages": total_page,
            "per_page": per_page
        }
        return res


class UserSecurity():
    KEY = 'b8d4471654c7330c'
    aes = AESecurity(KEY)

    @classmethod
    def generate_authorization(cls, user_id, **params):
        '''用户id加密'''
        data = '{};{}'.format(user_id, int(time.time()))
        return cls.aes.encrypt(data)

    @classmethod
    def get_user_id(cls, authorization):
        '''从加密信息中过去用户'''
        try:
            if not authorization or authorization == 'null':
                return None
            data = cls.aes.decrypt(authorization)
            return data.split(';')[0]
        except BaseException as e:
            app.logger.error(e)
            return None


if __name__ == '__main__':
    id = BaseModel.generate_id()
    token = UserSecurity.generate_authorization(id)
    print(token)
    print(UserSecurity.get_user_id(token))
