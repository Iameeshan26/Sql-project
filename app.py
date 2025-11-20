import streamlit as st
import pandas as pd
import sqlite3

# --- 1. CONFIGURATION AND INITIAL SETUP ---
# Set the page configuration
st.set_page_config(
    page_title="SQL Project Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to execute SQL queries
def run_query(query):
    # IMPORTANT: Replace 'your_database.db' with your actual SQLite database file name.
    # If using MySQL/PostgreSQL, you'd need libraries like 'mysql.connector' or 'psycopg2'
    # and connection details (host, user, password, etc.).
    try:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        cursor.execute(query)
        # Fetch data only if it's a SELECT query
        if query.strip().upper().startswith('SELECT'):
            data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result_df = pd.DataFrame(data, columns=columns)
            return result_df, "Query executed successfully!"
        else:
            conn.commit()
            return None, f"Command '{query.split()[0].upper()}' executed and database updated."
    except sqlite3.Error as e:
        return None, f"Database Error: {e}"
    finally:
        if 'conn' in locals() and conn:
            conn.close()

# --- 2. STREAMLIT APP LAYOUT ---

# Header Section
st.title("📊 SQL Project Analysis Tool")
st.markdown("### Powered by Streamlit")

# Sidebar for Navigation/Details
st.sidebar.header("Project Details")
st.sidebar.markdown(
    """
    This app serves as an interactive frontend for the SQL project 
    from the GitHub repository: 
    [Iameeshan26/Sql-project](https://github.com/Iameeshan26/Sql-project.git)
    """
)
st.sidebar.info("You can enter and execute any valid SQL query in the main window.")

# --- 3. MAIN QUERY EXECUTION SECTION ---

st.header("Custom SQL Query Runner")
st.warning("⚠️ **NOTE:** This template uses a local **SQLite** database connection. Ensure your database file (`your_database.db`) is in the same directory as this script.")

# Text area for user input query
sql_query = st.text_area(
    "Enter your SQL Query below (e.g., `SELECT * FROM table_name LIMIT 10;`)",
    height=150,
    value="SELECT name FROM sqlite_master WHERE type='table';" # Default query to show tables
)

# Execute Button
if st.button("Execute Query", type="primary"):
    with st.spinner('Executing SQL query...'):
        df, message = run_query(sql_query)
        
        # Display Status/Error Message
        if "Error" in message:
            st.error(message)
        else:
            st.success(message)

            # Display Results if it was a SELECT query
            if df is not None:
                st.subheader(f"Query Results ({len(df)} rows)")
                # Use st.dataframe for an interactive table
                st.dataframe(df)

# --- 4. PRE-DEFINED QUERIES (Optional) ---
# You can add buttons for key project queries here
st.markdown("---")
st.header("Key Project Insights")

if st.button("Show Project's Main Query Results"):
    # Replace the query below with the primary analytical query from your SQL project
    main_query = """
    -- EXAMPLE: Find the top 5 customers by total purchase amount
    SELECT 
        customer_name, 
        SUM(total_amount) AS total_spent 
    FROM 
        sales_data 
    GROUP BY 
        customer_name 
    ORDER BY 
        total_spent DESC 
    LIMIT 5;
    """
    st.code(main_query, language="sql")
    
    with st.spinner('Running main project analysis...'):
        df, message = run_query(main_query)
        
        if "Error" in message:
            st.error(message)
        elif df is not None:
            st.success("Main query executed successfully!")
            st.dataframe(df)
            st.line_chart(df.set_index(df.columns[0])) # Example visualization