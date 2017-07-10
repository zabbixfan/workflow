# -*- coding: utf-8 -*-
from app.common.EmailOperator import SendEmail
from jinja2 import *
from app import celery
import os

@celery.task()
def applyMail(mailtitle='Workflow工单申请',toUser=['songcheng3215@tops001.com'],toHander=None,mailArgs={'content':'','title':''}):
    temp = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
    env = Environment(loader=FileSystemLoader(temp))
    template = env.get_template("mail.html")
    email_tmplate=template.render(content=mailArgs["content"],title=mailArgs["title"])
    SendEmail(to_addrs=toUser,from_name='Workflow工单',title=mailtitle,msg=email_tmplate,type='html',toHander=toHander)
