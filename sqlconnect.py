import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="Your_password")
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
    """Insert a row into `tablename` using parameterized query.

    `values` may be a comma-separated string (from the Streamlit input)
    or a list/tuple of values. Strings will be passed as-is to the
    parameterized query so quoting is handled by the connector.
    """
    if isinstance(values, str):
        vals = [v.strip() for v in values.split(',')]
    elif isinstance(values, (list, tuple)):
        vals = list(values)
    else:
        raise TypeError("values must be a string, list, or tuple")

    placeholders = ','.join(['%s'] * len(vals))
    sql = f"INSERT INTO {tablename} VALUES ({placeholders})"
    mycursor.execute(sql, tuple(vals))
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
    # If it's a SELECT, return results; otherwise commit and return None
    if query.strip().upper().startswith('SELECT'):
        return mycursor.fetchall()
    else:
        mydb.commit()
        return None
