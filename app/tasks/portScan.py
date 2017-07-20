#!coding:utf-8
# from app.models.projectInfo import ProjectInfo
from app.tasks.saveProject import *
from app.tasks.cacheWithTime import cache
import socket
from config import Config
import consul,time
from concurrent import futures
import threading
@cache(timeout=3600)
def getInfo():
    projects = session.query(ProjectInfo).all()
    return [(project.project,project.env,project.ip,project.port)for project in projects]

c = consul.Consul()
def singleCheck(ip,port):
    port = int(port)
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(Config.SOCKET_TIMEOUT)
    try:
        s.connect((ip,port))
        res = 'success'
    except Exception,e:
        # print "{}:{},{}".format(ip,port,e)
        res = 'failed'
    finally:
        s.close()
    return res

def clearCounter(project,env,ip):
    c.kv.put('services/{}/{}/{}/health'.format(project,env,ip),'0')
    c.kv.put('services/{}/{}/{}/unhealth'.format(project, env, ip), '0')
def writeToConsul(service):
    if service[2]:
        res = singleCheck(service[2], service[3])
        if res == "success":
            _,v = c.kv.get('services/{}/{}/{}/health'.format(service[0],service[1],service[2]))

            if v:
                v = str(int(v['Value'])+1)
            else:
                v = str(0)
            c.kv.put('services/{}/{}/{}/health'.format(service[0], service[1], service[2]), v)
        elif res == "failed":
            _,v = c.kv.get('services/{}/{}/{}/unhealth'.format(service[0],service[1],service[2]))
            if v:
                v = str(int(v['Value']) + 1)
            else:
                v = str(0)
            c.kv.put('services/{}/{}/{}/unhealth'.format(service[0], service[1], service[2]), v)
        _,health = c.kv.get('services/{}/{}/{}/health'.format(service[0],service[1],service[2]))
        _,unhealth = c.kv.get('services/{}/{}/{}/unhealth'.format(service[0],service[1],service[2]))
        health = int(health['Value']) if health else 0
        unhealth = int(unhealth['Value']) if unhealth else 0
        if health >= Config.HEALTH_THRESHOLD or unhealth >=Config.UNHEALTH_THRESHOLD:
            if health >= Config.HEALTH_THRESHOLD:
                c.kv.put('services/{}/{}/{}/status'.format(service[0], service[1], service[2]), 'ok')
            if unhealth >= Config.UNHEALTH_THRESHOLD:
                c.kv.put('services/{}/{}/{}/status'.format(service[0], service[1], service[2]), 'failure')
            clearCounter(service[0],service[1],service[2])
    else:
        c.kv.put('services/{}/{}'.format(service[0],service[1]),'')

def checkServices():
    services = getInfo()
    worker = max(Config.SCAN_WORKER,len(services))
    print worker
    with futures.ThreadPoolExecutor(max_workers=worker) as excutor:
        res = excutor.map(writeToConsul,services)
    return {}

    # for service in services:
    #     writeToConsul(service)



# while True:
#     start = time.time()
#     event = threading.Event()
#     checkServices()
#     print time.time() - start
#     time.sleep(3)
#     # event.wait(3)



