#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''工具类'''
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

import re
import random

RE_CHINESE = re.compile(u"[\u4e00-\u9fa5]+")  # 正则查找中文
RE_ENGLISH = re.compile(u"[A-Za-z]+")  # 正则查找英文


STR = [
    '0', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', 'a', 'b',
    'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
]


def find_chinese(str):
    """
    查找字符串中中文集合
    :param str:
    :return:
    """
    return re.findall(RE_CHINESE, str)


def find_english(str):
    """
    查找字符串中的英文
    :param str:
    :return:
    """
    return re.findall(RE_ENGLISH, str)





def reduplicate(list):
    """
    去掉list中的重复值
    :param list:
    :return:
    """
    temp = []
    for item in list:
        if item not in temp:
            temp.append(item)
    return temp


def get_random_str(str_len):
    """
    获取随机字符串
    :param str_len: 需要获取的长度
    :return:
    """
    str_list = ""
    for i in range(0, str_len):
        str_list = str_list + STR[int(random.uniform(0, len(STR)))]
        pass
    return str_list


def generate_body_sort_script(sort='desc', **params):
    """生成es权重排序的body数据"""
    inline = []
    for key in params:
        inline.append("doc['{}'].value * params.{}".format(key, key))

    inline = "+".join(inline)

    body = {
        "sort": {
            "_script": {
                "type": "number",
                "script": {
                    "lang": "painless",
                    "inline": inline,
                    "params": params
                },
                "order": sort
            }
        }
    }
    return body


def generate_body(sort='desc', _script=None, match=None, term=None,
                  _range=None):
    '''构造esbody'''
    body = {}
    if _script:
        body = generate_body_sort_script(sort=sort, **_script)

    body['query'] = {
        "bool": {
            "must": [],
            "filter": []
        }
    }
    if match:
        for key, value in match.iteritems():
            body['query']['bool']['must'].append(
                {"match":
                    {
                        key: {
                            "query": value,
                            "operator": "and"
                        }
                    }
                }
            )

    if term:
        for key, value in term.iteritems():
            body['query']['bool']['filter'].append({"term": {key: value}})

    if _range:
        for key, value in _range.iteritems():
            body['query']['bool']['filter'].append({"range": {key: value}})

    return body


def filter_dict(json, **params):
    '''
    过滤json数据
    :param json:
    :param params:
    :param source_include:
    :return:
    '''
    source_include = params.get('source_include')
    source_exclude = params.get('source_exclude')

    temp = {}
    if source_include:
        for item in source_include:
            temp[item] = json[item]
        return temp
    elif source_exclude:
        for item in source_exclude:
            del json[item]
        return json


def check_back_card(card_num):
    """检查银行卡的合法性"""
    total = 0
    even = True

    card_num = list(card_num)
    card_num.reverse()
    check_num = card_num[0]
    card_num.pop(0)

    for item in card_num:
        item = int(item)
        if even:
            item <<= 1

        if item > 9:
            item -= 9

        total += item
        even = not even

    return int(check_num) is (10 - (total % 10)) % 10

