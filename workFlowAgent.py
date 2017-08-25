#!coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import socket,threading,logging,json,os,jinja2,re
from concurrent import futures
from config import Config
from sqlalchemy import create_engine
from sqlalchemy import Column,String,DATETIME,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.common.httpHelp import httpRequset
from app.common.ansible_sdk import ansibleRunner
from app.tasks.mailTask import applyMail
from app.common.time_helper import current_datetime,strtime_to_datetime
from app.models.servers import *
import datetime
serverPort = Config.WORKFLOW_AGENT_PORT
allowHost = Config.ALLOW_HOST
eng = create_engine(Config.SQLALCHEMY_DATABASE_URI,pool_recycle=55)
Model = declarative_base()
Session  = sessionmaker(bind=eng)
session = Session()


class Tickets(Model):
    __tablename__= "workflow_list"
    id = Column(String(255),primary_key=True)
    name = Column(String(255))
    type = Column(String(255),default="")
    status = Column(String(255),default="")
    requestMan = Column(String(255),default="")
    auditor = Column(String(255),default="")
    executor = Column(String(255),default="")
    email = Column(String(255),default="")
    data = Column(String(65535), default="")
    createTime = Column(DATETIME)
    requestManEng = Column(String(255),default="")
    @staticmethod
    def commit():
        session.commit()

class TicketLog(Model):
    __tablename__ = "workflow_operatelog"
    id = Column(Integer,primary_key=True)
    ticketId = Column(String(255),default="")
    user = Column(String(255),default="")
    time = Column(DATETIME)
    action = Column(String(255),default="")
    content = Column(String(1000),default="")
    @staticmethod
    def commit():
        session.commit()
    def save(self,wait_commit=False):
        # if not self.id:
        #     self.id=uuid().get_hex()
        session.add(self)
        if wait_commit:
            session.flush()
        else:
            session.commit()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s",
    filename="app.log",
    filemode="a+"
)

def getProjectType(projectName):
    res = httpRequset(url=Config.CMDB_URL,uri='/api/projects')
    for project in res.json()['data']:
        if project['name'] == projectName:
            return project['type']
    else:
        return "Java:War"

def writeTicketLog(servcie,tid,result):
    log = TicketLog()
    log.ticketId = tid
    log.time = current_datetime()
    if result['unreachable']:
        log.content = "{}:{}".format(servcie,result['unreachable'])
    elif result['failed']:
        log.content = "{}:{}".format(servcie,result['failed'])
    elif result['success']:
        for k,v in result['success'].items():
            if v['stderr']:
                log.content = "{}:{}".format(servcie,v['stderr'])
                break
            if 'stderr_lines' in v.keys():
                if v['stderr_lines']:
                    log.content = "{}:{}".format(servcie,','.join(v['stderr_lines'][-1]))
                    break
            if v['stdout_lines']:
                log.content = "{}:{}".format(servcie,v['stdout_lines'][-1])
            session.add(log)
            session.commit()
            session.close()
def restartCommand(task):
    logging.warn(json.dumps(task,indent=4))
    success = True
    for serv in task['data']['restartProject']:
        name,env,ip = serv.split('/')
        type = getProjectType(name)
        if type == "Java:War":
            projectType = "tomcat"
        elif type in ["Java:Jar","Java:HttpJar"]:
            projectType = "java"
        projectName = name.lower().replace("-","")
        resources = [{"hostname": ip, "username": "root"}]
        cmd = "/etc/init.d/{}-{} restart".format(projectType,projectName)
        #cmd = "whoami"
        tqm = ansibleRunner(resources)
        tqm.run(host_list=[ip], module_name='shell', module_args=cmd)
        taskResult = tqm.get_result()
        logging.warn(json.dumps(taskResult,indent=4))
        writeTicketLog(serv,task['id'],taskResult)
        if taskResult['failed'] or taskResult['unreachable']:
            success = False
            logging.error("{}:{},{}".format(task['id'],taskResult['failed'],taskResult['unreachable']))
        else:
            status = taskResult['success'][ip]['stdout_lines']
            pattern = re.compile(r'is\srunning\swith\spid\:\s\d+')
            if not pattern.search(status[-1]):
                success = False
                logging.error("{}:{}".format(task['id'],taskResult['success'][ip]))
    if success:
        q = session.query(Tickets).filter(Tickets.id == task['id']).first()
        q.status = 'Complete'
        q.commit()
        toUser = Config.AUDITOR
        toHander = Config.AUDITORHANDER
        logging.warn(task['email'])
        logging.warn(",".join(toUser))
        if task['email'] not in toUser:
            toUser = Config.AUDITOR + [task['email']]
            toHander = Config.AUDITORHANDER + [(task['requestMan'], task['email'])]
        logging.warn(",".join(toUser))
        content = {
            "title": "Workflow工单申请",
            "content": "<p>您的工单{}已完成，服务已重启,请登录workflow查看重启结果<p>".format(task['name'])
        }
        applyMail(toUser=toUser, toHander=toHander, mailArgs=content)

