import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def show_message(mail):
    if mail.is_multipart():
        for part in mail.get_payload():
            show_message(part)
    else:
        type = mail.get_content_charset()
        if type == None:
            print mail.get_payload()
        else:
            try:
                print unicode(mail.get_payload(), type)
            except UnicodeDecodeError:
                print mail


username = "charing84@hotmail.com"
password = "sayhello88907420"

conn = imaplib.IMAP4_SSL("imap-mail.outlook.com", 993)
conn.login(username, password)
conn.select("INBOX")
type, data = conn.search(None, 'ALL')

msgList = data[0].split()
print msgList
last = msgList[len(msgList) - 1]

type, data=conn.fetch(4, '(RFC822)')
mail = email.message_from_string(data[0][1])
subject = (email.Header.decode_header(mail['subject'])[0][0])
print subject
print (email.Header.decode_header(mail['From'])[0][0])
print (email.Header.decode_header(mail['To'])[0][0])

# show_message(mail)
mime = MIMEMultipart()
sender = "charing84@hotmail.com"
receivers = "236294386@qq.com"
mime['From'] = sender
mime['To'] = receivers
mime['Subject'] = 'mail_test'

payload = mail.get_payload()


if not isinstance(payload, str):
    for part in payload:
        # print part.is_multipart()
        mime.attach(part)
    # print mail.is_multipart()
    # print mail.as_string()
else:
    mime.attach(MIMEText(payload, 'html', 'utf-8'))


print mime.as_string()