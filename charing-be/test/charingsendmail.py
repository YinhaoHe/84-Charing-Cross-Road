# decoding=utf-8
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print 'Content-Type: text/html;charset=utf-8\r\n'


    smtp = smtplib.SMTP()
    smtp.connect("smtp-mail.outlook.com", 587)

    sender = "charing84@hotmail.com" #发件人的邮箱
    password = "sayhello88907420"
    receivers = "236294386@qq.com" #收件人的邮箱

    smtp.starttls()
    smtp.login(sender, password)

    msg = MIMEText('mail_content')
    msg['From'] = sender
    msg['To'] = receivers
    msg['Subject'] = 'mail_test'
    smtp.sendmail(sender, receivers, msg.as_string())
    smtp.quit()

send_mail()
