#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask import g,jsonify,request
from flask_restful import Resource, reqparse,inputs
from ..common.ApiResponse import ApiResponse, ResposeStatus
from ..common.alopex_auth_sdk import AccessTokenModel
from app.common.api_doc_helper import get_request_parser_doc_dist
from app.common.AuthenticateDecorator import need_user
from app.domains.projectGroups import projectList,createProjectGroup
from flasgger import swag_from

def get_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    return rp.parse_args() if return_parse_args else rp

def post_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("name",required=True,nullable=False)
    rp.add_argument("groupType",required=True,nullable=False)
    rp.add_argument("groupPath",required=True,type=inputs.regex('^[a-zA-Z][a-zA-Z0-9\-]+[a-z0-9]$'))
    rp.add_argument("members",required=True,default=[],action='append')
    return rp.parse_args() if return_parse_args else rp

class projectGroups(Resource):
    @swag_from(get_request_parser_doc_dist("get grouplist", ["projectGroup"], get_args(False)))
    @need_user()
    def get(self):
        return ApiResponse(projectList())

    @swag_from(get_request_parser_doc_dist("add a group", ["projectGroup"], post_args(False)))
    @need_user()
    def post(self):
        args = post_args()
        return ApiResponse(createProjectGroup(name=args.name,groupType=args.groupType,path=args.groupPath,members=args.members))

api.add_resource(projectGroups,'/projectgroups')

