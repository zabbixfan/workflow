#!coding:utf-8
import json
from app.common.httpHelp import httpRequset
from config import Config
from app import logger
from app.common.ApiResponse import ResposeStatus
from zerorpc import Client
import re

def getUserId(username):
    current = 1
    total = 1
    pageSize = 100
    userid = []
    while current <= total:
        uri = '/api/v4/users?per_page={}&page={}'.format(pageSize, current)
        result = httpRequset(uri=uri, method="get",url=Config.CODEHUB_URL)
        total = int(result.headers['X-Total-Pages'])
        current += 1
        userid.extend([user["id"] for user in result.json() if user["username"] in username])
    return userid
def createCMDBGroup(name,leader):
    #创建cmdb组
    uri = '/api/projectgroups'
    payload = {
        'name': name,
        'manager': leader
    }
    r = httpRequset(uri=uri,data=payload,method='post')
    if r.status_code > 300:
        return {'message':'create cmdbgroup failed'},ResposeStatus.ParamFail
    rolemembers=[
        {
            "inherit":False,
            "role_code": "Manager",
            "role_name": "负责人",
            "members": []
        }
    ]
    BasekitClient = Client(Config.ONEKIT_RPC, timeout=3000, passive_heartbeat=False)
    try:
        BasekitClient.AddGroup(name,0,rolemembers)
    except Exception as e:
        logger().info("create onekit group {}".format(e))
    #创建onekit组
    return 'create success',ResposeStatus.Success
def createCodeHubGroup(name,path,members):
    #创建group
    uri = '/api/v4/groups'
    payload = {
        'name': name,
        'path': path,
        'description': 'cmdbgroup'
    }
    r = httpRequset(uri=uri,method='post',params=payload,url=Config.CODEHUB_URL)
    if r.status_code>300:
        logger().error('create codehub group failed ,{},{}'.format(json.dumps(payload),r.content))
        return {'message':'创建codehub组失败'},ResposeStatus.ParamFail
    else:
        #如有成员，则加入
        if members:
            gid = r.json()['id']
            userId = getUserId(members)
            for id in userId:
                uri = '/api/v4/groups/{}/members'.format(gid)
                data = {
                    "user_id": id,
                    "access_level": 30
                }
                r = httpRequset(uri=uri, data=data, method="post",url=Config.CODEHUB_URL)
                if r.status_code < 300:
                    print "add user ok"
                else:
                    print "{}:{}".format(id, r.content)
    return 'create success',ResposeStatus.Success

def projectList():
    groups=[]
    r = httpRequset(uri='/api/select/projectgroups')
    if r.status_code == 200:
        groups = [group['name'] for group in r.json()['data']]
    return groups
def createProjectGroup(name,leader,groupType,path,members):
    error = False
    if groupType == 'all' or groupType == 'codehub':
        param = re.compile('^[a-zA-Z][a-zA-Z0-9\-]+[a-z0-9]$')
        if not param.match(path):
            error = True
    if error == True:
        return {'message':'path参数错误'},ResposeStatus.ParamFail
    if groupType == 'all':
        res,status = createCMDBGroup(name,leader)
        if status != ResposeStatus.Success:
            return res,status
        res,status = createCodeHubGroup(name,path,members)
    if groupType == 'cmdb':
        res,status = createCMDBGroup(name,leader)
    if groupType == 'codehub':
        res,status = createCodeHubGroup(name,path,members)
    return res,status
