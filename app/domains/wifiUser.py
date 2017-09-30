from app.models.wifiUser import radCheck
from app.common.pageHelper import PageResult
from app.common.httpHelp import getUserInfoByName
from app.common.ApiResponse import ResposeStatus
from app.tasks.syncWifiUserFromAlopex import syncFromAlopex
from app.common.time_helper import strtime_to_timestamp
def wifiUserList(keyword=None,offset=0,limit=20):
    q=radCheck.query
    if keyword:
        key = keyword.replace("%", "").replace("_", "").replace("*", "")
        key = '%{}%'.format(key)
        q=q.filter(radCheck.username.like(key))
    return PageResult(q.order_by(radCheck.id.desc()), limit, offset).to_dict(lambda data: {
        "id": data.id,
        "name": data.username
    })

def addWifiUser(username='',value=''):
    if username:
        if getUserInfoByName(username):
            q=radCheck.query.filter(radCheck.username == username).first()
            if not q:
                user = radCheck()
                user.username = username
                user.value = value
                user.save()
                return "add wifiuser success",ResposeStatus.Success
        else:
            return "user not in alopex",ResposeStatus.ParamFail
    else:
        return "please input a vaild username",ResposeStatus.ParamFail
def changeWifiUserPassWord(id=None,value=None):
    if id and value:
        q = radCheck.query.filter(radCheck.id == id).first()
        if q:
            q.value = value
            q.commit()
            return "change wifiuser password success",ResposeStatus.Success
        else:
            return "user not exist",ResposeStatus.ParamFail
    else:
        return "please input vaild id and value",ResposeStatus.ParamFail
def deleteWifiUserPassWord(id=None):
    if id:
        q = radCheck.query.filter(radCheck.id == id).first()
        if q:
            q.delete(q)
            return "delete wifiuser success", ResposeStatus.Success
        else:
            return "user not exist",ResposeStatus.ParamFail
    else:
        return "please input vaild id",ResposeStatus.ParamFail
def searchWifiUsersByName(name):
    if name:
        q = radCheck.query.filter(radCheck.username.like(name)).first()
        if q:
            return {
                'username':q.username,
                'value':q.value,
                'id':q.id
            }
    return {}

def getUsersBySystime(sysTime):
    if sysTime:
        sysTime = strtime_to_timestamp("{} 00:00:00.000".format(sysTime))
    syncFromAlopex.delay(sysTime)
    return {
        'data':'begin syncing..'
    }