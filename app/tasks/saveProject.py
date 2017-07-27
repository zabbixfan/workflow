#!coding:utf-8
import re

import consul
from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from zerorpc import Client

from app.common.httpHelp import httpRequset

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


def saveProjcetToConsul(pid):
    BasekitClient = Client(
        "tcp://192.168.255.170:3200", timeout=3000, passive_heartbeat=True)
    c=consul.Consul()
    res = BasekitClient.GetProjectInfo(pid)
    print res
    port = 8000+int(pid)
    projectName = res['name']
    c.kv.put('services/{}/port'.format(projectName),str(port))
    for environment in res["environment"]:
        for ip in environment["devices"]:
            pstring = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            pattern=re.compile(pstring)
            match = pattern.search(ip["name"])
            ip = str(match.group())
            # for key in ['status','unhealth','health']:
            c.kv.put('services/{}/{}/{}/status'.format(projectName,environment['envFlag'],ip),'')
            c.kv.put('services/{}/{}/{}/isCheck'.format(projectName,environment['envFlag'],ip),'True')
        if not environment["devices"]:
            c.kv.put('services/{}/{}'.format(projectName,environment['envFlag']),'')
    return None


def saveProjects():
    r = httpRequset(uri='/api/projects')
    projects = r.json()['data']
    for project in projects:
        if project['type'].startswith('Java'):
             saveProjcetToConsul(project['id'])
