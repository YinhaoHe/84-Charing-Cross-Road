#-*- encoding: gb2312 -*-
import os, sys, string
import poplib

# pop3��������ַ
host = "pop-mail.outlook.com"
# ����
username = "charing84@hotmail.com"
# ����
password = "sayhello88907420"
# ����һ��pop3�������ʱ��ʵ�����Ѿ������Ϸ�������#hotmailʹ��SSL����,�˿�995

pp = poplib.POP3_SSL(host)
# ���õ���ģʽ�����Կ�����������Ľ�����Ϣ
# pp.set_debuglevel(1)

# ������������û���
pp.user(username)
# ���������������
pp.pass_(password)
# ��ȡ���������ż���Ϣ��������һ���б���һ����һ���ж��Ϸ��ʼ����ڶ����ǹ��ж����ֽ�

ret = pp.stat()
print('Messages: %s. Size: %s' % ret)

# ��Ҫȡ�������ż���ͷ�����ż�id�Ǵ�1��ʼ�ġ�
for i in range(1, ret[0]+1):
    # ȡ���ż�ͷ����ע�⣺topָ�������������ż�ͷΪ�����ģ�Ҳ����˵��ȡ0�У�
    # ��ʵ�Ƿ���ͷ����Ϣ��ȡ1����ʵ�Ƿ���ͷ����Ϣ֮���ٶ�1�С�
    mlist = pp.top(i, 0)
    print mlist[1]

# �г����������ʼ���Ϣ��������ÿһ���ʼ������id�ʹ�С������stat��������ܵ�ͳ����Ϣ
resp, mails, octets = pp.list()
print mails

# pp.retr(1)����ȡ��һ���ʼ�������Ϣ���ڷ���ֵ��ǰ��д洢��lines���б���ġ�resp�Ƿ��ص�״̬��Ϣ
resp, lines, octets = pp.retr(1)
print 'lines:', len(lines)
print '\n\n'
# ����ʼ�
msg_content = '\r\n'.join(lines)
print msg_content

# �˳�
pp.quit()