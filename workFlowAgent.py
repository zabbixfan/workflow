import socket,threading,subprocess,logging,json,os,jinja2
from config import Config
from sqlalchemy import create_engine
from sqlalchemy import Column,String,DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.common.httpHelp import httpRequset
from app.tasks.mailTask import applyMail
serverPort = Config.WORKFLOW_AGENT_PORT
# serverPort = 6212
allowHost = ['192.168.6.120','192.168.255.1','192.168.99.219']
eng = create_engine("mysql+mysqldb://root:zxc123zxc@192.168.7.60/workflow?charset=utf8mb4")
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

    def save(self,wait_commit=False):
        # if not self.id:
        #     self.id=uuid().get_hex()
        session.add(self)
        if wait_commit:
            session.flush()
        else:
            session.commit()
    @staticmethod
    def commit():
        session.commit()

logging.basicConfig(
    level=logging.DEBUG,
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
        return "tomcat"

def restartCommand(task,hostFile):
    print json.dumps(task,indent=4)
    success = True
    for serv in task['data']['restartProject']:
        name,env,ip = serv.split('/')
        type = getProjectType(name)
        if type == "Java:War":
            projectType = "tomcat"
        elif type in ["Java:Jar","Java:HttpJar"]:
            projectType = "java"
        projectName = name.lower().replace("-","")
        cmd = 'pyenv activate workflow && /Users/manatee/.pyenv/shims/ansible -i {} {} -m shell -a "/etc/init.d/{}-{} restart" -u root '.format(hostFile,ip,projectType,projectName)
        print cmd
        p = subprocess.Popen(["/bin/bash", "-l", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        res, _ = p.communicate()
        print res
        if res.find('is running with pid:') == -1:
            success = False
            logging.error("".format(task['id'],res))
    if success:
        q = session.query(Tickets).filter(Tickets.id == task['data']['id']).first()
        q.status = 'Complete'
        q.commit()
        toUser = Config.AUDITOR
        toHander = Config.AUDITORHANDER
        print task['email']
        print toUser
        if task['email'] not in toUser:
            toUser.append(task['email'])
            toHander.append((task['requestMan'], task['email']))
            print toUser
            print toHander
        content = {
            "title": "Workflow工单申请",
            "content": "<h4>您有一个新的工单已完成，服务已重启</h4>"
        }
        applyMail(toUser=toUser, toHander=toHander, mailArgs=content)

def workFunction(sock,addr):
    if addr[0] not in allowHost:
        sock.sendall("not allow")
        sock.close()
        return None
    else:
        try:
            data = sock.recv(1024)
            sock.send("recevice data complate")
        except Exception as e:
            logging.info(str(e))
            print str(e)
        finally:
            sock.close()
    if data:
        task = json.loads(data)
        ips = []

        if task["type"] == 'restartProject':
            for serv in task['data']['restartProject']:
                ips.append('{}\n'.format(serv.split('/')[-1]))
                ips = list(set(ips))
            if not os.path.isdir("{}/{}".format('runDir', task['id'])):
                os.makedirs("{}/{}".format('runDir', task['id']))
            hostFile = "{}/{}/hosts".format('runDir', task['id'])
            with open("{}/{}/hosts".format('runDir', task['id']),'w+') as f:
                f.writelines(ips)
            print hostFile
            restartCommand(task,hostFile)


def agent():
    s = socket.socket()
    s.bind(('0.0.0.0',serverPort))
    s.listen(1024)
    while True:
        c , addr = s.accept()
        t = threading.Thread(target=workFunction,args=(c,addr))
        t.start()

if __name__ == '__main__':
    agent()
