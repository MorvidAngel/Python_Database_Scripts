import smtplib

from database_connection import test_db_connection, logs
from email.mime.text import MIMEText
from config import *


##Running TestDBConnection for each microsoft sql server instance

for x in server_list:
  test_db_connection(x["server"], db_uid, x["password"])
  

##Once all TestDBConnect has been run for all instances send an email with the log results

conn_log = ""
for l in logs:
    conn_log = conn_log + l

sender = pyalert_email
receivers = recipient

msg = MIMEText(conn_log, "html")

msg['Subject'] = 'Availability Group Connection Test'
msg['From'] = pyalert_email
msg['To'] = recipient

server = smtplib.SMTP(smtp_server, smtp_port, smtp_host)

server.sendmail(sender, receivers, msg.as_string())

print("Successfully sent email")

server.quit()
