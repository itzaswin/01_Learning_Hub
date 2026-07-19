import sqlite3

conn = sqlite3.connect("db\\users.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cur.execute("INSERT INTO users(username,password) VALUES('admin','admin123')")

conn.commit()
conn.close()

print("Database Created")