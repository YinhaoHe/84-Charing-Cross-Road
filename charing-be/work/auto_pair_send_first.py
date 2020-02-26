# decoding=utf-8
import psycopg2
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys
import smtplib

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
        return True
    except Exception, e:
        return False


try:
    conn = psycopg2.connect(database="charing", user="postgres", password="postgres", host="127.0.0.1",
                            port="5432")
    cur = conn.cursor()
    cur.execute("SELECT email,first_mail_content,sex,pair_email FROM users where pair_email is NULL and sex = FALSE ORDER BY register_time ASC limit 1")
    rows = cur.fetchall()  # all rows in table

    if len(rows) != 1:
        sys.exit()

    first_email = rows[0][0]
    first_first_mail_content = rows[0][1]

    cur.execute("SELECT email,first_mail_content,sex,pair_email FROM users where pair_email is NULL and sex = True ORDER BY register_time ASC limit 1")
    rows = cur.fetchall()  # all rows in table

    if len(rows) != 1:
        sys.exit()

    second_email = rows[0][0]
    second_first_mail_content = rows[0][1]

    cur.execute("update users set pair_email = %s where email = %s", (second_email, first_email))
    cur.execute("update users set pair_email = %s where email = %s", (first_email, second_email))
    conn.commit()

    print ("auto pair success: %s %s" % (first_email, second_email))

    sender = "charing84@hotmail.com"  # 发件人的邮箱
    msg1 = MIMEText(first_first_mail_content)
    msg1['From'] = sender
    msg1['To'] = second_email
    msg1['Subject'] = u'一封来自查令路84号(charing84.net)的邮件'
    send_mail(second_email, msg1.as_string())
    print ("first_mail from %s to %s send success" % (first_email, second_email))

    msg2 = MIMEText(second_first_mail_content)
    msg2['From'] = sender
    msg2['To'] = first_email
    msg2['Subject'] = u'一封来自查令路84号(charing84.net)的邮件'
    send_mail(first_email, msg2.as_string())
    print ("first_mail from %s to %s send success" % (second_email, first_email))

    # for i in rows:
    #     print(i)
except Exception, e:
    print Exception, ":", e
finally:
    cur.close()
    conn.close()
