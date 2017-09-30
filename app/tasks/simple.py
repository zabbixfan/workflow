#!coding:utf-8
import sys
reload(sys)
import json
sys.setdefaultencoding('utf-8')
from app.common.httpHelp import httpRequset
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

# CODEHUB_TOKEN = 'imfeye86uxakg8LG8ZYQ'
# CODEHUB_URL = 'https://codehub.tops001.com'
#
# commit ='44967e59'
# pid = 47
# head = {'PRIVATE-TOKEN': CODEHUB_TOKEN}
# uri = "/api/v4/projects/{pid}/repository/commits/{commit}".format(pid=pid,commit=commit)
# url = "{}{}".format(CODEHUB_URL,uri)
# try:
#     r = requests.get(url=url,headers=head)
# except Exception as e:
#     print e
# if r.status_code < 300:
#     print r.json()['message']

# params = {
#     'search': 'BrokerService'
# }
# from config import Config
# head = {'PRIVATE-TOKEN': 'imfeye86uxakg8LG8ZYQ'}
# import requests
# r = requests.get(url='https://codehub.tops001.com/api/v4/groups', params=params, headers=head)
# print r.json()[0]['name']

import Queue
import random
import time
import threading
# q=Queue.Queue()
# def producer():
#     while True:
#         number=random.randint(1,10)
#         q.put(number)
#         time.sleep(1)
#         print 'producer:',number
#     return
#
# def consumer():
#     while True:
#         if not q.empty():
#             item=q.get()
#             print 'consumer:',item
#     return
#
# if __name__ == '__main__':
#     t1=threading.Thread(target=producer)
#     t2=threading.Thread(target=consumer)
#     t1.start()
#     t2.start()



class A(object):
    def foo1(self):
        print "A"
class B(object):
    def foo2(self):
        pass
class C(A):
    def foo1(self):
        print "C"
class D(B, C):
    pass

# d = D()
# d.foo1()

def bob(mylist):
    for i in range(0,len(mylist)-1):
        for j in range(0,len(mylist)-1-i):
            if mylist[j]>mylist[j+1]:
                tmp = mylist[j]
                mylist[j]=mylist[j+1]
                mylist[j+1]=tmp
        print mylist
    return mylist
# m=[1,2,3,4,0,7,3,8,2]
# print bob(m)
import base64
import binascii,hashlib
rel = '{MD5}' + base64.b64encode(binascii.unhexlify(hashlib.md5('10275858').hexdigest()))
print hashlib.md5('10275858').hexdigest()
print binascii.unhexlify(hashlib.md5('10275858').hexdigest())
print rel