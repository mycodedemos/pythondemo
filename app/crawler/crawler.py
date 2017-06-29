#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
爱奇艺
http://www.iqiyi.com/
"""
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from app.common.base import BaseObject
from app.models import VideoSource as VS
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from datetime import date
from enum import Enum

import requests

HTTP_FORMAT = 'http:{}'


class BaseCrawler():
    def generator_soup(self, url):
        res = requests.get(url)
        return bs(res.content, 'lxml')

    def parser(self, url):
        pass

    def parser_item(self, url):
        pass

    def parser_list(self, url):
        pass

    def parser_search(self, url):
        pass


class Iqiyi():
    def parser_item(self, url):
        res = requests.get(url)
        # item = Item(url=url, type='video', source=Source.IQIYI.value)
        # soup = bs(res.content, 'lxml')
        #
        # metas = soup.find_all('meta')
        # for meta in metas:
        #     name = meta.attrs.get('name')
        #     content = meta.attrs.get('content')
        #     if name == 'irTitle':
        #         item.name = content
        #     elif name == 'irAlbumName':
        #         item.album_name = content
        #
        # des = soup.select('#data-videoInfoDes')[0]
        # item.description = des.string
        #
        # tags = soup.select('#datainfo-taglist')[0].children
        #
        # tags = [tag.string for tag in
        #         filter(lambda x: isinstance(x, Tag), tags)]
        #
        # item.tags = ','.join(tags)


class Souhu(BaseCrawler):
    PIC_CLASS = dict(
        movie='movie-pic', drama='drama-pic'
    )

    def parser_item(self, url):
        if 'item' not in url:
            return None
        item = VS.query_item(url=url)
        if not item:
            item = VS(url=url,
                      source=VS.Source.SOUHU.value)
        soup = self.generator_soup(url)

        # 获取视频类型
        script = soup.select_one('script')
        type_string = script.get_text(strip=True)
        type_index = type_string.find('filmType') + 12
        type_end = type_string.find(';', type_index) - 1
        item.type = type_string[type_index:type_end]
        poster_tag = soup.select_one(
            'div.{}'.format(self.PIC_CLASS[item.type])).select_one(
            'img')
        item.poster = HTTP_FORMAT.format(poster_tag['src'])
        item.name = poster_tag['alt']
        metas = list(soup.select_one('ul.cfix').find_all('li'))
        meta_len = len(metas)
        item.alias = ''.join(list(metas[0].stripped_strings)).split('：')[1]

        pd = ''.join(list(metas[1].stripped_strings)).split('：')[1]

        item.publish_date = None if len(pd) == 4 else pd
        item.year = int(pd) if len(pd) == 4 else pd[:4]

        print()
        for region in metas[2].select('a'):
            name = region.string
            url = region['href']
            print(name, url)

        regions = []
        if meta_len >= 3 and metas[2]:
            regions = [dict(name=meta.string, url=self.format_url(meta['href']))
                       for meta in metas[2].select('a')]
            item.region = '/'.join([x['name'] for x in regions])

        genres = []
        if meta_len >= 4 and metas[3]:
            genres = [dict(name=meta.string, url=self.format_url(meta['href']))
                      for meta in metas[3].select('a')]
            item.genre = '/'.join([x['name'] for x in genres])

        directors = []
        if meta_len >= 5 and metas[4]:
            directors = [
                dict(name=meta.string, url=self.format_url(meta['href']))
                for meta in metas[4].select('a')]
            item.director = '/'.join([x['name'] for x in directors])
        actors = []
        if meta_len >= 6 and metas[5]:
            actors = [dict(name=meta.string, url=self.format_url(meta['href']))
                      for meta in metas[5].select('a')]
            item.actor = '/'.join([x['name'] for x in actors])

        rating_tag = metas[6].select_one('strong') if meta_len >= 7 and metas[
            6] else None

        item.rating = float(rating_tag.string) if rating_tag else 0

        episodes = []
        ep_ul_tag = soup.select_one('ul.listA')
        if ep_ul_tag:
            ep_tags = ep_ul_tag.select('div.pic')
            episodes = [dict(name=o.select_one('a')['title'],
                             url=self.format_url(o.select_one('a')['href']),
                             poster=self.format_url(o.select_one('img')['src']))
                        for o in ep_tags]
        ext = dict(
            regions=regions,
            genres=genres,
            directors=directors,
            actors=actors,
            episodes=episodes
        )
        item.ext = ext
        des_tag = soup.select_one('span.full_intro')
        item.description = des_tag.string if des_tag else ""
        item.create_self()

    def parser_item_new(self, url):
        soup = self.generator_soup(url)

        genres = soup.select_one('div.colL')
        print(genres)

    def parser_search(self, url):
        soup = self.generator_soup(url)

        areas = list(soup.select('div.area'))
        for area in areas:
            a = area.select_one('div.btnBox a')
            if a:
                self.parser_item(self.format_url(a['href']))

    def format_url(self, url):
        return HTTP_FORMAT.format(url)


class QQ(BaseCrawler):
    TYPE = {
        "电视剧": VS.Type.DRAMA.value,
        "动漫": VS.Type.CARTOON.value,
        "电影": VS.Type.MOVIE.value,
        "综艺": VS.Type.SHOW.value,
    }

    def parser(self, url):
        if 'detail' in url:
            self.parser_item(url)
        elif 'search' in url:
            self.parser_search(url)


    def parser_item(self, url):
        soup = self.generator_soup(url)

        item = VS.query_item(url=url)

        if not item:
            item = VS(url=url, source=VS.Source.QQ.value)

        metas = soup.find_all('meta')
        for meta in metas:
            property = meta.attrs.get('property')
            content = meta.attrs.get('content')
            if property == 'og:title':
                item.name = content
            elif property == 'og:description':
                item.description = content
            elif property == 'og:image':
                item.poster = content

        type = soup.select_one('span.type')
        item.type = self.TYPE.get(type.string)
        type_item = soup.select('div.type_item')

        for o in type_item:
            subs = list(filter(lambda x: x != '\n', o.children))
            if len(subs) > 0 and subs[0]:
                if '地' in subs[0].string:
                    item.region = subs[1].string
                elif '别' in subs[0].string:
                    item.alias = subs[1].string
                elif '出品时间' in subs[0].string:
                    item.year = int(subs[1].string)
                elif '总集数' in subs[0].string:
                    item.episode_count = int(subs[1].string)
                elif '上映时间' in subs[0].string:
                    item.publish_date = subs[1].string
        # 标签
        tag_tags = soup.select('a.tag')
        genres = [dict(name=o.string, url=o['href']) for o in tag_tags]
        item.genre = '/'.join([x['name'] for x in genres])

        actor_items = soup.select('ul.actor_list li.item')
        directors = []
        actors = []
        for o in actor_items:
            itemprop = o.attrs.get('itemprop')
            a = o.select_one('a[_stat=info:actor_avatar]')
            if itemprop:
                ext_item = dict(
                    poster=HTTP_FORMAT.format(a.select_one('img')['src']),
                    url=a['href'],
                    name=o.select_one('span[_stat=info:actor_name]').string
                )
            if itemprop == 'director':
                directors.append(ext_item)
            elif itemprop == 'actor':
                actors.append(ext_item)

        item.director = '/'.join([x['name'] for x in directors])
        item.actor = '/'.join([x['name'] for x in actors])

        # 剧集
        episode_tags = soup.select('span[itemprop=episode]')
        episodes = [dict(url=o.select_one('a')['href'],
                         name=o.select_one('span').string) for o in
                    episode_tags] if episode_tags else []

        if item.is_moive:
            episodes = [
                dict(url=o['href'], name=o.select_one('span.icon_text').string)
                for o in soup.select_one('div.video_btn').select(
                    'a[_stat=info:playbtn]')]
            item.episode_count = len(episodes)

        ext = dict(
            genres=genres,
            directors=directors,
            actors=actors,
            episodes=episodes
        )

        # 评分
        rating_tag = soup.select_one('div.video_score')
        if rating_tag:
            item.rating = float(rating_tag.select_one('span.score').string)

            if rating_tag.select_one('a.score_db'):
                ext['douban'] = dict(
                    url=rating_tag.select_one('a.score_db')['href'])

        item.ext = ext

        item.create_self()
        return item

    def parser_search(self, url):
        soup = self.generator_soup(url)

        items = []

        a_tags = soup.select('a[_stat=intent:list_title]')
        for o in a_tags:
            item_url = o['href']
            if 'detail' in item_url:
                self.parser_item(item_url)

        h2_tags = soup.select('h2.result_title')
        for o in h2_tags:
            item_type = o.select_one('span.type')
            if item_type and item_type.string in '电影 电视剧 综艺 动漫':
                item_url = o.select_one('a')['href']
                if 'detail' in item_url:
                    self.parser_item(item_url)
                    print(item_url)


class Maomiav():
    pass

if __name__ == '__main__':
    parer = QQ()
    # item = parer.parser_item('https://v.qq.com/detail/z/zwyy7umzhkroixx.html')
    # print(item.name)
    # parer.parser_item('http://v.qq.com/detail/f/fiduo27kl7cfubk.html')
    # parer.parser_item('https://v.qq.com/detail/b/bqejbbv8mgtusrs.html')
    # parer.parser_item('http://v.qq.com/detail/i/iectcu0y1nv0vp5.html')
    # parer.parser_search('http://v.qq.com/detail/c/cymqf1mz55umyqy.html')

    url = 'http://www.698AA.com/htm/index.htm'

    soup = bs(requests.get(url).content,'lxml')
    print(soup)


