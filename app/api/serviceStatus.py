#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask import jsonify
from flask_restful import Resource, reqparse
from ..common.ApiResponse import ApiResponse
from ..common.alopex_auth_sdk import AccessTokenModel
from app.common.api_doc_helper import get_request_parser_doc_dist
from flasgger import swag_from
# from app.tasks.portScan import checkServices
from app.domains.services import ServicesList,getServiceInfo
from app.tasks.saveProject import saveProjects

def get_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('offset',type=int,default=0)
    rp.add_argument('limit',type=int,default=20)
    rp.add_argument('keyword[]',dest="keyword",action="append")
    rp.add_argument('env[]',dest="env",default=[],action="append")
    rp.add_argument('status',default='')
    return rp.parse_args() if return_parse_args else rp


class ServicesFromConsul(Resource):
    def get(self):
        args = get_args()
        return ApiResponse(ServicesList(keyword=args.keyword,envs=args.env,offset=args.offset,limit=args.limit,status=args.status))

class getServiceByKeyword(Resource):
    def get(self):
        rp = reqparse.RequestParser()
        rp.add_argument('keyword', default="", action=True)
        key = rp.parse_args().keyword
        res = getServiceInfo(key)
        return jsonify(res)


class syncProjectToConsul(Resource):
    def get(self):
        import threading
        t= threading.Thread(target=saveProjects)
        t.start()
        return ApiResponse('')


api.add_resource(ServicesFromConsul, '/services')
api.add_resource(getServiceByKeyword,'/service')
api.add_resource(syncProjectToConsul, '/syncconsul')