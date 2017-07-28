#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask import g,jsonify,request
from flask_restful import Resource, reqparse,inputs
from ..common.ApiResponse import ApiResponse, ResposeStatus
from ..common.alopex_auth_sdk import AccessTokenModel
from app.common.api_doc_helper import get_request_parser_doc_dist
from app.common.AuthenticateDecorator import need_user
from app.domains.ticketLogs import getTicketLog
from flasgger import swag_from

class ticketLog(Resource):
    def get(self,id):
        return ApiResponse(getTicketLog(id))

api.add_resource(ticketLog,'/ticketlog/<string:id>')