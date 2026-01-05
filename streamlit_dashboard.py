import streamlit as st
import pandas as pd
from sqlconnect import mycursor, showdatabases, usedatabase

st.set_page_config(page_title="SQL Table Exporter", layout="wide")
st.title("SQL Table Exporter")

def to_sql_literal(val):
	if val is None:
		return "NULL"
	if isinstance(val, bool):
		return '1' if val else '0'
	if isinstance(val, (int, float)):
		return str(val)
	s = str(val).replace("'", "''")
	return f"'{s}'"

dbs = [d[0] for d in showdatabases()]
selected_db = st.selectbox("Select database", ["-- choose --"] + dbs)

if selected_db and selected_db != "-- choose --":
	usedatabase(selected_db)
	mycursor.execute("SHOW TABLES")
	tables = [t[0] for t in mycursor.fetchall()]
	selected_table = st.selectbox("Select table", ["-- choose --"] + tables)

	if selected_table and selected_table != "-- choose --":
		limit = st.number_input("Max rows to load (0 = all)", min_value=0, value=1000, step=100)
		load = st.button("Load table")

		if load:
			q = f"SELECT * FROM `{selected_table}`"
			if limit and limit > 0:
				q += f" LIMIT {int(limit)}"
			mycursor.execute(q)
			rows = mycursor.fetchall()
			cols = [c[0] for c in mycursor.description]
			df = pd.DataFrame(rows, columns=cols)

			st.subheader(f"Preview: {selected_db}.{selected_table} ({len(df)} rows)")
			st.dataframe(df)

			# Build SQL INSERTs
			col_list = ", ".join([f"`{c}`" for c in cols])
			inserts = []
			for r in rows:
				vals = ", ".join(to_sql_literal(v) for v in r)
				inserts.append(f"INSERT INTO `{selected_table}` ({col_list}) VALUES ({vals});")
			sql_text = "\n".join(inserts)

			st.download_button("Download SQL INSERTs", sql_text, file_name=f"{selected_db}_{selected_table}.sql", mime="text/sql")
			st.subheader("Generated SQL (first 5000 chars)")
			st.code(sql_text[:5000], language="sql")

			if len(sql_text) > 5000:
				st.info("Download contains the full SQL. Preview is truncated.")

