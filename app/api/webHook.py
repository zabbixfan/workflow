#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask import g,jsonify,request
from flask_restful import Resource, reqparse,inputs

from app.models.tickets import Tickets
from app.models.ipPool import ipPool
from app.models.ticketLogs import TicketLog
from app.common.time_helper import current_datetime
from app.common.httpHelp import getUserIdByName
from config import Config
from app.tasks.mailTask import applyMail
from app.common.portCheck import singleCheck
import json
class webHook(Resource):
    def post(self,id):

        ticket = Tickets.query.filter(Tickets.id==id).first()
        if ticket:
            data = request.json
            ip = ipPool.query.filter(ipPool.ip == data['params']['vmIP']).first()
            result = data['result']
            #执行成功
            if result.endswith('success'):
                ticket.status='Complete'
                ticket.commit()
                if ip:
                    ip.manager = ticket.requestManEng
                    ip.name = data['params']['vmName']
                    ip.status = 'Running'
                    ip.hostServer = data['hostServer']
                    ip.projectGroup = json.loads(ticket.data)['projectGroupName']
                    ip.projectEnv = data['params']['env']
                    ip.type = 'kvm'
            #执行失败
            else:
                ip.status = 'Unused'
            ip.commit()
            log = TicketLog()
            log.ticketId = id
            log.time = current_datetime()
            if 'message' in data.keys():
                log.content = data['message']
            else:
                log.content = data['result']
            log.save()

            toUser = Config.AUDITOR
            toHander = Config.AUDITORHANDER
            if ticket.email not in toUser:
                toUser = Config.AUDITOR + [ticket.email]
                toHander = Config.AUDITORHANDER + [(ticket.requestMan, ticket.email)]
            content = {
                "title": "Workflow工单申请",
                "content": "<p>您的工单{}已完成，资源已开通,请登录workflow工单查看资源明细<p>".format(ticket.name)
            }
            applyMail(toUser=toUser, toHander=toHander, mailArgs=content)
        else:
            data = request.json
            print data['action']
            ip = ipPool.query.filter(ipPool.ip == data['params']['vmIP']).first()
            result = data['result']
            #执行成功
            if data['action'] == 'createVm':
                if result.endswith('success'):
                    if ip:
                        ip.name = data['params']['vmName']
                        ip.status = 'Running'
                        ip.hostServer = data['hostServer']
                        ip.projectGroup = data['params']['vmName'].split("-")[0]
                        ip.projectEnv = data['params']['env']
                        ip.type = 'kvm'
                #执行失败
                else:
                    ip.status = 'Unused'

            if data['action'] == 'deleteVm':
                if result.endswith('success'):
                    if ip:
                        ip.status = 'Unused'
                else:
                    ip.status = 'Running'
            if data['action'] in ['stopVm','restartVm','startVm']:
                if result.endswith('success'):
                    if ip and data['action']=='stopVm':
                        ip.status = 'Stopping'
                    if ip and data['action'] in ['startVm','restartVm']:
                        ip.status = 'Running'
                else:
                    if ip:
                        if singleCheck(ip.ip):
                            ip.status = 'Running'
                        else:
                            ip.status = 'Stopping'
            ip.commit()
            log = TicketLog()
            log.ticketId = id
            if 'message' in data.keys():
                log.content = data['message']
            else:
                log.content = data['result']
            log.save()
            #todo other kvm action
        return {}

api.add_resource(webHook,'/webhook/<string:id>')