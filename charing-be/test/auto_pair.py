# decoding=utf-8
import psycopg2
import sys

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

    # for i in rows:
    #     print(i)
except Exception, e:
    print Exception, ":", e
finally:
    cur.close()
    conn.close()
