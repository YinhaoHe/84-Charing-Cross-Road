# decoding=utf-8 
from flask import Flask 
from flask import request
import re
import psycopg2
import sys
app = Flask(__name__)

reload(sys)
sys.setdefaultencoding("utf-8")

@app.route('/post', methods=['POST'])
def post():
    first_mail_content = request.form['first_mail_content'].encode(encoding='utf-8')
    email = request.form['email'].encode(encoding='utf-8')

    if not re.compile(r"""^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+""").match(email):
        return """["false","email_error"]"""

    sex = request.form['sex']
    # return 'first_mail_content:%s\r\nemail:%s\r\nsex:%s' % (first_mail_content, email, sex)
    if sex == u"男":
        sex_bool = True
    elif sex == u"女":
        sex_bool = False
    else:
        return """["false","sex_error"]"""

    try:
        conn = psycopg2.connect(database="charing", user="postgres", password="postgres", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        cur.execute(u"insert into users(email,first_mail_content,sex) values (%s,%s,%s)",
                    (email, first_mail_content, sex_bool))
        conn.commit()
        return """["true"]"""
    except Exception, e:
        print Exception
        print e
        if "duplicate key value" in str(e) and "pk_email" in str(e):
            return ("""["false","duplicate_email"]""")
        else:
            return ("""["false","db_error"]""")
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
