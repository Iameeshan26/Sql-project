from sqlconnect import *
print("----**Menu**----")
while True:
    print("\n1. Create Database \n2. Use Database \n3. Show Databases \n4. Create Table \n5. Insert Data \n6. Show Table Data \n7. Drop Table \n8. Delete Data \n9. Update Data \n10. Join Tables \n11. Custom Query \n12. Drop Database \n13. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        dbname = input("Enter the database name: ")
        createdatabase(dbname)
    elif choice == 2:
        dbname = input("Enter the database name: ")
        usedatabase(dbname)
    elif choice == 3:
        databases = showdatabases()
        for db in databases:
            print(db)
    elif choice == 4:
        table = input("Enter the table name: ")
        columns = input("Enter the columns (name datatype, ...): ")
        createtable(table, columns)
    elif choice == 5:
        table = input("Enter the table name: ")
        values = input("Enter the values (value1, value2, ...): ")
        insertdata(table, values)
    elif choice == 6:
        table = input("Enter the table name: ")
        data = showtable(table)
        for row in data:
            print(row)
    elif choice == 7:
        table = input("Enter the table name to drop: ")
        droptable(table)
    elif choice == 8:
        table = input("Enter the table name: ")
        condition = input("Enter the condition (e.g., id=1): ")
        deletedata(table, condition)
    elif choice == 9:
        table = input("Enter the table name: ")
        updates = input("Enter the updates (e.g., name='newname'): ")
        condition = input("Enter the condition (e.g., id=1): ")
        updatedata(table, updates, condition)
    elif choice == 10:
        table1 = input("Enter the first table name: ")
        table2 = input("Enter the second table name: ")
        joincondition = input("Enter the join condition (e.g., table1.id=table2.id): ")
        joined_data = jointables(table1, table2, joincondition)
        for row in joined_data:
            print(row)
    elif choice == 11:
        query = input("Enter your custom SQL query: ")
        print(customquery(query))
    elif choice == 12:
        database = input("Enter the database name to drop: ")
        dropdatabase(database)
    elif choice == 13:
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")