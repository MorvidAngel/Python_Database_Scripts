## How To Clone

To clone and run this application, you'll need [Git](https://git-scm.com) and [python](https://www.python.org/downloads/) installed on your computer. 

From your command line:

```bash
$ git clone https://github.com/DevThompson/Python_Database_Scripts
```

## How To Use

There are only two scripts that can be called directly database_backup.py and test_connection.py

`database_backup.py` takes in a server name or a short hand name of one if it's been predefined. If the server hasn't been predefined then a password must be entered as well. It then takes in input for a database name and folder path(Must be relative to the server). It will then attempt to connect to the database provided and create a backup of that database to the folder path.

`test_connection.py` runs three instances of a function stored in `database_connection.py` called `test_db_connection()`. It passes a servername, a username, and password into this function. It currently pulls the servers, passwords and username from the config file. All servers are stored in the config file in a list, which stores their names and passwords in a dictionary for each server The function then does a check against the server passed and runs a query stored in `check_avail_group.py` which returns list of databases in any of the existing availability groups on that server. It then takes that list and attempts to connect to each database to ensure they're online. If it fails to connect to a database it marks it adds it to the log marked as failed and sends an email with the error. If the connection succeeds it adds it to the log marked as succeeded. Once each instance of `test_db_connection()` is finished running `test_connection.py` will then send an email with the log.

## Current Config.py template
```
sql_ins_01= server1
sql_ins_02= server2
sql_ins_03= server3
db_uid= database user id
db_pwd_01= password for server1
db_pwd_02= password for server2
db_pwd_03= password for server3
smtp_server= smtp server
smtp_host= smtp host
smtp_port= smtp port
pyalert_email= email that will be sending the logs
recipient= email to receive status logs
recipient1= email to receive error logs

server_list = [
  {
      "server": sql_ins_01,
      "password": db_pwd_01
  },
  {
      "server": sql_ins_02,
      "password": db_pwd_02
  },
  {
      "server": sql_ins_03,
      "password": db_pwd_03
  }
]
```