# decoding=utf-8
from celery_send_mail import send_mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = "charing84@hotmail.com" #发件人的邮箱
msg = MIMEText('hello, celery')
msg['From'] = sender
msg['To'] = '236294386@qq.com'
msg['Subject'] = 'mail_test'

send_mail.delay('236294386@qq.com', msg.as_string())
