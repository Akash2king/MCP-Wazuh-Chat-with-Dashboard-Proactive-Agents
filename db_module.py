import sqlite3
from datetime import datetime

DB_FILE = "chat_logs.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT,
                timestamp TEXT
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS tools_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT,
                usage TEXT,
                timestamp TEXT
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proactive_enabled INTEGER,
                proactive_interval INTEGER
                )""")
    # Default preference
    c.execute("SELECT COUNT(*) FROM preferences")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO preferences (proactive_enabled, proactive_interval) VALUES (?,?)", (1, 60))
    conn.commit()
    conn.close()

def save_message(role, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO messages (role, content, timestamp) VALUES (?,?,?)",
              (role, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_tool_log(tool_name, usage):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO tools_log (tool_name, usage, timestamp) VALUES (?,?,?)",
              (tool_name, usage, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def get_all_tool_logs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT tool_name, usage, timestamp FROM tools_log ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows

def get_user_preferences():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT proactive_enabled, proactive_interval FROM preferences LIMIT 1")
    row = c.fetchone()
    conn.close()
    return {"enabled": bool(row[0]), "interval": row[1]}

def update_user_preferences(enabled, interval):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE preferences SET proactive_enabled=?, proactive_interval=? WHERE id=1", (int(enabled), interval))
    conn.commit()
    conn.close()
