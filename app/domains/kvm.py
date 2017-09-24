#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.ipPool import *
from app.common.pageHelper import PageResult
from flask import g
from app.common.time_helper import datetime_to_strtime
from app.tasks.jobTask import createKvmVmJob,operateKvmVmJob,createKvmVmbackEnd
from app.common.httpHelp import getUserInfoByName
def kvmList(keyword=None,offset=0,limit=20,status=None):
    q = ipPool.query.filter(ipPool.type == 'kvm')
    if status:
        q = q.filter(ipPool.status == status)
    else:
        q = q.filter(ipPool.status != 'unUsed')
    if keyword:
        key = keyword.replace("%", "").replace("_", "").replace("*", "")
        key = '%{}%'.format(key)
        q = q.filter(db.or_(ipPool.ip.like(key),ipPool.name.like(key)))
    return PageResult(q.order_by(ipPool.sys_time.desc()), limit, offset).to_dict(lambda data: {
        "id": data.id,
        "name": data.name,
        "hostServer": data.hostServer,
        "manager": getUserInfoByName(data.manager)['name'],
        "ip": data.ip,
        "env": data.projectEnv,
        "projectGroup": data.projectGroup,
        "status": data.status,
        "lastUpdate": datetime_to_strtime(data.sys_time, format_str="%Y-%m-%d")
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
    servers=ipPool.query.filter(ipPool.status=='unUsed').all()
    servers.sort(lambda x, y: cmp(''.join([i.rjust(3, '0') for i in x.ip.split('.')]),
                                ''.join([i.rjust(3, '0') for i in y.ip.split('.')])))
    for server in servers[:instances]:
        server.status='Locking'
        server.manager=manager
        server.type='kvm'
        server.commit()
        createKvmVmbackEnd(query,server.ip,backEndCreate=True,manager=manager)
    return ''

def operateVm(id,action):
    server = ipPool.query.filter(ipPool.id==id).first()
    if server:
        name=server.name
        ip=server.ip
        server.status = 'Locking'
        server.commit()
        operateKvmVmJob(name,ip,action)
    return ''
