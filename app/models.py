#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''models'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from app.common.base import BaseModel
from app.config import db
from app.config import BaseConfig
from datetime import date
from datetime import datetime
from datetime import timedelta
from enum import Enum


class Action(BaseModel, db.Model):
    __tablename__ = 'action'
    id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.VARCHAR, default="")
    ip = db.Column(db.VARCHAR, default="")
    action_type = db.Column(db.INT, default=BaseConfig.TYPE_ACTION_VIEW)
    item_id = db.Column(db.VARCHAR)
    item_type = db.Column(db.INT)
    is_del = db.Column(db.INT, default=0)
    create_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())


class Image(BaseModel, db.Model):
    __tablename__ = 'image'
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


class Task(BaseModel, db.Model):
    class DoneStatus(Enum):
        undo = 0
        done = 1
        under_way = 2

    __tablename__ = 'task'
    id = db.Column(db.VARCHAR, primary_key=True)
    user_id = db.Column(db.VARCHAR, default="")
    name = db.Column(db.VARCHAR, default="")
    total_work = db.Column(db.INT, default=0)
    begin_work = db.Column(db.INT, default=0)
    daily_work = db.Column(db.INT, default=0)
    total_day = db.Column(db.INT, default=0)
    begin_day = db.Column(db.DATE)
    end_day = db.Column(db.DATE)
    type = db.Column(db.INT, default=1, doc='类型：1、总完成量，2、按每天完成')
    done_status = db.Column(db.INT, default=0, doc='完成状态、0：外开始、1：已完成、2：进行中')
    status_message = db.Column(db.VARCHAR, default="")
    remark = db.Column(db.VARCHAR, default="")
    is_del = db.Column(db.INT, default=0)
    create_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())
    update_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())

    todo_work = 0  # 需要做的工作
    last_day_work = 0  # 最后一天的工作

    daily_tasks = db.relationship('TaskDaily', backref='task', lazy='dynamic')

    @property
    def is_total(self):
        print(self.type)
        return self.type == 1

    @property
    def is_daily(self):
        return self.type == 2

    @property
    def work_days(self):
        days = self.total_day
        return [(self.begin_day + timedelta(i)).isoformat() for i in
                range(0, days)]

    def __init__(self, total_work=0, daily_work=10, begin_work=1, type=1,
                 **params):
        """
        任务分为总量和按天分类

        :param type: 1/总量   2/按天
            if type == 1 ：
                total_work、daily_work、begin_work为必传
            elif type == 2：
                daily_work、total_day必传
        :param total_work:
        :param daily_work:
        :param begin_work:
        :param params:
        """
        self.id = params.get('id', self.generate_id())
        self.daily_work = int(daily_work)
        begin_day = params.get('begin_day')
        self.begin_day = self.make_begin_day(begin_day)
        self.name = params.get('name')
        self.type = int(type)

        print(self.is_total,self.is_daily)

        if self.is_total:
            self.total_work = int(total_work)
            self.begin_work = int(begin_work)
            self.todo_work = self.total_work - self.begin_work + 1
            self.last_day_work = self.todo_work % self.daily_work
            self.total_day = self.todo_work // self.daily_work + \
                             (1 if self.last_day_work > 0 else 0)

        if self.is_daily:
            self.total_day = int(params.get('total_day'))
            print(self.total_day)
            self.total_work = self.total_day * self.daily_work
            self.todo_work = self.todo_work
        print(self)

        self.end_day = self.begin_day + timedelta(self.total_day - 1)
        self.status_message = '{}, 共{}工作量, 每天完成{}, {}天完成, {}开始, {}结束'.format(
            self.name, self.todo_work, self.daily_work, self.total_day,
            self.begin_day, self.end_day
        )
        self.remark = params.get('remark')
        self.user_id = params.get('user_id')

    def make_begin_day(self, d):
        if not d:
            return date.today()
        return d if isinstance(d, date) else date(int(d.split('-')[0]),
                                                  int(d.split('-')[1]),
                                                  int(d.split('-')[2]))


class TaskDaily(BaseModel, db.Model):
    class DoneStatus(Enum):
        undo = 0
        done = 1
        over_done = 2
        diff_done = 3

    __tablename__ = 'task_daily'
    id = db.Column(db.INT, primary_key=True)
    task_id = db.Column(db.VARCHAR, db.ForeignKey('task.id'), default="")
    todo_work = db.Column(db.INT, default=0)
    done_work = db.Column(db.INT, default=0)
    work_day = db.Column(db.DATE)
    remark = db.Column(db.VARCHAR, default="")
    done_status = db.Column(db.INT, default=0)
    is_del = db.Column(db.INT, default=0)
    create_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())
    update_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())

    def done(self, done_work):
        """完成任务"""
        if done_work == self.todo_work:
            remark = '完成任务'
            done_status = self.DoneStatus.done.value
        elif done_work > self.todo_work:
            diff_day = (done_work - self.todo_work) / self.task.daily_work
            remark = '超额完成任务\n预计提前 {} 天完成任务'.format(diff_day) if self.task.is_total else ''
            done_status = self.DoneStatus.over_done.value
        elif done_work < self.todo_work:
            diff_day = (self.todo_work - done_work) / self.task.daily_work
            remark = '没有完成任务\n预计延后 {} 天完成任务'.format(diff_day) if self.task.is_total else ''
            done_status = self.DoneStatus.diff_done.value

        self.remark = remark
        self.done_work = done_work
        self.done_status = done_status
        self.update_self()

        self.task.done_status = Task.DoneStatus.under_way.value
        self.task.update_self()
        return self


class Article(BaseModel, db.Model):
    __tablename__ = 'article'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, default="")
    category_id = db.Column(db.INT, db.ForeignKey('category.id'))
    tags = db.Column(db.String, default="")
    content = db.Column(db.String, default="")
    is_del = db.Column(db.INT, default=0)
    create_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())
    update_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())


class Category(BaseModel, db.Model):
    __tablename__ = 'category'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String, default="")
    is_del = db.Column(db.INT, default=0)
    create_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())
    update_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow())

    articles = db.relationship("Article", backref="category", lazy='dynamic')
