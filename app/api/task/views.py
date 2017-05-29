#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''支持接口'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from app.config import app
from app.config import BaseConfig
from app.common.base import BaseResponse
from app.common.base import BaseRequest
from app.common.decorator import args_required
from app.api.task.models import Task
from app.api.task.models import TaskDaily
from app.api.action.models import Action

from flask import Blueprint
from flask import g

task_bp = Blueprint('task', __name__)


@task_bp.route('/task', methods=['POST'])
@args_required('name', 'total_work', 'daily_work')
def create():
    '''生成任务'''
    args = BaseRequest.get_args()
    task = Task(**args).create_self()
    todo_work = task.begin_work - 1
    for day in task.work_days:
        daily_work = task.daily_work if day != task.end_day.isoformat() or task.last_day_work == 0 else task.last_day_work
        todo_work += daily_work
        TaskDaily.create(
            task_id=task.id,
            todo_work=todo_work,
            work_day=day
        )
    return BaseResponse.return_success(data=task.to_dict().filter('id'))


@task_bp.route('/task/<string:task_id>', methods=['GET'])
def detail(task_id):
    '''获取任务'''
    item = Task.query_item(id=task_id)
    return BaseResponse.return_success(item.to_dict(rel=True))


@task_bp.route('/task_daily/<int:id>', methods=['PUT'])
@args_required('done_work')
def done_daily_task(id):
    '''完成每天任务'''
    args = BaseRequest.get_args()
    todo_work = BaseRequest.get_arg_int(args, 'done_work')

    item = TaskDaily.query_item(id=id)
    if not item:
        return BaseResponse.return_not_found()

    task = item.task

    if not task:
        return BaseResponse.return_not_found('id can not found task')

    item.done(todo_work)

    return BaseResponse.return_success(item.to_dict().filter('remark'))
