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
from config import Config
from app.tasks.mailTask import applyMail
from app.tasks.jobTask import createProjectJob,restartProjectJob
def ticketList(keyword=None,offset=0,limit=20,type=None,status=None):
    userinfo = g.user
    role = userinfo.get("role","")
    username = userinfo.get("name","")
    q = Tickets.query
    if status:
        q = q.filter(Tickets.status==status)
    else:
        q = q.filter(Tickets.status!='Delete')
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
        "createAt": datetime_to_strtime(data.createTime,format_str="%Y-%m-%d %H:%M:%S")
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
        "createAt": datetime_to_strtime(q.createTime,format_str="%Y-%m-%d %H:%M:%S"),
        "data": json.loads(q.data)
        }
    return res
def deleteTicketInfo(id):
    username = g.user.get("name", "")
    q = Tickets.query.filter(Tickets.id==id).first()
    if q:
        q.status = 'Delete'
        q.commit()
        return "delete ticket success"

def auditTicket(id,status):
    q = Tickets.query.filter(Tickets.id==id).first()
    if q:
        q.status = status
        q.commit()
    if status == 'Approve':
        query = {
            'id':q.id,
            'status': q.status,
            'data': json.loads(q.data),
            'requestMan': q.requestMan,
            'email': q.email,
            'type': q.type
        }
        jobDict[q.type].delay(query)
    return "audit ticket success",ResposeStatus.Success
class newTicket:
    def __init__(self,requestMan,name,status,types,id=None,email=None,requestManEng=None):
        self.requestMan = requestMan
        self.id = uuid().get_hex()
        if id:
            self.id = id
        self.name = name
        self.status = status
        self.type = types
        self.email = email
        self.requestManEng = requestManEng
    def Approve(self,ticket):
        data = {
            'id': ticket.id,
            'status': ticket.status,
            'data': json.loads(ticket.data),
            'requestMan': ticket.requestMan,
            'email': ticket.email,
            'type': ticket.type
        }
        # print json.dumps(data,indent=4)
        jobDict[ticket.type].delay(data)

class projectTicket(newTicket):
    def dataCheck(self,data):
        print data
        error = False
        message =''
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
                'rule': r'(^$|^[\d\w\.\-]+$)'
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
                projectGroupName
                projectType
                owner
                domainName
                gitGroup
            }   
         ]
        :return: 
        '''
        error,message = self.dataCheck(data)
        if error:
            return {'message':message},ResposeStatus.ParamFail
        else:
            ticket = Tickets.get_by_ticketid(self.id)
            if not ticket:
                ticket = Tickets()
                ticket.createTime = datetime.now()
            ticket.requestMan = self.requestMan
            ticket.requestManEng = self.requestManEng
            ticket.name = self.name
            ticket.status = self.status
            ticket.type = self.type
            ticket.id = self.id
            ticket.data = json.dumps(data)
            if self.email:
                ticket.email = self.email
            ticket.save()
        if self.status == 'Apply':
            toUser = Config.AUDITOR
            toHander = Config.AUDITORHANDER
            content = {
                "title": "Workflow工单申请",
                "content": "<h1>您有一个新的工单待处理，请登录http://workflow.apitops.com查看</h1s>"
            }
            applyMail.delay(toUser=toUser, toHander=toHander,mailArgs=content)
        elif self.status == 'Approve':
            self.Approve(ticket=ticket)

        return {
                'data': data,
                'requestMan': self.requestMan,
                'id': self.id,
                'type': self.type,
                'name': self.name,
                'status': self.status
        },ResposeStatus.Success
class restartTicket(newTicket):
    def dataCheck(self,data):
        error = False
        message =''
        params = [
            {
                'name': 'restartProject',
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
        if isinstance(data['restartProject'],list):
            if len(data['restartProject'])<3:
                pass
            else:
                logger().error(data)
                error = True
                message = '重启服务最多只能选择2个'
                return error, message
        else:
            logger().error(data)
            error = True
            message = 'param restartProject type should be list'
            return error, message

        return error,message
    def apply(self,data):
        '''

        :param data:
        data:[
            {
                restartProject:['projectName/env/ip','']
            }
         ]
        :return:
        '''
        pass
        error,message = self.dataCheck(data)
        if error:
            return {'message':message},ResposeStatus.ParamFail
        else:
            ticket = Tickets.get_by_ticketid(self.id)
            if not ticket:
                ticket = Tickets()
                ticket.createTime = datetime.now()
            ticket.requestMan = self.requestMan
            ticket.requestManEng = self.requestManEng
            ticket.name = self.name
            ticket.status = self.status
            ticket.type = self.type
            ticket.id = self.id
            ticket.data = json.dumps(data)
            if self.email:
                ticket.email = self.email
            ticket.save()
        if self.status == 'Apply':
            toUser = Config.AUDITOR
            toHander = Config.AUDITORHANDER
            content = {
                "title": "Workflow工单申请",
                "content": "<h1>您有一个新的工单待处理，请登录http://workflow.apitops.com查看</h1s>"
            }
            applyMail.delay(toUser=toUser, toHander=toHander,mailArgs=content)
        if self.status == 'Approve':
            self.Approve(ticket)
        if self.status == 'Complete':
            print 'complete'
        if self.status == 'Refuse':
            print 'refuse'
        return {
                'data': data,
                'requestMan': self.requestMan,
                'id': self.id,
                'type': self.type,
                'name': self.name,
                'status': self.status
        },ResposeStatus.Success
typeDict = {
    "createProject": projectTicket,
    "restartProject": restartTicket
}
jobDict = {
    "createProject": createProjectJob,
    "restartProject": restartProjectJob
}