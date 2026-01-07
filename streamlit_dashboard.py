import streamlit as st
import pandas as pd
from sqlconnect import (
    createdatabase, usedatabase, showdatabases, showtable, 
    createtable, insertdata, droptable, dropdatabase, 
    deletedata, updatedata, jointables, customquery, mycursor, mydb
)

st.set_page_config(page_title="SQL Database Manager", layout="wide")
st.title("🗄️ SQL Database Manager")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
operation = st.sidebar.radio(
    "Select Operation",
    [
        "📊 View Databases",
        "📈 View Tables",
        "➕ Create Database",
        "➕ Create Table",
        "📝 Insert Data",
        "🔍 Query Data",
        "✏️ Update Data",
        "🗑️ Delete Data",
        "🗑️ Drop Table",
        "🗑️ Drop Database",
        "🔗 Join Tables",
        "💬 Custom Query"
    ]
)

# ==================== VIEW DATABASES ====================
if operation == "📊 View Databases":
    st.header("View All Databases")
    try:
        databases = showdatabases()
        if databases:
            db_list = [db[0] for db in databases]
            df = pd.DataFrame(db_list, columns=["Database Name"])
            st.dataframe(df, use_container_width=True)
            st.success(f"Total Databases: {len(db_list)}")
        else:
            st.info("No databases found")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ==================== VIEW TABLES ====================
