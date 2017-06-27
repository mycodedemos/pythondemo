#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from app.common.aliyun import OSSClient
from app.common.base import BaseResponse
from app.common import utils
from app.models import Article

from datetime import date
from datetime import datetime
import json
import requests
import unittest
import os
import webbrowser

BUCKET = 'file-easyjava-net'


class AliyunTestCase(unittest.TestCase):
    def setUp(self):
        self.oss = OSSClient()
        pass

    def tearDown(self):
        pass

    def test_put_object(self):
        key = 'test/{}/{}.json'.format(date.today().isoformat(),
                                       datetime.utcnow().timestamp())
        data = dict(id=12, name='win')
        url = self.oss.put_object(BUCKET, key, json.dumps(data))
        print(url)
        res = requests.get(url)
        self.assertEqual(data, res.json())

        url = self.oss.put_object(BUCKET, key, requests.get(url))
        print(url)
        res = requests.get(url)
        self.assertEqual(data, res.json())
        url = self.oss.put_object(BUCKET, key, open(
            '{}/app/static/temp/hsybs.json'.format(os.getcwd()), 'rb'))
        print(url)
        res = requests.get(url)
        self.assertEqual(data, res.json())
        print(os.getcwd())

    def test_make_api(self):
        item = Article.query_item(id=1)
        data = BaseResponse(data=item.to_dict())

        key = 'test/{}/{}.json'.format(date.today().isoformat(),
                                       datetime.utcnow().timestamp())
        url = self.oss.put_object(BUCKET, key, data.to_json())
        print(url)
        res = requests.get(url)
        self.assertEqual(data.to_dict(), res.json())
        webbrowser.open(url)


if __name__ == '__main__':
    unittest.main()
