import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="eeshu2604")
mycursor = mydb.cursor()
def createdatabase(dbname):
    mycursor.execute(f"CREATE DATABASE {dbname}")
def usedatabase(dbname):
    mycursor.execute(f"USE {dbname}")
def showdatabases():
    mycursor.execute("SHOW DATABASES")
    result = mycursor.fetchall()
    return result
def showtable(tablename):
    mycursor.execute(f"SELECT * FROM {tablename}")
    result = mycursor.fetchall()
    return result
def createtable(tablename, columns):
    mycursor.execute(f"CREATE TABLE {tablename} ({columns})")
    mydb.commit()
def insertdata(tablename, values):
    mycursor.execute(f"INSERT INTO {tablename} VALUES ({values})")
    mydb.commit()
def droptable(tablename):
    mycursor.execute(f"DROP TABLE {tablename}")
    mydb.commit()
def dropdatabase(dbname):
    mycursor.execute(f"DROP DATABASE {dbname}")
    mydb.commit()
def deletedata(tablename, condition):
    mycursor.execute(f"DELETE FROM {tablename} WHERE {condition}")
    mydb.commit()
def updatedata(tablename, set_values, condition):
    mycursor.execute(f"UPDATE {tablename} SET {set_values} WHERE {condition}")
    mydb.commit()
def jointables(table1, table2, join_condition):
    mycursor.execute(f"SELECT * FROM {table1} JOIN {table2} ON {join_condition}")
    result = mycursor.fetchall()
    return result
def customquery(query):
    mycursor.execute(query)
    result = mycursor.fetchall()
    return result