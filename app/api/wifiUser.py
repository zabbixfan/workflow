#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask_restful import Resource, reqparse,inputs
from ..common.ApiResponse import ApiResponse, ResposeStatus
from app.common.api_doc_helper import get_request_parser_doc_dist
from app.domains.wifiUser import wifiUserList,addWifiUser,changeWifiUserPassWord,deleteWifiUserPassWord,searchWifiUsersByName,getUsersBySystime
from app.common.AuthenticateDecorator import need_user
from flasgger import swag_from

def get_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('offset',type=int,default=0)
    rp.add_argument('limit',type=int,default=20)
    rp.add_argument('keyword',type=unicode,required=False)
    rp.add_argument('status',type=unicode,default="")
    return rp.parse_args() if return_parse_args else rp

def post_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('username',required=True)
    rp.add_argument('value',required=True)
    return rp.parse_args() if return_parse_args else rp

def operate_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('value',required=True)
    return rp.parse_args() if return_parse_args else rp
def syncuser_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('systime',default=None)
    return rp.parse_args() if return_parse_args else rp

class wifiUserResource(Resource):
    @swag_from(get_request_parser_doc_dist("get wifiuserlist", ["wifiUser"], get_args(False)))
    @need_user(roles=['admin'])
    def get(self):
        args = get_args()
        return ApiResponse(wifiUserList(keyword=args.keyword, offset=args.offset, limit=args.limit))
    @swag_from(get_request_parser_doc_dist("add a wifiuser", ["wifiUser"], post_args(False)))
    @need_user(roles=['admin'])
    def post(self):
        args = post_args()
        res,status=addWifiUser(args.username,args.value)
        return ApiResponse(res,status)
class wifiUserResources(Resource):
    @swag_from(get_request_parser_doc_dist("change wifiuser password", ["wifiUser"], operate_args(False)))
    @need_user(roles=['admin'])
    def put(self,id):
        args = operate_args()
        res,status = changeWifiUserPassWord(id,args.value)
        return ApiResponse(res,status)
    @swag_from(get_request_parser_doc_dist("delete a wifiuser", ["wifiUser"]))
    @need_user(roles=['admin'])
    def delete(self,id):
        res,status = deleteWifiUserPassWord(id)
        return ApiResponse(res,status)
class SearchWifiUserResource(Resource):
    @swag_from(get_request_parser_doc_dist("search wifiuser", ["wifiUser"], operate_args(False)))
    def get(self):
        args=get_args()
        return ApiResponse(searchWifiUsersByName(args.keyword))
class wifiUserSyncResource(Resource):
    @swag_from(get_request_parser_doc_dist("sync wifiuser from alopex", ["wifiUser"], syncuser_args(False)))
    def get(self):
        args = syncuser_args()
        return ApiResponse(getUsersBySystime(args.systime))


api.add_resource(wifiUserResource,'/wifiuser')
api.add_resource(wifiUserSyncResource,'/wifiusersync')
api.add_resource(wifiUserResources,'/wifiuser/<string:id>')
api.add_resource(SearchWifiUserResource,'/searchwifiuser')