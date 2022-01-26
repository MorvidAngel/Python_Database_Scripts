import pyodbc 
import smtplib

from email.mime.text import MIMEText
from queries.check_avail_group import check_avail_group
from config import pyalert_email, recipient1, smtp_host, smtp_port, smtp_server

logs= ['Connection Attempt:']

def test_db_connection (srv, uid, pwd):
    #Connecting to master database
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{srv};DATABASE=master;UID={uid};PWD={pwd}')
    cursor = connection.cursor()

    #Query to return a list of databases that belong to any of the existing availability groups depending on the instance passed
    cursor.execute(check_avail_group)

    result = cursor.fetchall()

    #Loops through each database returned by the query
    for DB in result:
        ##Attempting to connect to database 
        try:
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{srv};DATABASE={DB[0]};UID={uid};PWD={pwd}')

            if conn is not None:
                logs.append(f'<p>{DB[0]}:<span style="color: green">  Succeeded</span></p>')
                conn.close()
        ##Send email with error and which database the error occurred with should connection fail to establish
        except (Exception, pyodbc.Error) as error:
            logs.append(f'<p>{DB[0]}:<span style="color: red">  Failed</span></p>')

            sender = pyalert_email
            receivers = recipient1
            msg = MIMEText(str(error))
            msg['Subject'] = f'ERROR CONNECTION TO {DB[0]} ON {srv} FAILED'
            msg['From'] = pyalert_email
            msg['To'] = recipient1

            server = smtplib.SMTP(smtp_server, smtp_port, smtp_host)

            server.connect()
            
            server.sendmail(sender, receivers, msg.as_string())

            server.quit()
