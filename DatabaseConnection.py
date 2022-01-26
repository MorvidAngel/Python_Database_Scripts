import pyodbc 
import os
from email.mime.text import MIMEText
import smtplib


Logs = []


def TestDBConnect (SRV, UID, PWD):
    #Connecting to master database
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{SRV};DATABASE=master;UID={UID};PWD={PWD}')
    
    cursor = connection.cursor()

    #Query to return a list of databases that belong to any of the existing availability groups depending on the instance passed
    query = """
              SELECT
                    dbcs.database_name AS [DatabaseName]
              FROM 
                    master.sys.availability_groups AS AG
                      LEFT OUTER JOIN 
                        master.sys.dm_hadr_availability_group_states as agstates
                          ON AG.group_id = agstates.group_id
                      INNER JOIN 
                        master.sys.availability_replicas AS AR
                          ON AG.group_id = AR.group_id
                      INNER JOIN 
                        master.sys.dm_hadr_availability_replica_states AS arstates
                          ON AR.replica_id = arstates.replica_id AND arstates.is_local = 1
                      INNER JOIN 
                        master.sys.dm_hadr_database_replica_cluster_states AS dbcs
                          ON arstates.replica_id = dbcs.replica_id
                      LEFT OUTER JOIN 
                        master.sys.dm_hadr_database_replica_states AS dbrs
                          ON dbcs.replica_id = dbrs.replica_id AND dbcs.group_database_id = dbrs.group_database_id
              WHERE
                    AG.name in ('AVG_SQLN01', 'AVG_SQLN02', 'AVG_SQLN03')
              ORDER BY 
                    AG.name ASC
                  , dbcs.database_name
              """
    cursor.execute(query)
    result = cursor.fetchall()

    #Loops through each database returned by the query
    for DB in result:
        ##Attempting to connect to database 
        try:
            Logs.append(f'Connecting to database...{DB[0]}')
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{SRV};DATABASE={DB[0]};UID={UID};PWD={PWD}')

            if conn is not None:
                Logs.append(f'Connection to database...{DB[0]} was successful, Closing Connection.')
                conn.close()
        ##Send email with error and which database the error occurred with should connection fail to establish
        except (Exception, pyodbc.Error) as error:
            Logs.append(str(error))

            sender = 'pyalert@nib-bahamas.com'
            receivers = ['ITInfraOps@nib-bahamas.com', 'dthompson@nib-bahamas.com']
            msg = MIMEText(str(error))

            msg['Subject'] = f'ERROR CONNECTION TO {DB[0]} ON {SRV} FAILED'
            msg['From'] = 'pyalert@nib-bahamas.com'
            msg['To'] = 'ITInfraOps@nib-bahamas.com'

            with smtplib.SMTP(os.environ.get('SMTPSERVER'), os.environ.get('SMTPPORT'), os.environ.get('SMTPHOSTNAME')) as server:

                server.sendmail(sender, receivers, msg.as_string())
