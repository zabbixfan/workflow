#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask import g,jsonify,request
from flask_restful import Resource, reqparse,inputs
from ..common.ApiResponse import ApiResponse, ResposeStatus
from ..common.alopex_auth_sdk import AccessTokenModel
from app.common.api_doc_helper import get_request_parser_doc_dist
from app.common.AuthenticateDecorator import need_user
from app.domains.tickets import ticketList ,typeDict,getTicketInfo,deleteTicketInfo,auditTicket
from flasgger import swag_from

def get_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('offset',type=int,default=0)
    rp.add_argument('limit',type=int,default=20)
    rp.add_argument('keyword',type=unicode,required=False)
    rp.add_argument('type',type=unicode,default="")
    rp.add_argument('status',type=unicode,default="")
    return rp.parse_args() if return_parse_args else rp

def post_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("name")
    rp.add_argument("ticketType",required=True,nullable=False)
    rp.add_argument("status")
    # rp.add_argument("data",type=dict,default=[],action='append')
    rp.add_argument("data", type=dict)
    return rp.parse_args() if return_parse_args else rp
def audit_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("id",required=True,nullable=False)
    rp.add_argument('status', type=unicode, default="")
    return rp.parse_args() if return_parse_args else rp

class tickets(Resource):
    @swag_from(get_request_parser_doc_dist("get ticketlist", ["Tickets"], get_args(False)))
    @need_user()
    def get(self):
        args = get_args()
        print g.user
        return ApiResponse(ticketList(keyword=args.keyword,offset=args.offset,limit=args.limit,status=args.status,type=args.type))
    @swag_from(get_request_parser_doc_dist("add a ticket", ["Tickets"], post_args(False)))
    @need_user()
    def post(self):
        res={}
        args = post_args()
        ticketType = args.ticketType
        requestMan = g.user["name"]
        requestManEng = g.user["loginName"]
        email = g.user["email"]
        if ticketType in typeDict.keys():
            ticket = typeDict[ticketType](requestMan=requestMan,name=args.name,status=args.status,types=ticketType,email=email,requestManEng=requestManEng)
            res,status= ticket.apply(args.data)
        return ApiResponse(res,status) if res else ApiResponse(res,status=ResposeStatus.Fail)

    @need_user(roles=["admin"])
    def put(self):
        res={}
        args = audit_args()
        res,status = auditTicket(id=args.id,status=args.status)
        return ApiResponse(res,status) if res else ApiResponse(res,status=ResposeStatus.Fail)


class ticket(Resource):
    @need_user()
    def put(self,id):
        res={}
        args = post_args()
        ticketType = args.ticketType
        requestMan = g.user["name"]
        if ticketType in typeDict.keys():
            ticket = typeDict[ticketType](requestMan=requestMan,name=args.name,status=args.status,types=ticketType,id=id)
            res,status= ticket.apply(args.data)
        return ApiResponse(res,status) if res else ApiResponse(res,status=ResposeStatus.Fail)
    @need_user()
    def get(self,id):
        return ApiResponse(getTicketInfo(id))
    @need_user()
    def delete(self,id):
        return ApiResponse(deleteTicketInfo(id))



api.add_resource(tickets,'/tickets')
api.add_resource(ticket,'/tickets/<string:id>')
