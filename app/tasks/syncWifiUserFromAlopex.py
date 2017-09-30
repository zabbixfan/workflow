#!coding:utf-8
from app import celery
from app.common.httpHelp import getUserBySystime
from app.models.wifiUser import radCheck
from app.common.time_helper import current_datetime,datetime_to_timestamp
import datetime,time
@celery.task()
def syncFromAlopex(sysTime=datetime_to_timestamp(current_datetime()-datetime.timedelta(days=1))):
    users = radCheck.query.all()
    allEmployees = [r for r in getUserBySystime() if r['status']=='regular']
    for user in users:
        if user.username not in [em['loginName'] for em in allEmployees]:
            radCheck.delete(user)
            users.remove(user)
    userNames = [u.username for u in users ]
    syncEmployees = [r for r in getUserBySystime(sysTime) if r['status']=='regular']
    for employee in syncEmployees:
        print employee
        if employee['loginName'] not in userNames:
            addUser = radCheck()
            addUser.username = employee['loginName']
            addUser.value = 'TopsTech001'
            addUser.save()
            print "add user {}".format(employee['loginName'])
    return {}