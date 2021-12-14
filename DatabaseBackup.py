import os
import pyodbc 
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.



BackupInst = input('Enter Instance: ')
BackupDb = input('Enter Database: ')
BackupFol = input('Enter Folder Destination')

SRV = os.environ.get(BackupInst)
UID = os.environ.get('DBUID')

if SRV == os.environ.get('SQLINS01'):
  PWD = os.environ.get('DBPWD01') 
elif SRV == os.environ.get('SQLINS02'):
  PWD = os.environ.get('DBPWD01') 
elif SRV == os.environ.get('SQLINS03'):
  PWD = os.environ.get('DBPWD01') 
else:
  print ("No Password stored for that instance")
  PWD = input('Enter Password: ')

DBConn = None

try:
  print(f'Connecting to database...{BackupDb}')
  DBConn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{SRV};DATABASE={BackupDb};UID={UID};PWD={PWD}')

  if DBConn is not None:
      print(f'Connection to database...{BackupDb} was successful, attempting to backup')

      Disk = (f'{BackupFol}\{BackupDb.replace(" ", "")}.bak')
      cursor = DBConn.cursor()
      DBConn.autocommit = True
      cursor.execute(f"BACKUP DATABASE [{BackupDb}] TO DISK = N'{Disk}' with compression").fetchall
      while cursor.nextset():
        pass
      DBConn.autocommit = False
      DBConn.close()
      
except (Exception, pyodbc.Error) as error:
  print(str(error))
