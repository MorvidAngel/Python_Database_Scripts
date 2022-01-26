import os
import pyodbc 
from dotenv import load_dotenv
import datetime
load_dotenv()  # take environment variables from .env.


#Takes environment name variable not actual instance name
BackupInst = input('Enter Instance: ')
#Takes database name
BackupDb = input('Enter Database: ')
#Takes a folder path, relative to the machine the instance is on
BackupFol = input('Enter Folder Destination: ') 

SRV = os.environ.get(BackupInst) #Checks to see if is a value set for the environment variable passed
UID = os.environ.get('DBUID') #Grabs the username stored in an environment variable

#Checks to see if a password is stored for that instance, if not one must be entered
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

#Attempts to connect to the database
try:
  print(f'Connecting to database...{BackupDb}')
  DBConn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{SRV};DATABASE={BackupDb};UID={UID};PWD={PWD}')

  #If connection successfull attempts to create a backup based on parameters previously entered
  if DBConn is not None:
    try:
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

    #Returns error if backup fails
    except (Exception, pyodbc.Error) as error:
      print(f'Failed to preform backup for {BackupDb}')
      print(str(error))

#Returns error if connection fails      
except (Exception, pyodbc.Error) as error:
  print(f'Connection to database {BackupDb} failed')
  print(str(error))
