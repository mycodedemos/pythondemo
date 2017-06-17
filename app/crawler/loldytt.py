#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
电影天堂
http://www.loldytt.com/
"""
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."


from bs4 import BeautifulSoup as bs
import requests



if __name__ == '__main__':
    res = requests.get('http://www.iqiyi.com/v_19rr6z41d8.html')
    print(res.content)
    soup = bs(res.content,'lxml')
    print(soup.title.string)