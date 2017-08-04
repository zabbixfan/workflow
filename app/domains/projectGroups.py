#!coding:utf-8
import json
from app.common.httpHelp import httpRequset
from config import Config
from app import logger
from app.common.ApiResponse import ResposeStatus
def getUserId(username):
    current = 1
    total = 1
    pageSize = 100
    userid = []
    while current <= total:
        uri = '/api/v4/users?per_page={}&page={}'.format(pageSize, current)
        result = httpRequset(uri=uri, method="get")
        total = int(result.headers['X-Total-Pages'])
        current += 1
        userid.extend([user["id"] for user in result.json() if user["username"] in username])
    return userid
def createCodeHubGroup(name,path,members):
    uri = '/api/v4/groups'
    payload = {
        'name': name,
        'path': path,
        'description': 'cmdbgroup'
    }

    r = httpRequset(uri=uri,method='post',params=payload,url=Config.CODEHUB_URL)
    if r.status_code>300:
        logger().error('create codehub group failed ,{},{}'.format(json.dumps(payload),r.content))
        return '创建codehub组失败',ResposeStatus.ParamFail
    else:
        if members:
            gid = r.json()['id']
            userId = getUserId(members)
            for id in userId:
                uri = '/api/v4/groups/{}/members'.format(gid)
                data = {
                    "user_id": id,
                    "access_level": 30
                }
                r = httpRequset(uri=uri, data=data, method="post")
                if r.status_code < 300:
                    print "add user ok"
                else:
                    print "{}:{}".format(id, r.content)
    return 'create success'

def projectList():
    groups=[]
    r = httpRequset(uri='/api/select/projectgroups')
    # print type(r.json())
    if r.status_code == 200:
        groups = [group['name'] for group in r.json()['data']]
    return groups
def createProjectGroup(name,groupType,path,members):
    uri = '/api/v4/users/22'
    r = httpRequset(url=Config.CODEHUB_URL,uri=uri)
    print r.json()
    # if groupType == 'all':
    #     pass
    # if groupType == 'cmdb':
    #     pass
    # if groupType == 'codehub':
    #     res = createCodeHubGroup(name,path,members)