elif operation == "📈 View Tables":
    st.header("View Table Data")
    databases = [db[0] for db in showdatabases()]
    
    col1, col2 = st.columns(2)
    with col1:
        selected_db = st.selectbox("Select Database", databases)
    
    if selected_db:
        try:
            usedatabase(selected_db)
            mycursor.execute("SHOW TABLES")
            tables = [table[0] for table in mycursor.fetchall()]
            
            with col2:
                selected_table = st.selectbox("Select Table", tables)
            
            if selected_table:
                try:
                    rows = showtable(selected_table)
                    mycursor.execute(f"DESCRIBE {selected_table}")
                    columns = [col[0] for col in mycursor.fetchall()]
                    
                    if rows:
                        df = pd.DataFrame(rows, columns=columns)
                        st.subheader(f"Data from {selected_table}")
                        st.dataframe(df, use_container_width=True)
                        st.success(f"Total Records: {len(df)}")
                    else:
                        st.info("Table is empty")
                except Exception as e:
                    st.error(f"Error fetching table data: {str(e)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ==================== CREATE DATABASE ====================
elif operation == "➕ Create Database":
    st.header("Create New Database")
    
    db_name = st.text_input("Enter Database Name", placeholder="my_database")
    
    if st.button("Create Database", key="create_db"):
        if db_name.strip():
            try:
                createdatabase(db_name)
                mydb.commit()
                st.success(f"✅ Database '{db_name}' created successfully!")
            except Exception as e:
                st.error(f"Error creating database: {str(e)}")
        else:
            st.warning("Please enter a valid database name")

# ==================== CREATE TABLE ====================
elif operation == "➕ Create Table":
    st.header("Create New Table")
    
    databases = [db[0] for db in showdatabases()]
    selected_db = st.selectbox("Select Database", databases)
    
    if selected_db:
        usedatabase(selected_db)
        
        table_name = st.text_input("Table Name", placeholder="my_table")
        
        st.subheader("Define Columns")
        st.info("Example format: `id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100)`")
        
        columns_definition = st.text_area(
            "Columns Definition (comma-separated)",
            placeholder="id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), email VARCHAR(100)",
            height=150
        )
        
        if st.button("Create Table", key="create_table"):
            if table_name.strip() and columns_definition.strip():
                try:
                    createtable(table_name, columns_definition)
                    st.success(f"✅ Table '{table_name}' created successfully!")
                except Exception as e:
                    st.error(f"Error creating table: {str(e)}")
            else:
                st.warning("Please fill in all fields")

# ==================== INSERT DATA ====================
elif operation == "📝 Insert Data":
    st.header("Insert Data into Table")
    
    databases = [db[0] for db in showdatabases()]
    selected_db = st.selectbox("Select Database", databases)
    
    if selected_db:
        usedatabase(selected_db)
        mycursor.execute("SHOW TABLES")
        tables = [table[0] for table in mycursor.fetchall()]
        
        selected_table = st.selectbox("Select Table", tables)
        
        if selected_table:
            # Get column information
            mycursor.execute(f"DESCRIBE {selected_table}")
            columns_info = mycursor.fetchall()
            columns = [col[0] for col in columns_info]
            
            st.subheader(f"Insert Data into {selected_table}")
            st.write("**Columns:**", ", ".join(columns))
            
            values_input = st.text_input(
                "Enter Values (comma-separated, in order)",
                placeholder="1, John Doe, john@example.com"
            )
            
            if st.button("Insert Data", key="insert_data"):
                if values_input.strip():
                    try:
                        insertdata(selected_table, values_input)
                        st.success(f"✅ Data inserted successfully into {selected_table}!")
                    except Exception as e:
                        st.error(f"Error inserting data: {str(e)}")
                else:
                    st.warning("Please enter values")

# ==================== QUERY DATA ====================
elif operation == "🔍 Query Data":
    st.header("Query Table Data")
    
    databases = [db[0] for db in showdatabases()]
    selected_db = st.selectbox("Select Database", databases)
    
    if selected_db:
        usedatabase(selected_db)
        mycursor.execute("SHOW TABLES")
        tables = [table[0] for table in mycursor.fetchall()]
        
        selected_table = st.selectbox("Select Table", tables)
        
        if selected_table:
            mycursor.execute(f"DESCRIBE {selected_table}")
            columns_info = mycursor.fetchall()
            columns = [col[0] for col in columns_info]
            
            st.subheader(f"Query {selected_table}")
            
            # Simple filtering
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_column = st.selectbox("Filter by Column", ["-- No Filter --"] + columns)
            
            with col2:
                operator = st.selectbox("Operator", ["=", ">", "<", ">=", "<=", "LIKE"])
            
            with col3:
                filter_value = st.text_input("Filter Value")
            
            if st.button("Execute Query", key="query_data"):
                try:
                    if filter_column != "-- No Filter --" and filter_value.strip():
                        if operator == "LIKE":
                            condition = f"`{filter_column}` LIKE '%{filter_value}%'"
                        else:
                            condition = f"`{filter_column}` {operator} '{filter_value}'"
                        query = f"SELECT * FROM {selected_table} WHERE {condition}"
                    else:
                        query = f"SELECT * FROM {selected_table}"
                    
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    
                    if results:
                        df = pd.DataFrame(results, columns=columns)
                        st.dataframe(df, use_container_width=True)
                        st.success(f"Found {len(df)} record(s)")
                    else:
                        st.info("No records found matching the criteria")
                except Exception as e:
                    st.error(f"Error executing query: {str(e)}")

# ==================== UPDATE DATA ====================
elif operation == "✏️ Update Data":
    st.header("Update Table Data")
    
    databases = [db[0] for db in showdatabases()]
    selected_db = st.selectbox("Select Database", databases)
    
    if selected_db:
        usedatabase(selected_db)
        mycursor.execute("SHOW TABLES")
        tables = [table[0] for table in mycursor.fetchall()]
        
        selected_table = st.selectbox("Select Table", tables)
        
        if selected_table:
            mycursor.execute(f"DESCRIBE {selected_table}")
            columns_info = mycursor.fetchall()
            columns = [col[0] for col in columns_info]
            
            st.subheader(f"Update Records in {selected_table}")
            
            st.write("**SET Clause** (what to update)")
            set_values = st.text_input(
                "SET values",
                placeholder="column1 = 'value1', column2 = 'value2'"
            )
            
            st.write("**WHERE Clause** (which rows to update)")
            where_condition = st.text_input(
                "WHERE condition",
                placeholder="id = 1"
            )
            
            if st.button("Update Data", key="update_data"):
                if set_values.strip() and where_condition.strip():
                    try:
                        updatedata(selected_table, set_values, where_condition)
                        st.success(f"✅ Data updated successfully in {selected_table}!")
                    except Exception as e:
                        st.error(f"Error updating data: {str(e)}")
                else:
                    st.warning("Please fill in both SET and WHERE clauses")

# ==================== DELETE DATA ====================
elif operation == "🗑️ Delete Data":
    st.header("Delete Data from Table")
    
    databases = [db[0] for db in showdatabases()]
    selected_db = st.selectbox("Select Database", databases)
    
    if selected_db:
        usedatabase(selected_db)
        mycursor.execute("SHOW TABLES")
        tables = [table[0] for table in mycursor.fetchall()]
        
        selected_table = st.selectbox("Select Table", tables)
        
        if selected_table:
            st.subheader(f"Delete Records from {selected_table}")
            
            condition = st.text_input(
                "WHERE condition (Required)",
                placeholder="id = 5"
            )
            
            st.warning("⚠️ This will delete data from your database. Be careful!")
            
            if st.button("Delete Data", key="delete_data"):
                if condition.strip():
                    confirm = st.checkbox("I understand this action cannot be undone")
                    if confirm and st.button("Confirm Delete", key="confirm_delete"):
                        try:
                            deletedata(selected_table, condition)
                            st.success(f"✅ Data deleted successfully from {selected_table}!")
                        except Exception as e:
                            st.error(f"Error deleting data: {str(e)}")
                else:
                    st.warning("Please specify a WHERE condition")

# ==================== DROP TABLE ====================
elif operation == "🗑️ Drop Table":
    st.header("Drop Table")
    
    databases = [db[0] for db in showdatabases()]
    selected_db = st.selectbox("Select Database", databases)
    
    if selected_db:
        usedatabase(selected_db)
        mycursor.execute("SHOW TABLES")
        tables = [table[0] for table in mycursor.fetchall()]
        
        selected_table = st.selectbox("Select Table to Drop", tables)
        
        st.warning("⚠️ Dropping a table will permanently delete it and all its data!")
        
        if st.button("Drop Table", key="drop_table"):
            confirm = st.checkbox("I understand this action cannot be undone", key="drop_table_confirm")
            if confirm and st.button("Confirm Drop Table", key="confirm_drop_table"):
                try:
                    droptable(selected_table)
                    st.success(f"✅ Table '{selected_table}' dropped successfully!")
                except Exception as e:
                    st.error(f"Error dropping table: {str(e)}")

# ==================== DROP DATABASE ====================
elif operation == "🗑️ Drop Database":
    st.header("Drop Database")
    
    databases = [db[0] for db in showdatabases()]
    selected_db = st.selectbox("Select Database to Drop", databases)
    
    st.warning("⚠️ Dropping a database will permanently delete it and all its tables!")
    
    if st.button("Drop Database", key="drop_db"):
        confirm = st.checkbox("I understand this action cannot be undone", key="drop_db_confirm")
        if confirm and st.button("Confirm Drop Database", key="confirm_drop_db"):
            try:
                dropdatabase(selected_db)
                st.success(f"✅ Database '{selected_db}' dropped successfully!")
            except Exception as e:
                st.error(f"Error dropping database: {str(e)}")

# ==================== JOIN TABLES ====================
elif operation == "🔗 Join Tables":
    st.header("Join Tables")
    
    databases = [db[0] for db in showdatabases()]
    selected_db = st.selectbox("Select Database", databases)
    
    if selected_db:
        usedatabase(selected_db)
        mycursor.execute("SHOW TABLES")
        tables = [table[0] for table in mycursor.fetchall()]
        
        col1, col2 = st.columns(2)
        
        with col1:
            table1 = st.selectbox("Select First Table", tables)
        
        with col2:
            table2 = st.selectbox("Select Second Table", tables)
        
        join_condition = st.text_input(
            "Join Condition",
            placeholder="table1.id = table2.user_id"
        )
        
        if st.button("Execute Join", key="join_tables"):
            if join_condition.strip():
                try:
                    results = jointables(table1, table2, join_condition)
                    
                    # Get column names
                    mycursor.execute(f"SELECT * FROM {table1} JOIN {table2} ON {join_condition} LIMIT 0")
                    columns = [desc[0] for desc in mycursor.description]
                    
                    if results:
                        df = pd.DataFrame(results, columns=columns)
                        st.subheader(f"Join Result: {table1} ⟕ {table2}")
                        st.dataframe(df, use_container_width=True)
                        st.success(f"Found {len(df)} record(s)")
                    else:
                        st.info("No records found matching the join condition")
                except Exception as e:
                    st.error(f"Error executing join: {str(e)}")
            else:
                st.warning("Please specify a join condition")

# ==================== CUSTOM QUERY ====================
elif operation == "💬 Custom Query":
    st.header("Execute Custom Query")
    
    st.info("Execute any custom SQL query. SELECT queries return results; other queries execute modifications.")
    
    query_input = st.text_area(
        "Enter your SQL Query",
        placeholder="SELECT * FROM users WHERE age > 18;",
        height=200
    )
    
    if st.button("Execute Query", key="custom_query"):
        if query_input.strip():
            try:
                results = customquery(query_input)
                
                # Get column names if it's a SELECT query
                if results and mycursor.description:
                    columns = [desc[0] for desc in mycursor.description]
                    df = pd.DataFrame(results, columns=columns)
                    st.subheader("Query Results")
                    st.dataframe(df, use_container_width=True)
                    st.success(f"Query executed successfully. Found {len(df)} record(s)")
                else:
                    st.success("✅ Query executed successfully!")
            except Exception as e:
                st.error(f"Error executing query: {str(e)}")
        else:
            st.warning("Please enter a query")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

