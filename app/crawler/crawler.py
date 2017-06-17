#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
爱奇艺
http://www.iqiyi.com/
"""
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from app.common.base import BaseObject
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from enum import Enum

import requests


class Source(Enum):
    IQIYI = 1


class Item(BaseObject):
    name = None
    album_name = None
    album_url = None
    tags = None
    type = None  # video album
    source = 0  # iqiyi
    description = None
    url = None
    watch_url = None
    download_urls = []


class Iqiyi():
    def parser_item(self, url):
        res = requests.get(url)
        item = Item(url=url, type='video', source=Source.IQIYI.value)
        soup = bs(res.content, 'lxml')

        metas = soup.find_all('meta')
        for meta in metas:
            name = meta.attrs.get('name')
            content = meta.attrs.get('content')
            if name == 'irTitle':
                item.name = content
            elif name == 'irAlbumName':
                item.album_name = content

        des = soup.select('#data-videoInfoDes')[0]
        item.description = des.string

        tags = soup.select('#datainfo-taglist')[0].children

        tags = [tag.string for tag in
                filter(lambda x: isinstance(x, Tag), tags)]

        item.tags = ','.join(tags)


if __name__ == '__main__':
    i = Iqiyi()
    i.parser_item('http://www.iqiyi.com/v_19rr6z41d8.html')
