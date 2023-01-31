import pyodbc 
import smtplib

from email.mime.text import MIMEText
from queries.check_avail_group import check_avail_group
from queries.check_online_db import check_online_db
from queries.check_offline_db import check_offline_db
from queries.get_server_name import get_server_name
from config import pyalert_email, recipient, smtp_host, smtp_port, smtp_server

ag_logs= ['Availability Group Databases:']
online_logs=['Online Databases:']
offline_logs=['Offline Databases:']

def test_AG_connection (srv, uid, pwd):
    #Connecting to master database
    connstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{srv};DATABASE=master;UID={uid};PWD={pwd}'

    try:
        connection = pyodbc.connect(connstr)

        if connection is not None:
            cursor = connection.cursor()

            #Query to return a list of databases that belong to any of the existing availability groups depending on the instance passed
            cursor.execute(check_avail_group)

            result = cursor.fetchall()

            cursor.execute(get_server_name)

            servername = cursor.fetchone()
    except (Exception, pyodbc.Error) as error:

            ag_logs.append(f'<p>{srv}:<span style="color: red">  Connection Failed</span></p>')

            sender = pyalert_email
            receivers = recipient

            msg = MIMEText(str(error))
            
            msg['Subject'] = f'ERROR CONNECTION TO {srv} FAILED'
            msg['From'] = pyalert_email
            msg['To'] = recipient

            server = smtplib.SMTP(smtp_server, smtp_port, smtp_host)

            server.connect()
            
            server.sendmail(sender, receivers, msg.as_string())

            server.quit()

            return


    #Loops through each database returned by the query
    for DB in result:
        #Attempting to connect to database
        conndbstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{srv};DATABASE={DB[0]};UID={uid};PWD={pwd}'
        try:
            conn = pyodbc.connect(conndbstr)

            if conn is not None:
                ag_logs.append(f'<p>{servername[0]} - {DB[0]}:<span style="color: green">  Connection Successful</span></p>')
                conn.close()
        ##Send email with error and which database the error occurred with should connection fail to establish
        except (Exception, pyodbc.Error) as error:
            ag_logs.append(f'<p>{servername[0]} - {DB[0]}:<span style="color: red">  Connection Failed</span></p>')

            sender = pyalert_email
            receivers = recipient

            msg = MIMEText(str(error))
            
            msg['Subject'] = f'ERROR CONNECTION TO {DB[0]} ON {srv} FAILED'
            msg['From'] = pyalert_email
            msg['To'] = recipient

            server = smtplib.SMTP(smtp_server, smtp_port, smtp_host)

            server.connect()
            
            server.sendmail(sender, receivers, msg.as_string())

            server.quit()

def test_online_connection (srv, uid, pwd):
    #Connecting to master database
    connstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{srv};DATABASE=master;UID={uid};PWD={pwd}'
    try:
        connection = pyodbc.connect(connstr)

        if connection is not None:
            cursor = connection.cursor()

            #Query to return a list of databases that are listed as online
            cursor.execute(check_online_db)

            result = cursor.fetchall()

            cursor.execute(get_server_name)

            servername = cursor.fetchone()
    except (Exception, pyodbc.Error) as error:
            ag_logs.append(f'<p>{srv}:<span style="color: red">  Connection Failed</span></p>')

            sender = pyalert_email
            receivers = recipient

            msg = MIMEText(str(error))
            
            msg['Subject'] = f'ERROR CONNECTION TO {srv} FAILED'
            msg['From'] = pyalert_email
            msg['To'] = recipient

            server = smtplib.SMTP(smtp_server, smtp_port, smtp_host)

            server.connect()
            
            server.sendmail(sender, receivers, msg.as_string())

            server.quit()

            return
    #Loops through each database returned by the query
    for DB in result:
        #Attempting to connect to database 
        conndbstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{srv};DATABASE={DB[0]};UID={uid};PWD={pwd}'
        try:
            conn = pyodbc.connect(conndbstr)

            if conn is not None:
                online_logs.append(f'<p>{servername[0]} - {DB[0]}:<span style="color: green">  Connection Successful</span></p>')
                conn.close()
        ##Send email with error and which database the error occurred with should connection fail to establish
        except (Exception, pyodbc.Error) as error:
            online_logs.append(f'<p>{servername[0]} - {DB[0]}:<span style="color: red">  Connection Failed</span></p>')

            sender = pyalert_email
            receivers = recipient

            msg = MIMEText(str(error))
            
            msg['Subject'] = f'ERROR CONNECTION TO {DB[0]} ON {srv} FAILED'
            msg['From'] = pyalert_email
            msg['To'] = recipient

            server = smtplib.SMTP(smtp_server, smtp_port, smtp_host)

            server.connect()
            
            server.sendmail(sender, receivers, msg.as_string())

            server.quit()

def test_offline_connection (srv, uid, pwd):
    #Connecting to master database
    connstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{srv};DATABASE=master;UID={uid};PWD={pwd}'
    connection = pyodbc.connect(connstr)
    cursor = connection.cursor()

    #Query to return a list of databases that are listed as offline
    cursor.execute(check_offline_db)

    result = cursor.fetchall()

    cursor.execute(get_server_name)

    servername = cursor.fetchone()

    #Loops through each database returned by the query
    for DB in result:
        ##Adds log for each offline database
            offline_logs.append(f'<p>{servername[0]} - {DB[0]}:<span style="color: red">  OFFLINE</span></p>')
            
