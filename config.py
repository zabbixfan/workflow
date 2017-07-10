#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class Config_Dev(object):
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 要比数据库 wait_timeout 参数要小
    SQLALCHEMY_POOL_RECYCLE = 50
    SQLALCHEMY_ECHO = False
    ID_TOKEN_DEFAULT_EXPIRES = 8640000

    ACCESS_TOKEN_DEFAULT_EXPIRES = 86400
    CORS_ORIGINS = [*]

    APP_ID = ""
    APP_SECRET = ""

    AUTH_SERVER_HOST = ""
    AUTH_SERVER_LOGIN_URL = ""
    AUTH_SERVER_LOGOUT_URL = ""
    Powers = {}

    EMALL_USER = ""
    EMALL_PASSWORD = ""
    EMALL_SMTP_HOST = "smtp.exmail.qq.com"
    EMALL_SMTP_PORT = 465
    AUDITOR = ['']
    AUDITORHANDER = [('','')]

    CELERY_TASK_SERIALIZER = 'json'
    TEMPLATE_DIR = ''
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_IGNORE_RESULT = True
    CELERY_BROKER_URL = ""
    CELERY_RESULT_BACKEND = ""
    # CELERYD_MAX_TASKS_PER_CHILD = 50
    # CELERYBEAT_SCHEDULE = {
    #     'syncSearchCodeStatus': {
    #         'task': 'app.tasks.syncTasks.syncSearchCodeStatus',
    #         'schedule': timedelta(seconds=20)
    #     },
    # }
    CMDB_URL = ''
    CODEHUB_TOKEN = ''
    CODEHUB_URL = ''
    PACIFIC_URL = ''


class Config_Ga(Config_Dev):
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_ECHO = False
    AUTH_SERVER_HOST = ""
    AUTH_SERVER_LOGIN_URL = ""
    AUTH_SERVER_LOGOUT_URL = ""

    APP_ID = ""
    APP_SECRET = ""


Config = Config_Dev

if os.environ.get('ENV_CODE') == "GA":
    Config = Config_Ga
