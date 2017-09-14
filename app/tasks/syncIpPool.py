import socket,threading
from config import Config
from app import create_app
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
def syncSingleIp(ip,app):
    with app.app_context():
        q=ipPool.query.filter(ipPool.ip==ip).first()
        if not q:
            q = ipPool()
        if scanSingleHost(ip) == 0:
            q.status="used"
        else:
            q.status="unUsed"
        q.ip=ip
        q.save()
        print "sync {} success".format(ip)
        return None
def syncIp():
    ips = []
    app=create_app()
    for ip in Config.IPPOOL:
        for i in range(7,254):
            ips.append("192.168.{}.{}".format(ip,str(i)))
    for ip in ips:
        t=threading.Thread(target=syncSingleIp,args=(ip,app))
        t.start()
    return None



