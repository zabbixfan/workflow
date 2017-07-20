#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask_restful import Resource, reqparse
from ..common.ApiResponse import ApiResponse
from ..common.alopex_auth_sdk import AccessTokenModel
from app.common.api_doc_helper import get_request_parser_doc_dist
from flasgger import swag_from
# from app.tasks.portScan import checkServices
from app.domains.services import ServicesList

def get_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('offset',type=int,default=0)
    rp.add_argument('limit',type=int,default=20)
    rp.add_argument('keyword',default=[],action=True)
    rp.add_argument('env',type=unicode,default=[],action=True)
    return rp.parse_args() if return_parse_args else rp


class getServiceInfo(Resource):
    def get(self):
        args = get_args()
        key = args.keyword if isinstance(args.keyword,list) else [args.keyword]
        envs = args.env if isinstance(args.env,list) else [args.env]
        return ApiResponse(ServicesList(keyword=key,envs=envs,offset=args.offset,limit=args.limit))


class getServiceName(Resource):
    def get(self):
        pass


api.add_resource(getServiceInfo,'/services')