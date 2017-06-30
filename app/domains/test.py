#!coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
def _formataddr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
Config={
  'mail_host':'smtp.exmail.qq.com',
  'mail_port':465,
  'mail_user':'songcheng3215@tops001.com',
  'mail_pass':'wwPePF80mSkHNmve',
  'receivers':[_formataddr("胡科<songcheng3215@tops001.com>")]
  #'receivers': ['kakao-ops@tops001.com']
}
def send_mail(to_list,sub,content):
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(sub, 'utf-8')
    msg['From'] = Config['mail_user']
    msg['To'] = ';'.join(to_list)
    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(Config['mail_host'],Config['mail_port'])
        smtpObj.login(Config['mail_user'],Config['mail_pass'])
        smtpObj.sendmail(Config['mail_user'], Config['receivers'], msg.as_string())
        smtpObj.close()
        print "success"
    except Exception,e:
        print e
if __name__=='__main__':
    # with open('templates/index.html','r') as f:
    #     content=f.read()
    # print content
    send_mail(Config['receivers'],'it\'s title胡科',"haha")
