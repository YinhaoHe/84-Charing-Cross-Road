# decoding=utf-8
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys
import smtplib
import psycopg2


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


username = "charing84@hotmail.com"
password = "sayhello88907420"

imap = imaplib.IMAP4_SSL("imap-mail.outlook.com", 993)
imap.login(username, password)
imap.select("INBOX")
type, data = imap.search(None, '(UNSEEN UNDELETED)')# ALL

msgList = data[0].split()

print msgList

if len(msgList) == 0:
    sys.exit()

for current in msgList:
    type, data=imap.fetch(current, '(RFC822)')
    mail = email.message_from_string(data[0][1])
    subject = (email.Header.decode_header(mail['subject'])[0][0])
    # print subject
    # print (email.Header.decode_header(mail['From'])[0][0])# 不好用，带乱码
    print "from:" + (email.utils.parseaddr(mail.get("from"))[1])  # 好用
    # print (email.Header.decode_header(mail['To'])[0][0])# 不好用，带乱码
    # show_message(mail)

    mime = MIMEMultipart()
    sender = "charing84@hotmail.com"

    # 将邮件存入db（没做）
    # 去db里面找到from所对应的pair，如果找不到，无视这封邮件

    try:
        conn = psycopg2.connect(database="charing", user="postgres", password="postgres", host="127.0.0.1",
                                port="5432")
        cur = conn.cursor()
        cur.execute("SELECT pair_email FROM users where email=%s", (email.utils.parseaddr(mail.get("from"))[1],))
        rows = cur.fetchall()  # all rows in table
        if len(rows) != 1:
            continue  # 无视这封邮件

        pair_email = rows[0][0]

    except Exception, e:
        print Exception, ":", e
        continue
    finally:
        cur.close()
        conn.close()

    print ("ready to send to:" + pair_email)
    receivers = pair_email

    mime['From'] = sender
    mime['To'] = receivers
    mime['Subject'] = subject

    payload = mail.get_payload()

    if not isinstance(payload, str):
        for part in payload:
            # print part.is_multipart()
            mime.attach(part)
        # print mail.is_multipart()
        # print mail.as_string()
    else:
        mime.attach(MIMEText(payload, 'html', 'utf-8'))

    # print mime.as_string()

    send_mail_return = send_mail(receivers, mime.as_string())
    print ("send to %s success" % receivers)

    # if send_mail_return:
    #     imap.store(current, '+FLAGS', '\\seen')
