#!coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from app.common.httpHelp import httpRequset
r = httpRequset(uri='/api/projectgroups')
data = {"projectDescription": "", "projectType": "Python:Flask", "name": "jumpecs", "domainName": "jumpecs", "projectName": "jumpecs", "projectGroupName": "DevOps", "owner": "a6a567faece311e6a38aac87a304fa2e", "createGit": true}
print r.content
# if r.status_code < 300:
#     ids = [item['id'] for item in r.json()['data'] if item['name'] == data['projectGroupName']]
#     if ids:
#         gid = ids[0]
#         payload = {
#             'name': data['projectName'],
#             'groupId': gid,
#             'describe': data['projectDescription'],
#             'projectType': data['projectType'],
#             'manager': data['owner']
#             # 'repoUrl': repoUrl
#         }
#         r = httpRequset(uri='/api/projects', data=payload, method='post')