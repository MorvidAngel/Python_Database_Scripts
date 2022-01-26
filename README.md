## How To Clone

To clone and run this application, you'll need [Git](https://git-scm.com) and [python](https://www.python.org/downloads/) installed on your computer. 

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/DevThompson/Python_Database_Scripts
```

## How To Use

There are only two scripts that can be called directly database_backup.py and test_connection.py

`database_backup.py` takes in a server name or a short hand name of one if it's been predefined. If the server hasn't been predefined then a password must be entered as well. It then takes in input for a database name and folder path(Must be relative to the server). It will then attempt to connect to the database provided and create a backup of that database to the folder path.

`test_connection.py` runs three instances of a function stored in `database_connection.py` called `test_db_connection()`. It passes a servername, a username, and password into this function. The function then does a check against the server passed and runs a query stored in `check_avail_group.py` which returns list of databases in any of the existing availability groups on that server. It then takes that list and attempts to connect to each database to ensure they're online. If it fails to connect to a database it marks it adds it to the log marked as failed and sends an email with the error. If the connection succeeds it adds it to the log marked as succeeded. Once each instance of `test_db_connection()` is finished running `test_connection.py` will then send an email with the log.