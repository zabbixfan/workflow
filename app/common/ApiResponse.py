#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ApiResult(object):
    def __init__(self, status, message, code):
        self.status_code = code
        self.message = message
        self.restful_status = status


class ResposeStatus(object):
    Success = ApiResult('success', '成功', 200)
    ParamFail = ApiResult("fail", "params not invaild", 400)
    AuthenticationFailed = ApiResult("verify fail", "身份失效", 401)
    Powerless = ApiResult("power less", "没有权限执行该操作", 403)
    SignFail = ApiResult("sign failed", "sign error", 403)

def ApiResponse(obj=None, status=ResposeStatus.Success):
    return {
                "data": obj,
                "message": status.message,
                "status": status.restful_status
           }, status.status_code