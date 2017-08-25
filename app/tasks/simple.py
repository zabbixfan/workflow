# #!coding:utf-8
# import sys
# reload(sys)
# import json
# sys.setdefaultencoding('utf-8')
# from app.common.httpHelp import httpRequset
# import threading
# from concurrent import futures
# repo_url = "http://admin:admin123@repository.apitops.com/service/local/repositories/snapshots/content"
# url = "http://admin:admin123@repository.apitops.com/service/local/repositories/snapshots/content/com/tops001/topstechfin/"
#
# params={
#     'g':'',
#     'r':'snapshots',
#     'v': '1.0-SNAPSHOT',
#     'a': ''
# }
# headers={
#     'Accept':'application/json'
# }
# r = httpRequset(uri='',url=url,headers=headers)
# print r.json()
# del_urls = []
# versions = ['1.0.1-SNAPSHOT']
# # for path in r.json()['data']:
# #     artifacts = repo_url+ path['relativePath']
# #     for version in versions:
# #         del_url = artifacts + version + '/'
# #         print del_url
# #         del_urls.append(del_url)
# #         t= threading.Thread(target=httpRequset,args=(del_url,))
# #         t.start()
#         # r = httpRequset(uri='',url=del_url,headers=headers,method='delete')
#         #print json.dumps(r.json(), indent=4)
#         #print r.content
# print del_urls
# # with futures.ThreadPoolExecutor(max_workers=10) as excutor:
# #     hosts = [excutor.submit(httpRequset, '','delete', url,headers) for url in del_urls]
# # for future in futures.as_completed(hosts):
# #     pass
# # print r.content
# # print json.dumps(r.json(),indent=4)

#!/usr/bin/python
import os
import json
import requests
import sys

CODEHUB_TOKEN = 'imfeye86uxakg8LG8ZYQ'
CODEHUB_URL = 'https://codehub.tops001.com'

commit ='44967e59'
pid = 47
head = {'PRIVATE-TOKEN': CODEHUB_TOKEN}
uri = "/api/v4/projects/{pid}/repository/commits/{commit}".format(pid=pid,commit=commit)
url = "{}{}".format(CODEHUB_URL,uri)
try:
    r = requests.get(url=url,headers=head)
except Exception as e:
    print e
if r.status_code < 300:
    print r.json()['message']
