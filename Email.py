# -*- coding: utf-8 -*-
#
# @author: Toso
# @created: Sun Sep 30 2018 08:41:12 GMT+0800 (中国标准时间)
# @comment: ______________
#
 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time
import config

def sendmail():
    # SMTP 服务
    mail_host = "smtp.126.com"  #设置服务器
    mail_port = 25
    mail_user = ""    #用户名
    mail_pass = ""   #口令 

    #收发信息
    FromEmail = 'tipinfo@126.com'
    ToEmails = [config.Email,]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    EmailTitle = '12306有票了'
    EmailContent = '快来付款！'

    msg = MIMEMultipart()
    msg['From'] = "{}".format(FromEmail)
    msg['To'] = ",".join(ToEmails)
    msg['Subject'] = EmailTitle

    msg.attach(MIMEText(EmailContent, 'plain', 'utf-8'))

    #attach1 = MIMEText(open('f:\getweather.log', 'rb').read(), 'base64', 'utf-8')
    #attach1["Content-Type"] = 'pplication/octet-stream'
    #attach1["Content-Disposition"] = 'attrachment;filename="getweather.txt"'
    #msg.attach(attach1)
    
    try:
        server = smtplib.SMTP(mail_host, mail_port) 
        server.set_debuglevel(1)    
        server.login(mail_user,mail_pass) 
        server.sendmail(FromEmail, ToEmails, msg.as_string())
        server.quit()
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print "Error: 无法发送邮件"
        print e
