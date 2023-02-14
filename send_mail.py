import smtplib
from email.mime.text import MIMEText
from config import *


##Script created to minimize the duplication of code needed to send mail

def send_smt_email (sender, receivers, msg):
  server = smtplib.SMTP(smtp_server, smtp_port, smtp_host)

  server.sendmail(sender, receivers, msg.as_string())

  print("Successfully sent email")

  server.quit()
