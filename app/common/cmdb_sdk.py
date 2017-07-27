from app.common.httpHelp import httpRequset
from config import Config
from app.common.cacheWithTime import cache
@cache(86400)
def getProjectType(projectName):
    res = httpRequset(url=Config.CMDB_URL,uri='/api/projects')
    for project in res.json()['data']:
        if project['name'] == projectName:
            return project['type']
    else:
        return "tomcat"