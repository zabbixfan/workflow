from app.common.httpHelp import httpRequset
from config import Config
from app.common.cacheWithTime import cache
# @cache(86400)
def getProjectType(projectId):
    res = httpRequset(url=Config.CMDB_URL,uri='/api/project/{}'.format(projectId))
    # print res.json()
    return res.json()['data']['projectType']
