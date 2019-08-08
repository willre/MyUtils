#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time       : 2019-07-17 09:57
# @Author     : Barry
# @Site       : 
# @File       : base_mail.py
# @Software   : PyCharm
# Description : 


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage
import time

class Email:
    """
    send email
    """

    def __init__(self, host, port, sender, passwd, reciver):
        """
        初始化
        :param host: 邮件服务地址
        :param port:  邮件服务端口
        :param sender:  发送者账号
        :param passwd:  发送者密码
        :param reciver:  接收人邮件地址列表
        """
        self.host = host
        self.port = port
        self.sender = sender
        self.passwd = passwd
        self.reciver = reciver

        self.msg = MIMEMultipart()
        self.mail_content = ""

    def set_header(self,mail_subject):
        """
        设置 Header
        :param mail_from: 发送者
        :param mail_to:  接受者
        :param mail_subject:  邮件主题
        :return:
        """
        self.msg["From"] = self.sender
        self.msg["To"] = ";".join(self.reciver)
        self.msg["Subject"] = Header(mail_subject, "utf-8").encode()

        pass

    def set_content(self,mail_content, mail_type="plain", encoding="utf-8"):
        """
        设置邮件内容
        :param mail_content: 邮件正文
        :param mail_type: 邮件类型，html或者plain， plain 为纯文本
        :param encoding: 指定编码
        :return:
        """
        content = MIMEText(mail_content+ self.mail_content, mail_type)
        self.msg.attach(content)

        pass

    def attach(self, attatch_file, att_name):
        """
        添加附件
        :param attatch_file: 要添加的文件
        :param att_name:  发送邮件时，指定附件名称
        :return:
        """
        _att_file_content = ""
        try:
            with open(attatch_file, "rb") as f:
                _att_file_content = f.read()
        except Exception as e:
            print(e)
            exit()
        att = MIMEText(_att_file_content,  'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'

        att["Content-Disposition"] = 'attachment; filename="{}"'.format(att_name)

        self.msg.attach(att)

    def attache_img(self, image_filename):
        """
        :param image_filename: 图片文件文件名
        :return:
        """
        img = open(image_filename,"rb")
        img_content = img.read()
        img.close()
        msgImg =  MIMEImage(img_content)
        img_id = time.time()
        msgImg.add_header("Content-ID","<{}>".format(img_id))
        self.mail_content += '<br><img src="cid:{}"></br>'.format(img_id)
        self.msg.attach(msgImg)
        time.sleep(1)

    def send(self):

        """
        发送邮件
        :return:
        """
        # 登录 smtp 服务器
        smtp_ser = smtplib.SMTP_SSL(self.host, self.port)
        try:
            code = smtp_ser.login(self.sender,self.passwd)
            print(code)
        except Exception as e:
            print("Error info：", e)
            exit()
        #(235, b'Authentication successful')

        # 发送内容
        smtp_ser.sendmail(self.sender, self.reciver, self.msg.as_string())

        # 关闭连接
        smtp_ser.close()


if __name__ == '__main__':
    send_info = {
        "mail_host": "smtpdm.aliyun.com",
        "mail_port": 465,
        "mail_user": "username@a.com",
        "mail_pass": "password",
        "sender": "username@a.com",
        "receiver": ["reciver@b.com"],
        "content": "邮件测试",
        "subject": "测试邮件"
    }

    t_mail = Email(send_info["mail_host"], send_info["mail_port"], send_info["mail_user"], send_info["mail_pass"],send_info["receiver"])
    t_mail.set_header(send_info["subject"])

    t_mail.attach("f01.html", "f01.html")
    t_mail.attach("f02.txt", "f02.txt")
    t_mail.attache_img("img1.jpg")
    t_mail.attache_img("img2.jpg")

    # 将附件添加好后，才可以设置邮件内容，图片必须在set_content之前
    t_mail.set_content('<h1>这是一个邮件测试</h1>', mail_type="html")
    t_mail.send()


























