# decoding=utf-8
import sys
import smtplib
from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('celery_send_mail', broker='pyamqp://myuser:mypassword@localhost:5672/myvhost')

logger = get_task_logger(__name__)
@app.task(ignore_result=True)
def send_mail(receivers, msg_str):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect("smtp-mail.outlook.com", 587)

        sender = "charing84@hotmail.com"  # 发件人的邮箱
        password = "sayhello88907420"
        # receivers = "236294386@qq.com"  # 收件人的邮箱

        smtp.starttls()
        smtp.login(sender, password)

        smtp.sendmail(sender, receivers, msg_str)
        smtp.quit()
        logger.info('receiver:%s,send success' % receivers)
        return True
    except Exception, e:
        logger.info('receiver:%s,send fail' % receivers)
        return False
