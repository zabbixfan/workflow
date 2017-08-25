#!coding:utf-8
import re
import consul
from zerorpc import Client
from app.common.cmdb_sdk import getProjectType
from app.common.httpHelp import httpRequset
from app import celery
from config import Config


def saveProjcetToConsul(pid):
    c=consul.Consul()
    BasekitClient = Client(Config.ONEKIT_RPC, timeout=3000, passive_heartbeat=False)
    res = BasekitClient.GetProjectInfo(pid)
    print res
    port = 8000+int(pid)
    projectType = getProjectType(pid)
    projectName = res['name']
    c.kv.put('services/{}/port'.format(projectName),str(port))
    c.kv.put('services/{}/type'.format(projectName),projectType)
    for environment in res["environment"]:
        for ip in environment["devices"]:
            pstring = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            pattern=re.compile(pstring)
            match = pattern.search(ip["name"])
            ip = str(match.group())
            # for key in ['status','unhealth','health']:
            c.kv.put('services/{}/{}/{}/status'.format(projectName,environment['envFlag'],ip),'ok')
            c.kv.put('services/{}/{}/{}/isCheck'.format(projectName,environment['envFlag'],ip),'True')
        if not environment["devices"]:
            c.kv.put('services/{}/{}'.format(projectName,environment['envFlag']),'')
    return None

@celery.task()
def saveProjects():
    c=consul.Consul()
    c.kv.delete('services/',recurse=True)
    r = httpRequset(uri='/api/projects')
    projects = r.json()['data']
    for project in projects:
        if project['type'].startswith('Java'):
             saveProjcetToConsul(project['id'])
