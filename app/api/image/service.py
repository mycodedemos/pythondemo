#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''直接逻辑'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import requests

from app.models import Image
from app.common.third.juhe import Juhe
from app.common.security import Md5
from app.common.base import BaseDB

from sqlalchemy import desc


def crawler_data(key):
    jh = Juhe(key)

    for i in range(1, 120):
        image = Image.query.filter(
            Image.is_del == 0,
            Image.source == 'juhe',
            Image.publish_ts > 0
        ).order_by(
            Image.publish_ts).first()

        res = jh.get_img_by_time(image.publish_ts, 'desc', 1, 20)
        print(res)
        result = res['result']
        if not result:
            return
        data = res['result']['data']

        for item in data:
            third_id = item['hashId']
            args = {
                "third_id": third_id
            }
            image = Image.query_item(**args)
            if not image:
                args['id'] = Image.generate_id()
                args['content'] = item['content']
                args['url'] = item['url']
                args['publish_ts'] = item['unixtime']
                try:
                    Image.create(**args)
                except BaseException as e:
                    print(e)


def crawler_jisu_data():
    for i in range(2, 138):

        data = requests.get(
            url='http://api.jisuapi.com/xiaohua/pic',
            params={
                "pagenum": i,
                "pagesize": 20,
                "sort": "addtime",
                "appkey": "8e5a6c5affe49a6d"
            }
        ).json()['result']['list']

        for item in data:

            args = {
                "url": item['pic']
            }
            image = Image.query_item(**args)
            if not image:
                args['id'] = Image.generate_id()
                args['content'] = item['content']
                args['source'] = 'jisu'
                try:
                    Image.create(**args)
                except BaseException as e:
                    print(e)


def update_md5():
    images = Image.query.filter_by(is_del=0, md5="").all()

    for image in images:
        try:
            md5 = Md5.encrypt_by_url(image.url)
            print(md5)
            if md5 == '2923b250a3660c034aa7831d5e6d7f3c':
                Image.delete(id=image.id)
            else:
                Image.update_by_id(
                    id=image.id,
                    md5=md5
                )
        except BaseException as e:
            print(e, image.id)
            Image.update_by_id(
                id=image.id,
                is_del=1
            )


def remove_data():
    sql = "select * from " \
          "(select md5,count(0) as count from image " \
          "where is_del = 0 and md5 > '' " \
          "group by md5 order by count desc) as imd5 " \
          "where imd5.count >1;"
    res = BaseDB.query(sql, [])

    for item in res:
        print(item)
        image = Image.query_item(
            md5=item['md5']
        )
        print(image)
        Image.update_by_id(
            id=image.id,
            is_del=1
        )


def update_length():
    images = Image.query.filter_by(is_del=0, length=0).all()
    for image in images:
        res = requests.get(image.url)
        if res.status_code == 200:
            content_length = len(res.content)
            print(content_length)
            Image.update_by_id(
                id=image.id,
                length=content_length
            )
        else:
            Image.update_by_id(
                id=image.id,
                is_del=1
            )


if __name__ == '__main__':
    # crawler_data(Juhe.KEY)
    # crawler_data(Juhe.KEY2)
    update_length()
    update_md5()
    remove_data()
    pass