def scanSingleHost(ip,hostList):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(Config.SOCKET_TIMEOUT)
    try:
        s.connect((ip,22))
        hostList.append({
            'ip':ip,
            'system': 'linux'
        })
        res = 'success'
    except Exception,e:
        res = 'failed'
        if str(e).endswith('Connection refused'):
            hostList.append({
            'ip':ip,
            'system': 'win'
            })
    finally:
        s.close()
    return res

def syncSingleHost(data,servers):
    ip = data['ip']
    system = data['system']
    if system == "win":
        server = {
            'system':'win',
            'ip': ip
        }
    if system == 'linux':
        server = {
            'system': 'linux',
            'ip': ip
        }
        resources = [{"hostname": ip, "username": "root"}]
        tqm = ansibleRunner(resources)
        tqm.run(host_list=[ip], module_name='setup', module_args='')
        taskResult = tqm.get_result()
        if taskResult['success']:
            server['taskResult'] = 'success'
            hostInfo = taskResult['success'][ip]['ansible_facts']
            server['os_platform'] = hostInfo['ansible_distribution']
            server['os_name'] = '{} {}'.format(hostInfo['ansible_distribution'],hostInfo['ansible_distribution_version']).lower()
            server['host_name'] = hostInfo['ansible_hostname']
            server['cpu'] = hostInfo['ansible_processor_count']
            server['memory'] = hostInfo['ansible_memtotal_mb']
            server['disk'] =  sum([int(hostInfo["ansible_devices"][i]["sectors"]) * \
                               int(hostInfo["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
                               for i in hostInfo["ansible_devices"] if i[0:2] in ("sd", "ss","xv")])
        else:
            server['taskResult'] = 'failed'
    servers.append(server)

def scanInternal():
    ips = ["192.168.100.{}".format(ip) for ip in range(2,255)]
    hostList=[]
    with futures.ThreadPoolExecutor(max_workers=50) as excutor:
        hosts = [excutor.submit(scanSingleHost,ip,hostList) for ip in ips]
    for future in futures.as_completed(hosts):
        pass
        # print future.result()
        # excutor.map(scanSingleHost,ips)
    print len(hostList)
    servers=[]
    for host in hostList:
        print host['ip']
        syncSingleHost(host,servers)
    print len(servers)
    # print json.dumps({'hostInfo': servers},indent=4)
    return {
        'aliveHost': hostList,
        'hostInfo': servers
    }
def workFunction(sock,addr):
    if addr[0] not in allowHost:
        sock.sendall("not allow")
        sock.close()
        return None
    else:
        try:
            data = sock.recv(1024)
            task = json.loads(data)
            if task["type"] == 'scanInternalDataCenter':
                res=scanInternal()
                sock.sendall(json.dumps(res))
                sock.close()
            else:
                sock.send('recevie data complete')
        except Exception as e:
            logging.info(repr(e))
            print str(e)
        finally:
            sock.close()
    if data:
        task = json.loads(data)
        if task["type"] == 'restartProject':
            print "start restart"
            restartCommand(task)


def agent():
    s = socket.socket()
    s.bind(('0.0.0.0',serverPort))
    s.listen(1024)
    print "workFlowAgent is starting,Listen on 0.0.0.0:{}".format(serverPort)
    while True:
        c , addr = s.accept()
        t = threading.Thread(target=workFunction,args=(c,addr))
        t.start()

if __name__ == '__main__':
    agent()
