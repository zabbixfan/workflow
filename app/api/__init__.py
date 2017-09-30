#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Api

api = Api(prefix='/api', catch_all_404s=True)

import demo,user,tickets,serviceStatus,ticketLogs,projectGroup,ipPool,webHook,kvm,wifiUser