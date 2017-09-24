#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask import g,jsonify,request
from flask_restful import Resource, reqparse,inputs
from ..common.ApiResponse import ApiResponse, ResposeStatus
from app.common.api_doc_helper import get_request_parser_doc_dist
from app.common.AuthenticateDecorator import need_user
from app.domains.ipPool import getIpPool,deleteIp
from app.tasks.syncIpPool import syncIp
from flasgger import swag_from
import threading

def post_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("accesstoken", type=unicode, required=True, nullable=False)
    return rp.parse_args() if return_parse_args else rp

def deleteip_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("ip", type=unicode, required=True, nullable=False)
    return rp.parse_args() if return_parse_args else rp

def get_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument('keyword',default='')
    return rp.parse_args() if return_parse_args else rp


class ipPool(Resource):
    @swag_from(get_request_parser_doc_dist("get ipPool",["ipPool"],get_args(False)))
    def get(self):
        args=get_args()
        return ApiResponse(getIpPool(args.keyword))
    def post(self):
        args=deleteip_args()
        return ApiResponse(deleteIp(args.ip))
class syncIpPool(Resource):
    @swag_from(get_request_parser_doc_dist("syncipPool", ["ipPool"]))
    def get(self):
        return ApiResponse(syncIp())


api.add_resource(ipPool,'/ippool')
api.add_resource(syncIpPool,'/syncip')