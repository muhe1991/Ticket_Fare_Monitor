#! /usr/bin/python
# encoding=utf-8

import fare_query
import utilities


# depart_date_list = ["2017-09-14", "2017-09-15", "2017-09-16"]
# return_date_list = ["2017-10-02", "2017-10-03", "2017-10-04"]
# from_city_list = ["MUC"]
# to_city_list = ["PEK", "PVG"]

depart_date_list = ["2017-09-15"]
return_date_list = ["2017-10-03"]
from_city_list = ["MUC"]
to_city_list = ["PEK", "PVG"]


def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"


def run_monitor():

    [username, password] = utilities.fetch_email_credentials('credentials')

    email_str = "q_time\t\t\t\tfrom\t\tto\t\td_time\t\t\td_code\t\t\tr_time\t\tr_code\t\tfare\n"
    for depart_date in depart_date_list:
        for return_date in return_date_list:
            for from_city in from_city_list:
                for to_city in to_city_list:
                    [t, d, r, f, is_lowest] = fare_query.perform_a_query(from_city=from_city,
                                                                         to_city=to_city,
                                                                         date_depart=depart_date,
                                                                         date_return=return_date,
                                                                         solutions=5)
                    if is_lowest:
                        email_str += "%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s (Lowest)\n" \
                                     % (t, from_city, to_city, depart_date, d, return_date, r, f)
                    else:
                        email_str += "%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\n" \
                                     % (t, from_city, to_city, depart_date, d, return_date, r, f)

    send_email(user=username, pwd=password, recipient='mu.he@tum.de',
               subject='Ticket Fare Notice', body=email_str)


run_monitor()