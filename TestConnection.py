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

errLog = ""
for l in Logs:
    errLog = errLog + l + '\n'

sender = 'pyalert@nib-bahamas.com'
receivers = ['dthompson@nib-bahamas.com']

msg = MIMEText(errLog)

msg['Subject'] = 'Availibility Group Connection Test'
msg['From'] = 'pyalert@nib-bahamas.com'
msg['To'] = 'dthompson@nib-bahamas.com'

with smtplib.SMTP('mail.nib-bahamas.com') as server:

    server.sendmail(sender, receivers, msg.as_string())
    print("Successfully sent email")
