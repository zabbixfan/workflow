#!coding:utf-8
import requests,json,re
from app.common.httpHelp import httpRequset
from sqlalchemy import create_engine
from sqlalchemy import Column,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
eng = create_engine("mysql+mysqldb://root:zxc123zxc@192.168.7.60/workflow?charset=utf8mb4")
Model = declarative_base()
Session  = sessionmaker(bind=eng)
session = Session()
class ProjectInfo(Model):
    __tablename__ = "workflow_projectInfo"
    pid = Column(String(255))
    project = Column(String(255), primary_key=True)
    env = Column(String(32), primary_key=True)
    ip = Column(String(255), primary_key=True)
    port = Column(String(32),default="")
    def save(self,wait_commit=False):
            session.add(self)
            if wait_commit:
                session.flush()
            session.commit()
    @staticmethod
    def commit():
        session.commit()
    def __repr__(self):
        return 'projectInfo<project={},env={}>'.format(self.project,self.env)
def getByid(pid):
    pid = pid
    ipInfo = {}
    url = "http://onekit.apitops.com:5200/api/account/login"
    data = {
        "name": "songcheng3215",
        "password": "Sc10275858"
    }
    r = requests.post(url=url, data=data)
    if r.status_code == 200:
        token = r.json()["data"]["token"]
        url = "http://onekit.apitops.com:5200/api/project/{}".format(pid)
        headers = {
            "Authorization": token
        }
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            res = r.json()["data"]
            port = 8000+int(pid)
            projectName = res['name']
            for environment in res["environment"]:
                ips = []
                for ip in environment["devices"]:
                    pstring = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
                    pattern=re.compile(pstring)
                    match = pattern.search(ip["name"])
                    ips.append(str(match.group()))
                    ip = str(match.group())
                    p = session.query(ProjectInfo).filter(ProjectInfo.pid == pid).filter(ProjectInfo.ip == ip).first()

                    if not p:
                        p = ProjectInfo()
                    p.ip = ip
                    p.project = projectName
                    p.port = port
                    p.pid = pid
                    p.env = environment['envFlag']
                    session.add(p)
                    session.commit()
                    # p.save()
                if not environment["devices"]:
                    p = session.query(ProjectInfo).filter(ProjectInfo.pid == pid).filter(ProjectInfo.env==environment['envFlag']).first()
                    if not p:
                        p = ProjectInfo()
                    p.ip = ''
                    p.project = projectName
                    p.port = port
                    p.pid = pid
                    p.env = environment['envFlag']
                    p.save()
            return None


def saveProject():
    r = httpRequset(uri='/api/projects')
    projects = r.json()['data']
    for project in projects:
        if project['type'].startswith('Java'):
            getByid(project['id'])
