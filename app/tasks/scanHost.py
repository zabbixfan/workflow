#!coding:utf-8
ips = ['192.168.100.'+str(number) for number in range(1,255)]
# print ips
import socket
from concurrent import futures
linux = []
win = []
def singleCheck(ip):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip,22))
        # print "{}:{},{}".format(ip,22,'success')
        linux.append(ip)
        res = 'success'
    except Exception,e:
        # print "{}:{},{}".format(ip, 22, e)
        res = 'failed'
        # print str(e)
        if str(e).endswith('Connection refused'):
            win.append(ip)
    finally:
        s.close()
    return res
# for i in ips:
#     singleCheck(i)

with futures.ThreadPoolExecutor(max_workers=100) as excutor:
    excutor.map(singleCheck,ips)
print len(linux)
print win
# singleCheck('192.168.100.25')


# import json
# from app.common.ansible_sdk import ansibleRunner
# ips = ['192.168.100.'+str(number) for number in range(1,255)]
# # for ip in ips:
# def single(ip):
#     resources = [{"hostname": ip, "username": "root"}]
#     tqm = ansibleRunner(resources)
#     tqm.run(host_list=[ip], module_name='ping', module_args='')
#     taskResult = tqm.get_result()
#     print json.dumps(taskResult,indent=4)
# with futures.ThreadPoolExecutor(max_workers=100) as excutor:
#     excutor.map(single,ips)