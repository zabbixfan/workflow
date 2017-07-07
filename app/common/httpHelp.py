from .alopex_auth_sdk import SignatureGeneration
from config import Config
import requests
def httpRequset(uri,method='get',url=None,headers=None,params=None,data=None,secret_key=""):
    if url is None:
        url = Config.CMDB_URL
    fullurl = url + uri
    if data:
        sign = SignatureGeneration(data,secret_key)
    elif params:
        sign = SignatureGeneration(params,secret_key)
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

    res = request[method](url=fullurl, headers=head,params=params,data=data)
    return res