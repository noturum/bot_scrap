# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 14:18:35 2021

@author: Admin
"""

import sqlite3
from sqlite3 import Error
from  sqlite3 import OperationalError
def connDB():
    try:
        conn = sqlite3.connect('db_call.db', isolation_level=None)
        cursor = conn.cursor()

        return conn, cursor
    except Error as e:
        print('Error db')
def selectFromDb(db):
    conn, cursor=connDB()
    rows=[]
    sql="SELECT * From {0}".format(db)
    cursor.execute(sql)
    
    for row in cursor:
        rows.append(row)
    conn.close()
    return dict(items=rows)
def addUser(UID,FirstName,LastName,Type):
    conn,cursor=connDB()
    sql="insert into User(UID,FirstName,LastName,Type) values ({0},{1},{2},{3})".format(UID,FirstName,LastName,Type)
    cursor.execute(sql)
    conn.commit()
def deleteUser(UID):
    conn,cursor=connDB()
    sql="delete from User where UID={0}".format(UID)
    cursor.execute(sql)
    conn.commit()
def changeTypeUser(UID,Type):
    conn,cursor=connDB()
    sql="update User set Type={0} where UID={1}".format(Type,UID)
    cursor.execute(sql)
    conn.commit()
def addSearch(UID,Url,FirstName,LastName,Type):
    conn,cursor=connDB()
    sql="insert into User(UID,FirstName,LastName,Type) values ({0},{1},{2},{3})".format(UID,FirstName,LastName,Type)
    cursor.execute(sql)
    conn.commit()
def deleteUser(UID):
    conn,cursor=connDB()
    sql="delete from User where UID={0}".format(UID)
    cursor.execute(sql)
    conn.commit()
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
        print(s)
#executeSql('insert into users(firstName,lastName,type) values ("{}","{}","{}")'.format('Niko','Lie','sysadm'),True)
