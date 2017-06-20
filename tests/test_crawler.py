#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""base信息"""
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

from app.crawler.crawler import QQ
from app.models import VideoSource as VS

import unittest


class CrawlerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_qq(self):
        parer = QQ()
        item = parer.parser_item(
            'https://v.qq.com/detail/z/zwyy7umzhkroixx.html')

        self.assertEqual(item.type, VS.Type.DRAMA.value)


if __name__ == '__main__':
    unittest.main()
