import os
import pyodbc 
from dotenv import load_dotenv
import datetime
load_dotenv()  # take environment variables from .env.



BackupInst = input('Enter Instance: ')
BackupDb = input('Enter Database: ')
BackupFol = input('Enter Folder Destination: ')

SRV = os.environ.get(BackupInst)
UID = os.environ.get('DBUID')

if SRV == os.environ.get('SQLINS01'):
  PWD = os.environ.get('DBPWD01') 
elif SRV == os.environ.get('SQLINS02'):
  PWD = os.environ.get('DBPWD02') 
elif SRV == os.environ.get('SQLINS03'):
  PWD = os.environ.get('DBPWD03') 
else:
  print ("No Password stored for that instance")
  PWD = input('Enter Password: ')

DBConn = None

try:
  print(f'Connecting to database...{BackupDb}')
  DBConn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{SRV};DATABASE={BackupDb};UID={UID};PWD={PWD}')

  if DBConn is not None:
      print(f'Connection to database...{BackupDb} was successful, attempting to backup')
      Date = datetime.datetime.today().strftime ('%m%d%y')
      Disk = (f'{BackupFol}\{BackupDb.replace(" ", "_")}{Date}.bak')
      cursor = DBConn.cursor()
      DBConn.autocommit = True
      cursor.execute(f"BACKUP DATABASE [{BackupDb}] TO DISK = N'{Disk}' with compression").fetchall
      while cursor.nextset():
        pass
      DBConn.autocommit = False
      DBConn.close()
      
except (Exception, pyodbc.Error) as error:
  print(f'Connection to database {BackupDb} failed')
  print(str(error))
