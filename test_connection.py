import smtplib

from database_connection import test_AG_connection, test_offline_connection, test_online_connection, ag_logs, online_logs, offline_logs
from email.mime.text import MIMEText
from config import *


##Running TestDBConnection for each microsoft sql server instance

for x in server_list:
  test_online_connection(x["server"], db_uid, x["password"])
  test_offline_connection(x["server"], db_uid, x["password"])
  
  if x["aglistener"] is not None:
    test_AG_connection(x["aglistener"], db_uid, x["password"])
  

##Once all TestDBConnect has been run for all instances send an email with the log results

agl_email_log = ""
onl_email_log = ""
ofl_email_log = ""

#Store logs from test_AG_Connection
for agl in ag_logs:
    agl_email_log = agl_email_log + agl

#Store logs from test_online_connection
for onl in online_logs:
    onl_email_log = onl_email_log + onl

#Store logs from test_offline_connection
for ofl in offline_logs:
    ofl_email_log = ofl_email_log + ofl

sender = pyalert_email
receivers = recipient1

msg = MIMEText(agl_email_log, "html")
msg2 = MIMEText(onl_email_log, "html")
msg3 = MIMEText(ofl_email_log, "html")

msg['Subject'] = 'Availability Group Connection Test'
msg['From'] = pyalert_email
msg['To'] = recipient1

msg2['Subject'] = 'Online Database Report'
msg2['From'] = pyalert_email
msg2['To'] = recipient1

msg3['Subject'] = 'Offline Database Report'
msg3['From'] = pyalert_email
msg3['To'] = recipient1

server = smtplib.SMTP(smtp_server, smtp_port, smtp_host)

server.sendmail(sender, receivers, msg.as_string())
server.sendmail(sender, receivers, msg2.as_string())
server.sendmail(sender, receivers, msg3.as_string())

print("Successfully sent email")

server.quit()
