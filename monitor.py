#!/usr/bin/env python
#coding=utf-8

import time
import requests
import json
from config import Config




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

    r = requests.post(Config.OPEN_FALCON_AGENT_URL, data=json.dumps(payload))

