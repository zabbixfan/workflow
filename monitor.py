#!/usr/bin/env python
#coding=utf-8

import time
import requests
import json

OPEN_FALCON_AGENT_URL = "http://192.168.3.103:1988/v1/push"
PROJECT_ENV = "GA"
PROJECT_NAME = "brokerService"
PROJECT_IP_ADDR = "192.168.255.20"
PROJECT_CHECK_STATUS = "1"   # 1 正常  0 异常
PROJECT_IP_PORT = 8123


def project_health_check(project,env,status,ip_addr,port):
    ts = int(time.time())
    payload = [
    {
        "endpoint": "%s" % ip_addr,
        "metric": 'project_health_check',
        "timestamp": ts,
        "step": 10,
        "value": status,
        "counterType": "GAUGE",
        "tags": "env=%s,project=%s,port=%s," % (env,project,port),
    }
    ]

    r = requests.post(OPEN_FALCON_AGENT_URL, data=json.dumps(payload))

project_health_check(PROJECT_NAME,PROJECT_ENV,PROJECT_CHECK_STATUS,PROJECT_IP_ADDR,PROJECT_IP_PORT)