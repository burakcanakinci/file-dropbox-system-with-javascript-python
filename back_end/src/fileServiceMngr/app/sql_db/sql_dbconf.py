import mysql.connector

def dbCon():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'sqldb',
        'port': '3306',
        'database': 'fileServiceMgr'
    }
    connection = mysql.connector.connect(**config)

    return connection