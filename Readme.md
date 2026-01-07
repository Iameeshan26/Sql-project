# SQL Project — Streamlit Dashboard & MySQL Helper

This repository provides a small SQL management project with a Streamlit-based dashboard and simple MySQL helper functions. It is intended for learning and quick prototyping of SQL operations (create databases/tables, insert/update/delete rows, run queries) via a lightweight UI.

Contents

- `app.py` — example Streamlit app template that demonstrates running SQL queries against a local SQLite database (template only).
- `streamlit_dashboard.py` — the main Streamlit dashboard that connects to MySQL using the helper in `sqlconnect.py`. It exposes: view/create/drop databases, create/drop tables, insert/update/delete/query data, joins, and custom SQL execution.
- `sqlconnect.py` — MySQL helper functions: open connection, create/use database, create/drop table, insert/update/delete rows, run custom queries.
- `sql_load.py` — simple CLI menu that uses `sqlconnect.py` functions to interactively manage databases and tables from the terminal.

Quick overview

- The dashboard uses `mysql.connector` to connect to a MySQL server. Connection parameters are in `sqlconnect.py` (host, user, password). Update these credentials to match your environment.
- The Streamlit UI reads databases and tables and constructs SQL statements — be careful when running destructive actions (DROP, DELETE).

Setup

1. Install Python dependencies (macOS example):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install the common dependencies:

```bash
pip install streamlit mysql-connector-python pandas
```

2. Configure MySQL connection

Open `sqlconnect.py` and set the connection parameters near the top:

- `host` — usually `localhost` for a local server
- `user` — your MySQL username (e.g., `root`)
- `password` — your MySQL password

Example snippet (already present in `sqlconnect.py`):

```python
import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="your_password")
mycursor = mydb.cursor()
```

Make sure the user you provide has permission to create databases/tables if you plan to use those features.

Running the Streamlit dashboard

From the repository root run:

```bash
streamlit run streamlit_dashboard.py
```

This opens the UI in your default browser. Use the sidebar to pick operations.

Inserting data (notes & tips)

- The dashboard provides a simple text-input for comma-separated values when inserting a single row. Values are passed directly to the helper in `sqlconnect.py`.
- For safety and to avoid SQL syntax errors when values contain commas or quotes, prefer using the CLI (`sql_load.py`) or modify the insert helper to accept JSON or structured input.
- When inserting strings that contain commas, wrap them properly in the input or change the insert method to accept a JSON list.

Recommended improvements

- Use parameterized queries for all write operations (INSERT/UPDATE/DELETE) to avoid SQL injection and quoting issues. The helper `sqlconnect.py` can be updated to parse input and call `cursor.execute(sql, params)`.
- Replace free-text comma-separated insert UI with a dynamic form that shows one input per column — this removes ambiguity and improves UX.
- Add input validation (types, required columns, auto-increment handling) before attempting inserts.

Troubleshooting

- "ProgrammingError" or SQL syntax errors when inserting: ensure values are correctly quoted and the number of values matches the table columns. Use `DESCRIBE table_name` to check column order.
- Connection errors: verify MySQL is running and credentials in `sqlconnect.py` are correct. Test with the MySQL client or a small Python snippet.
- Streamlit UI shows unexpected behavior after editing files: restart the Streamlit server to pick up changes.

Security and caution

- This project is educational. Do not expose the dashboard to the public with production credentials.
- Avoid running DROP/DATABASE operations on important servers.

If you want, I can:

- Update `sqlconnect.py` to use parameterized inserts and safer `customquery` handling.
- Modify `streamlit_dashboard.py` to render a per-column insert form instead of a comma-separated text input.

Feel free to ask me to make these improvements now; tell me which change you'd like first.

---

Made with ❤️ — helper README
