#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask_restful import Resource, reqparse
from ..common.ApiResponse import ApiResponse
from ..common.alopex_auth_sdk import AccessTokenModel
from app.common.api_doc_helper import get_request_parser_doc_dist
from flasgger import swag_from

def post_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("accesstoken", type=unicode, required=True, nullable=False)
    return rp.parse_args() if return_parse_args else rp


class UserInfo(Resource):
    @swag_from(get_request_parser_doc_dist("get userinfo",["Users"],post_args(False)))
    def post(self):
        args = post_args()
        rel = AccessTokenModel.token2cls(args.accesstoken)
        return ApiResponse(rel.user if rel else rel)

api.add_resource(UserInfo,'/userinfo')