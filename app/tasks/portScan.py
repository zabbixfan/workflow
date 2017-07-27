#!coding:utf-8
# from app.models.projectInfo import ProjectInfo
from app.tasks.cacheWithTime import cache
import socket
from config import Config
import consul,time
from concurrent import futures
import monitor
import threading
c = consul.Consul()
@cache(timeout=3600)
def getInfo():
    _,services = c.kv.get('services/',recurse=True)
    projects = []
    for s in services:
        key = s['Key']
        if key.endswith('status'):
            project = key.split('/')[1]
            _,port = c.kv.get('services/{}/port'.format(project))
            port = port['Value']
            projects.append((project,key.split('/')[2],key.split('/')[3],port))
    return projects


def singleCheck(service):
    port = int(service[3])
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(Config.SOCKET_TIMEOUT)
    try:
        s.connect((service[2],port))
        res = 'success'
    except Exception,e:
        # print "{}:{},{}".format(ip,port,e)
        res = 'failed'
    finally:
        s.close()
    status = 1 if res == 'success' else 0
    #print res
    #monitor.project_health_check(service[0],service[1],status,service[2],service[3])

    # t = threading.Thread(target=monitor.project_health_check,args=(service[0],service[1],status,service[2],service[3]))
    # t.start()
    return res

def clearCounter(project,env,ip):
    c.kv.put('services/{}/{}/{}/health'.format(project,env,ip),'0')
    c.kv.put('services/{}/{}/{}/unhealth'.format(project, env, ip), '0')
def writeToConsul(service):
    res = singleCheck(service)
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


def checkServices():
    services = getInfo()
    worker = min(Config.SCAN_WORKER,len(services))
    print worker
    with futures.ThreadPoolExecutor(max_workers=worker) as excutor:
        res = excutor.map(writeToConsul,services)
    return {}

    # for service in services:
    #     writeToConsul(service)



while True:
    start = time.time()
    checkServices()
    print time.time() - start
    time.sleep(Config.INTERVAL)
    # event.wait(3)


