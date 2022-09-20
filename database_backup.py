import pyodbc 
import datetime

from config import *



#Takes environment name variable not actual instance name
backupinst = input('Enter Instance: ')
#Checks to see if a password is stored for that instance, if not one must be entered
if backupinst == 'SQLINS01':
  srv = sql_ins_01
  pwd = db_pwd_01
elif backupinst == 'SQLINS02':
  srv = sql_ins_02
  pwd = db_pwd_01
elif backupinst == 'SQLINS03':
  srv = sql_ins_03
  pwd = db_pwd_01
else:
  print ("No password stored for that server")
  srv = backupinst
  pwd = input('Enter Password: ')

#Takes database name
backupdb = input('Enter Database: ')
#Takes a folder path, relative to the machine the instance is on
backupfol = input('Enter Folder Destination: ') 

dbconn = None

#Attempts to connect to the database
try:
  print(f'Connecting to database...{backupdb}')

  dbconn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+f'{srv};DATABASE={backupdb};UID={db_uid};pwd={pwd}')

  #If connection successfull attempts to create a backup based on parameters previously entered
  if dbconn is not None:
    try:
      print(f'Connection to database...{backupdb} was successful, attempting to backup')

      date = datetime.datetime.today().strftime ('%m%d%y')

      disk = (f'{backupfol}\{backupdb.replace(" ", "_")}{date}.bak')

      cursor = dbconn.cursor()

      dbconn.autocommit = True

      cursor.execute(f"BACKUP DATABASE [{backupdb}] TO DISK = N'{disk}' with compression")
      
      while cursor.nextset():
        pass
      dbconn.autocommit = False
      dbconn.close()

    #Returns error if backup fails
    except (Exception, pyodbc.Error) as error:
      print(f'Failed to preform backup for {backupdb}')
      print(str(error))

#Returns error if connection fails      
except (Exception, pyodbc.Error) as error:
  print(f'Connection to database {backupdb} failed')
  print(str(error))
