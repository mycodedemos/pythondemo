#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''支持接口'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from app.common.base import BaseResponse
from app.common.base import BaseRequest
from app.common.decorator import args_required
from app.models import Task
from app.models import TaskDaily

from flask import Blueprint

task_bp = Blueprint('task', __name__)


@task_bp.route('/task', methods=['POST'])
@args_required('name', 'daily_work')
def create():
    '''生成任务'''
    args = BaseRequest.get_args()
    print(args)
    type = BaseRequest.get_arg_int(args, 'type', 1)
    if type == 1 and 'total_work' not in args:
        return BaseResponse.return_forbidden('total_work is necessary')
    elif type == 2 and 'total_day' not in args:
        return BaseResponse.return_forbidden('total_day is necessary')

    task = Task(**args).create_self()
    todo_work = task.begin_work - 1
    for day in task.work_days:
        daily_work = task.daily_work if day != task.end_day.isoformat() or task.last_day_work == 0 else task.last_day_work
        if task.is_total:
            todo_work += daily_work
        else:
            todo_work = daily_work
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


@task_bp.route('/task/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    '''获取任务'''
    item = Task.query_item(id=task_id)
    if not item:
        return BaseResponse.return_not_found()

    item.delete_self()

    TaskDaily.delete(task_id=task_id)

    return BaseResponse.return_success()


@task_bp.route('/task', methods=['GET'])
def tasks():
    '''任务列表'''
    args = BaseRequest.get_args()
    page = BaseRequest.get_arg_int(args, 'page', 1)
    per_page = BaseRequest.get_arg_int(args, 'per_page', 10)
    type = BaseRequest.get_arg_int(args, 'type', 1)
    paginate = Task.query_paginate(page, per_page, type=type)
    items = paginate.items
    res = [item.to_dict().filter('id', 'name', 'done_status') for item in items]
    return BaseResponse.return_success(
        BaseResponse.make_paginate(res, paginate.total, page, per_page))


@task_bp.route('/task_daily/<int:id>', methods=['PUT'])
@args_required('done_work')
def done_daily_task(id):
    '''完成每天任务'''
    args = BaseRequest.get_args()
    todo_work = BaseRequest.get_arg_int(args, 'done_work')

    item = TaskDaily.query_item(id=id)
    if not item:
        return BaseResponse.return_not_found()

    if item.done_status != 0:
        return BaseResponse.return_forbidden('不可重复做任务')

    task = item.task

    if not task:
        return BaseResponse.return_not_found('id can not found task')

    item.done(todo_work)

    return BaseResponse.return_success(item.to_dict().filter('remark'))
