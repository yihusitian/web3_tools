import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import CONFIG_OBJ


EMAIL_CONFIG = CONFIG_OBJ['emailConfig']
# 发件人邮箱和密码
sender_email = EMAIL_CONFIG['sender']
sender_password = EMAIL_CONFIG['authorizationCode']
# 收件人邮箱
receiver_email = EMAIL_CONFIG['receiver']

def sendEmailMessage(subject, body):
    # 创建 MIMEText 对象，用于邮件正文
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # 将正文添加到邮件中
    message.attach(MIMEText(body, "plain"))
    # 使用 163 邮箱的 SMTP 服务器连接
    try:
        smtp_server = smtplib.SMTP("smtp.163.com", 25)
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, receiver_email, message.as_string())
        smtp_server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败:", str(e))




