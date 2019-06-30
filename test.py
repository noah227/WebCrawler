# __Author__: NOAH227
# __Date__: 2019/6/27

import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.qq.com"   # e.g.
user_name = "xxx@xx.com"
password = "****"   # authorized pass code 

sender = "xxx@xx.com"  # for a better code check
receiver = ["noah227@foxmail.com", ]


def send_email(title, link):
    html_part = """
    <h3>Newly Found!</h3>
    <p><a href='%s'>%s</a></p>
    """ % (link, title)
    message = MIMEText(html_part, "html", "utf-8")

    message["From"] = Header("Valid user", "utf-8")
    message["To"] = Header("Dear Unknown", "utf-8")
    message["Subject"] = Header("又有新发现", "utf-8")   # 腾讯的反垃圾估计是识别主题的

    # noinspection PyBroadException
    try:
        smtpBoot = smtplib.SMTP()
        smtpBoot.connect(mail_host, 25)
        smtpBoot.login(user_name, password)
        smtpBoot.sendmail(sender, receiver, message.as_string())
        print("success!")  # log

    except Exception as e:
        print("failed!", e)
        pass


