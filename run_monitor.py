import fare_query
import fare_check
import smtplib
from email.mime.text import MIMEText
from email.header import Header


depart_date_list = ["2017-09-14", "2017-09-15", "2017-09-16"]
return_date_list = ["2017-10-02", "2017-10-03", "2017-10-04"]
from_city_list = ["MUC"]
to_city_list = ["PEK", "PVG"]


def send_fare_email(email_msg):
    sender = 'mu.he@tum.de'
    receiver = 'mu.he@tum.de'

    message = MIMEText(email_msg, 'plain', 'utf-8')
    message['From'] = Header("菜鸟教程", 'utf-8')
    message['To'] = Header("测试", 'utf-8')

    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"


def run_monitor():

    email_str = "q_time\t\tfrom\t\tto\t\td_time\t\td_codet\t\tr_time\t\tr_code\t\tfare\n"
    for depart_date in depart_date_list:
        for return_date in return_date_list:
            for from_city in from_city_list:
                for to_city in to_city_list:
                    [t, d, r, f] = fare_query.perform_a_query(from_city=from_city,
                                                              to_city=to_city,
                                                              date_depart=depart_date,
                                                              date_return=return_date,
                                                              solutions=5)
                    email_str += "%s\t\t%s\t\tto\t\td_time\t\td_codet\t\tr_time\t\tr_code\t\tfare\n" % (
                        t, from_city, to_city, depart_date, d, return_date, r, f
                    )

    send_fare_email(email_str)