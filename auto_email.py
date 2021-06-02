import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg_from = '1792962757@qq.com'
msg_to = '1792962757@qq.com'
password = 'jiubvyxxybymejhg'


def auto_email(warnList):
    # 邮件内容为所有的预警基金名称
    # 报错也会发邮件通知
    if isinstance(warnList, str):
        content = '运行时出现错误，错误如下：' + warnList
        subject = '运行报错！！！'
    else:
        content = '\n'.join(warnList)
        subject = '基金预警！！！'

    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to

    try:
        client = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
        print('连接到邮件服务器成功！！！')

        client.login(msg_from, password)
        print('登录成功！！！')

        client.sendmail(msg_from, msg_to, msg.as_string())
        print('发送成功！！！')
    except smtplib.SMTPException as e:
        print(e)
        print('发送失败！！！')
    finally:
        client.quit()
