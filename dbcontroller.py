import requests


import psycopg2
from psycopg2 import Error, OperationalError
def connDB():
    r = requests.post("https://bot-lhix.onrender.com/pass", data={'app': 'caller'})
    pwd = dict(r.json())['PWD']
    try:
        conn = psycopg2.connect(dbname='database', user='db_user',
                                password='mypassword', host='localhost')
        cursor = conn.cursor()

        return conn, cursor
    except Error as e:
        print('Error db')
def executeSql(sql,commit:bool=False):
    try:
        conn, cursor = connDB()
        cursor.execute(sql)
        if commit == True:
            conn.commit()
        # conn.close()

        return cursor.fetchall()
    except OperationalError as s:
        print('operation error')
        return 'error'