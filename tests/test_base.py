#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from app.models import TaskDaily
from app.common.base import BaseObject
from app.common.base import BaseResponse
from app.common.base import BaseDict

import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_base_reponse(self):
        res = BaseResponse()

        self.assertEqual(res.to_dict(), dict(
            data={},
            status=200,
            message="",
            version=res.version
        ))

    def test_base_dict(self):
        d = dict(id=12, name="win", money=12.3, is_man=True,
                 user=dict(id=13, name="shining", age=25))
        self.assertEqual(BaseDict(d).filter('is_man', 'name'),
                         dict(is_man=True, name="win"))
        self.assertEqual(BaseDict(d).filter(source_include=['is_man', 'name']),
                         dict(is_man=True, name="win"))

        self.assertEqual(
            BaseDict(d).filter(source_exclude=['id', 'money', 'user']),
            dict(is_man=True, name="win"))

        self.assertEqual(BaseDict(d).filter('id', 'user[id,name]'),
                         dict(id=12, user=dict(id=13, name="shining")))

        self.assertEqual(BaseDict(d).filter('id', 'user[id,name]'),
                         dict(id=12, user=dict(id=13, name="shining")))

        ds = dict(id=12, users=[dict(id=1, name="a"), dict(id=2, name="b")])

        self.assertEqual(BaseDict(ds).filter('users[id]'),
                         dict(users=[dict(id=1), dict(id=2)]))


if __name__ == '__main__':
    unittest.main()
