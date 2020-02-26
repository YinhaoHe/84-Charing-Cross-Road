#-*- encoding: gb2312 -*-
import os, sys, string
import poplib

# pop3服务器地址
host = "pop-mail.outlook.com"
# 用名
username = "charing84@hotmail.com"
# 密码
password = "sayhello88907420"
# 创建一个pop3对象，这个时候实际上已经连接上服务器了#hotmail使用SSL加密,端口995

pp = poplib.POP3_SSL(host)
# 设置调试模式，可以看到与服务器的交互信息
# pp.set_debuglevel(1)

# 向服务器发送用户名
pp.user(username)
# 向服务器发送密码
pp.pass_(password)
# 获取服务器上信件信息，返回是一个列表，第一项是一共有多上封邮件，第二项是共有多少字节

ret = pp.stat()
print('Messages: %s. Size: %s' % ret)

# 需要取出所有信件的头部，信件id是从1开始的。
for i in range(1, ret[0]+1):
    # 取出信件头部。注意：top指定的行数是以信件头为基数的，也就是说当取0行，
    # 其实是返回头部信息，取1行其实是返回头部信息之外再多1行。
    mlist = pp.top(i, 0)
    print mlist[1]

# 列出服务器上邮件信息，这个会对每一封邮件都输出id和大小。不象stat输出的是总的统计信息
resp, mails, octets = pp.list()
print mails

# pp.retr(1)代表取第一封邮件完整信息，在返回值里，是按行存储在lines的列表里的。resp是返回的状态信息
resp, lines, octets = pp.retr(1)
print 'lines:', len(lines)
print '\n\n'
# 输出邮件
msg_content = '\r\n'.join(lines)
print msg_content

# 退出
pp.quit()