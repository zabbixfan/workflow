import socket,threading
from config import Config
from app.models.ipPool import ipPool

def scanSingleHost(ip):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(Config.SOCKET_TIMEOUT)
    try:
        s.connect((ip,22))
        res = 0
    except Exception,e:

        if str(e).endswith('Connection refused'):
            res = 0
        else:
            res = 1
    finally:
        s.close()
    return res
def syncSingleIp(ip):
    q=ipPool.query.filter(ipPool.ip==ip).first()
    if not q:
        q = ipPool()
    if scanSingleHost(ip) == 0:
        q.isUsed="true"
    else:
        q.isUsed="false"
    q.ip=ip
    q.save()
    print "sync {} success".format(ip)
    return None
def syncIp():
    ips = []
    threads = []
    for ip in Config.IPPOOL:
        for i in range(7,254):
            ips.append("192.168.{}.{}".format(ip,str(i)))
    for ip in ips:
        q=ipPool.query.filter(ipPool.ip==ip).first()
        if not q:
            q = ipPool()
        if scanSingleHost(ip) == 0:
            q.isUsed="true"
        else:
            q.isUsed="false"
        q.ip=ip
        q.save()
        print "sync {} success".format(ip)
    return None
# print syncIp()

