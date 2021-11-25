import pyodbc 
import os
import datetime
from email.mime.text import MIMEText
import smtplib


Logs = []


def TestDBConnect (SRV, UID, PWD):
    ##Setting databases to check based on server instance
    if SRV == os.environ.get('INSQL01'):
        databases = ['AfterMail_TEMP', 'ArchiveManager', 'Audit Store', 'Audit Store Old', 'ConfigDb', 'ConfigDB-Dev', 'ConfigMgmt', 'Content', 'Content Old', 'HEATDiscoveryConfig', 'HEATMetricsCache', 'HEATSM', 'HEATSM-UAT', 'sem5']
    if SRV == os.environ.get('INSQL02'):
        databases = ['IdentityDirector', 'IvantiEPM', 'IvntAuto', 'SEEMSDb2', 'solarwindsdba', 'ReportServer', 'SolarWindsOrionLog', 'SolarWindsNetFlowStorage']
    if SRV == os.environ.get('INSQL03'):
        databases = ['Audit Store', 'Cognos', 'DSM', 'DYNAMICS', 'FileBoundProd', 'NDP', 'NIB', 'ov_txtsrch', 'SpecsIDBadging', 'TMATE_DBPRD', 'Management Reporter']

    conn = None

    for DB in databases:
        ##Attempting to connect to database within a specific instance
        try:
            Logs.append(f'Connecting to database...{DB}')
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{SRV};DATABASE={DB};UID={UID};PWD={PWD}')

            if conn is not None:
                Logs.append(f'Connection to database...{DB} was successful, Closing Connection.')
                conn.close()
        ##Send email with error and which database the error occurred with should connection fail to establish
        except (Exception, pyodbc.Error) as error:
            Logs.append(str(error))

            sender = 'pyalert@nib-bahamas.com'
            receivers = ['dthompson@nib-bahamas.com']
            msg = MIMEText(str(error))

            msg['Subject'] = f'ERROR CONNECTION TO {DB} ON {SRV} FAILED'
            msg['From'] = 'pyalert@nib-bahamas.com'
            msg['To'] = 'dthompson@nib-bahamas.com'

            with smtplib.SMTP(os.environ.get('SMTPSERVER'), os.environ.get('SMTPPORT'), os.environ.get('SMTPHOSTNAME')) as server:

                server.sendmail(sender, receivers, msg.as_string())