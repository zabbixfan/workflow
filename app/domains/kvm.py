#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.ipPool import *
from app.common.pageHelper import PageResult
from flask import g
from app.common.time_helper import datetime_to_strtime
from app.common.ApiResponse import ResposeStatus
import re,json
from app.tasks.jobTask import createKvmVmJob,operateKvmVmJob

def kvmList(keyword=None,offset=0,limit=20,status=None):
    q = ipPool.query.filter(ipPool.type == 'kvm')
    if status:
        q = q.filter(ipPool.status == status)
    else:
        q = q.filter(ipPool.status != 'Delete')
    if keyword:
        key = keyword.replace("%", "").replace("_", "").replace("*", "")
        key = '%{}%'.format(key)
        q = q.filter(db.or_(ipPool.ip.like(key),ipPool.name.like(key)))
    return PageResult(q.order_by(ipPool.create_time.desc()), limit, offset).to_dict(lambda data: {
        "id": data.id,
        "name": data.name,
        "hostServer": data.hostServer,
        "manager": data.manager,
        "projectGroup": data.projectGroup,
        "status": data.status,
        "createAt": datetime_to_strtime(data.create_time, format_str="%Y-%m-%d %H:%M:%S")
    })

def createVm(instances,group,env,cpu=2,memory=4096):
    query = {
        'data': {
            'vmInstances': instances,
            'projectGroupName': group,
            'projectEnv': env,
            'vmMEM': memory,
            'vmCPU': cpu
        }
    }
    manager=g.user['loginName']
    createKvmVmJob.delay(query,backEndCreate=True,manager=manager)
    return ''

def operateVm(id,action):
    q = ipPool.query.filter(ipPool.id==id).first()
    if q:
        name=q.name
        ip=q.ip
        operateKvmVmJob.delay(name,ip,action)
