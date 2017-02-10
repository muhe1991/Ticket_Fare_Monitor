import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'from@runoob.com'
receivers = ['holmes.hemu@gmail.com']

message = MIMEText('Python Test...', 'plain', 'utf-8')
message['From'] = Header("Tutorial", 'utf-8')
message['To'] = Header("test", 'utf-8')

subject = 'Python SMTP email test'
message['Subject'] = Header(subject, 'utf-8')


try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print "email success"
except smtplib.SMTPException:
    print "Error: cannot send"
