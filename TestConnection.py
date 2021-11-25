from DatabaseConnection import *
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from email.mime.text import MIMEText
import smtplib



username=os.environ.get('DBUID')

##Running TestDBConnection for each microsoft sql server instance
TestDBConnect(os.environ.get('INSQL01'), username, os.environ.get('DBPWD01'))

TestDBConnect(os.environ.get('INSQL02'), username, os.environ.get('DBPWD02'))

TestDBConnect(os.environ.get('INSQL03'), username, os.environ.get('DBPWD03'))

##Once all TestDBConnect has been run for all instances send an email with the log results
connLog = ""
for l in Logs:
    connLog = connLog + l + '\n'

sender = 'pyalert@nib-bahamas.com'
receivers = ['dthompson@nib-bahamas.com']

msg = MIMEText(connLog)

msg['Subject'] = 'Availibility Group Connection Test'
msg['From'] = 'pyalert@nib-bahamas.com'
msg['To'] = 'dthompson@nib-bahamas.com'

with smtplib.SMTP(os.environ.get('SMTPSERVER'), os.environ.get('SMTPPORT'), os.environ.get('SMTPHOSTNAME')) as server:

    server.sendmail(sender, receivers, msg.as_string())
    print("Successfully sent email")
