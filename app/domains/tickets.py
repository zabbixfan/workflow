#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.tickets import *
from app.common.pageHelper import PageResult
from flask import g
from app.common.time_helper import datetime_to_strtime
from app.models.tickets import Tickets
from app.common.ApiResponse import ResposeStatus
from app import logger
import re,json
from uuid import uuid1 as uuid
from datetime import datetime
def ticketList(keyword=None,offset=0,limit=20,type=None,status=None):
    userinfo = g.user
    role = userinfo.get("role","")
    username = userinfo.get("name","")
    q = Tickets.query
    if status:
        q = q.filter(Tickets.status==status)
    else:
        q = q.filter(Tickets.status!=statusMapper['Delete'])
    if type:
        q = q.filter(Tickets.type==type)
    if not role:
        q = q.filter(Tickets.requestMan==username)
    if keyword:
        key = keyword.replace("%","").replace("_","").replace("*","")
        key = '%{}%'.format(key)
        q = q.filter(Tickets.name.like(key))
    return PageResult(q.order_by(Tickets.createTime.desc()),limit,offset).to_dict(lambda data:{
        "id":data.id,
        "name":data.name,
        "status":data.status,
        "type":data.type,
        "requestMan":data.requestMan,
        "auditor": data.auditor,
        "executor": data.executor,
        "createAt": datetime_to_strtime(data.createTime)
    })
def getTicketInfo(id):
    res ={}
    q = Tickets.query.filter(Tickets.id==id).first()
    if q:
        res = {
        "id":q.id,
        "name":q.name,
        "status":q.status,
        "type":q.type,
        "requestMan":q.requestMan,
        "auditor": q.auditor,
        "executor": q.executor,
        "createAt": datetime_to_strtime(q.createTime),
        "data": json.loads(q.data)
        }
    return res
def deleteTicketInfo(id):
    q = Tickets.query.filter(Tickets.id==id).first()
    if q:
        q.status = statusMapper['Delete']
        q.commit()
        return "delete ticket success"

class newTicket:
    def __init__(self,requestMan,name,status,types,id=None,email=None):
        self.requestMan = requestMan
        self.id = uuid().get_hex()
        if id:
            self.id = id
        self.name = name
        self.status = status
        self.type = types
        self.email = email

class projectTicket(newTicket):
    def dataCheck(self,data):
        error = False
        message =''
        print data
        params = [
            {
                'name': 'projectName',
                'rule': r'^[a-zA-Z][a-zA-Z0-9\-]+[a-z0-9]$'
            },
            {
                'name': 'projectDescription',
                'rule': ''
            },
            {
                'name': 'projectGroupName',
                'rule': ''
            },
            {
                'name': 'projectType',
                'rule': ''
            },
            {
                'name': 'owner',
                'rule': ''
            },
            {
                'name': 'domainName',
                'rule': r'^[\d\w\.\-]+$'
            }
        ]
        for param in params:
            if param['name'] not in data.keys():
                error = True
                message = 'param {} not found'.format(param['name'])
                logger().error(data)
                return error,message
            elif not param['name']:
                error = True
                message = 'param {} can\'t be none'.format(param['name'])
                logger().error(data)
                return error,message
            if param.has_key('rule'):
                if param['rule']:
                    pattern = re.compile(param['rule'])
                    if not pattern.match(data[param['name']]):
                        logger().error(data)
                        error = True
                        message = 'param {} value does not match pattern:{}'.format(param['name'],param['rule'])
                        return error,message
        return error,message
    def apply(self,data):
        '''
        :param data:
         data:[
            {
                projectName:
                projectDescription:
                projectGroupId
                projectType
                owner
                domainName
                gitGroup
            }   
         ]
        :return: 
        '''
        paras = {}
        for d in data:
            error,message = self.dataCheck(d)
            if error:
                return {'message':message},ResposeStatus.ParamFail
        else:
            ticket = Tickets.get_by_ticketid(self.id)
            if not ticket:
                ticket = Tickets()
                ticket.createTime = datetime.now()
            ticket.requestMan = self.requestMan
            ticket.name = self.name
            ticket.status = statusMapper[self.status]
            ticket.type = self.type
            ticket.id = self.id
            ticket.data = json.dumps(data)
            if self.email:
                ticket.email = self.email
            ticket.save()
        if self.type == statusMapper['Apply']:
            pass
            #mail to auditor
        elif self.type == statusMapper['Approve']:
            #mail to auditor and executor
            pass
        return {
                    'data': data,
                    'requestMan': self.requestMan,
                    'id': self.id,
                    'type': self.type,
                    'name': self.name,
                    'status': self.status
                },ResposeStatus.Success

typeDict = {
    "createProject": projectTicket
}