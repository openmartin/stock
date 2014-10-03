# -*- coding: utf-8 -*-
# 没有做异常处理
# 通过shell脚本监控进程执行，如果
import json
import requests
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.Header import Header
from datetime import datetime, date, timedelta

URL = 'http://webmonitor.dcdn.sandai.net/query_single_device?USERID=160749490&VERSION=1&DCDNID=981B6F9C9A6A254D000148A1'

FROM_MAIL_ADDR = '000000000@yeah.net'
TO_MAIL_ADDR = '000000000@qq.com'

MAIL_NAME = 'smtp.yeah.net'
MAIL_PORT = '25'
MAIL_USER = '000000000'
MAIL_PASS = '000000000'

#监控间隔时间
MONITOR_INTERVAL = 60
#连续N次离线才发送邮件
ERR_HINT_LIMIT = 3

#True running
#False stopped
def test_router():
    r = requests.get(URL)
    router_status = json.loads(r.content)
    print router_status
    if router_status['ON_OFF_STATE'] == 1:
        return True
    else:
        return False

def send_mail():
    smtp = smtplib.SMTP()
    smtp.connect(MAIL_NAME, MAIL_PORT)
    smtp.login(MAIL_USER, MAIL_PASS)
    
    msg = MIMEMultipart()
    msg['Subject'] = Header(u'[迅雷路由离线]发生时间%s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'), charset='UTF-8')
    msg['From'] = FROM_MAIL_ADDR
    msg['To'] = TO_MAIL_ADDR
    msg["Accept-Language"]="zh-CN"
    msg["Accept-Charset"]="ISO-8859-1,utf-8"
    
    
    txt = MIMEText("迅雷路由离线，发生时间%s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'), _subtype='plain',  _charset='UTF-8')
    msg.attach(txt)
    
    smtp.sendmail(FROM_MAIL_ADDR, TO_MAIL_ADDR, msg.as_string())   
    smtp.quit()


if __name__ == '__main__':
    err_count = 0
    on_mode = True
    while True:
        if test_router():
            time.sleep(MONITOR_INTERVAL)
            on_mode = True
            err_count = 0
        else:
            err_count += 1
            time.sleep(MONITOR_INTERVAL)
        
        #连续N次发现路由离线
        if err_count >= ERR_HINT_LIMIT:
            if on_mode == True:
                send_mail()
                on_mode = False
    
    
    