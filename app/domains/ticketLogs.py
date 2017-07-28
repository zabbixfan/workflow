#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.ticketLogs import TicketLog
from app.common.time_helper import datetime_to_strtime
def getTicketLog(tid):
    res = []
    logs = TicketLog.query.filter(TicketLog.ticketId == tid).all()
    for log in logs:
        res.append({
        "id":log.ticketId,
        "time":datetime_to_strtime(log.time,format_str="%Y-%m-%d %H:%M:%S"),
        "status":log.content
        })
    return res