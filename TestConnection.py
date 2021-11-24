from DatabaseConnection import *
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from email.mime.text import MIMEText
import smtplib



username=os.environ.get('DBUID')

##Testing Instance 01
TestDBConnect(os.environ.get('INSQL01'), username, os.environ.get('DBPWD01'))
##Testing Instance 02
TestDBConnect(os.environ.get('INSQL02'), username, os.environ.get('DBPWD02'))
##Testing Instance 03
TestDBConnect(os.environ.get('INSQL03'), username, os.environ.get('DBPWD03'))

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
