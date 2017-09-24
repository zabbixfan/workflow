# from .alopex_auth_sdk import SignatureGeneration
from api_sign_sdk import SignatureGeneration
from config import Config
import requests
from app.common.cacheWithTime import cache

def httpRequset(uri,url=None,method='get',headers=None,params=None,data=None,secret_key="",jsons=None):
    if url is None:
        url = Config.CMDB_URL
    fullurl = url + uri
    if data:
        sign = SignatureGeneration(data,secret_key)
    elif params:
        sign = SignatureGeneration(params,secret_key)
    elif jsons:
        sign = SignatureGeneration(jsons, secret_key)
    else:
        sign = SignatureGeneration(secret_key=secret_key)

    if sign:
        head = {'PRIVATE-TOKEN': Config.CODEHUB_TOKEN,'X-Signature':sign}
    else:
        head = {'PRIVATE-TOKEN': Config.CODEHUB_TOKEN}
    if headers:
        head.update(headers)
    request = {
        'get': requests.get,
        'post': requests.post,
        'put': requests.put,
        'delete': requests.delete,
    }
    res = request[method](url=fullurl, headers=head,params=params,data=data,json=jsons)
    return res
@cache(timeout=3660)
def getUserInfoByName(name):
    names = {
        'keyword':name
    }
    r=httpRequset(url=Config.AUTH_SERVER_HOST,uri='/api/usersearch',params=names)
    if r.json()['data']['searchData']:
        return r.json()['data']['searchData'][-1]
    return {}

def getNameByPath(name):
    params = {
        'search': name
    }
    r = httpRequset(uri='/api/v4/groups', params=params, url=Config.CODEHUB_URL)
    if r.status_code < 300:
        groupName = r.json()[0]['name']
    else:
        groupName = name
    return groupName

