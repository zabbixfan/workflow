#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask_restful import Resource, reqparse,inputs
from ..common.ApiResponse import ApiResponse, ResposeStatus
from app.common.api_doc_helper import get_request_parser_doc_dist
from app.common.AuthenticateDecorator import need_user
from app.domains.kvm import kvmList,createVm,operateVm
from flasgger import swag_from

def get_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('offset',type=int,default=0)
    rp.add_argument('limit',type=int,default=20)
    rp.add_argument('keyword',type=unicode,required=False)
    rp.add_argument('status',type=unicode,default="")
    return rp.parse_args() if return_parse_args else rp

def post_args(return_arse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('cpu',type=int,default=1)
    rp.add_argument('memory',type=int,default=1024)
    rp.add_argument('instances',type=int,default=1)
    rp.add_argument('group',required=True)
    rp.add_argument('env',required=True)
    return rp.parse_args() if return_arse_args else rp

def operate_args(return_arse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('action',required=True)
    return rp.parse_args() if return_arse_args else rp



class kvms(Resource):
    @swag_from(get_request_parser_doc_dist("get kvmlist", ["Kvms"], get_args(False)))
    @need_user(roles=['admin'])
    def get(self):
        args = get_args()
        return ApiResponse(kvmList(keyword=args.keyword,offset=args.offset,limit=args.limit,status=args.status))

    @swag_from(get_request_parser_doc_dist("add a kvm", ["Kvms"], post_args(False)))
    @need_user(roles=['admin'])
    def post(self):
        args = post_args()
        return ApiResponse(createVm(args.instances,args.group,args.env,args.cpu,args.memory))

class kvm(Resource):
    @swag_from(get_request_parser_doc_dist("change kvm status", ["Kvms"], operate_args(False)))
    # @need_user(roles=['admin'])
    def put(self,id):
        args = operate_args()
        return ApiResponse(operateVm(id,args.action))
    @swag_from(get_request_parser_doc_dist("delete a kvm", ["Kvms"]))
    @need_user(roles=['admin'])
    def delete(self,id):
        return ApiResponse(operateVm(id,'deleteVm'))


api.add_resource(kvms,'/kvm')
api.add_resource(kvm,'/kvm/<string:id>')
