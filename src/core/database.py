import sqlite3
import json
import datetime

DB_NAME = "notebook.db"

def init_db():
    """Initialize the database with the cells table."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            output TEXT,
            variables TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_cell(code, output, variables):
    """Add a new execution cell to the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO cells (code, output, variables)
        VALUES (?, ?, ?)
    ''', (code, output, json.dumps(variables)))
    conn.commit()
    conn.close()

def get_history():
    """Retrieve all execution history."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, code, output, variables, timestamp FROM cells ORDER BY id ASC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_last_state():
    """Retrieve the variables from the last execution."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT variables FROM cells ORDER BY id DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return {}

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
