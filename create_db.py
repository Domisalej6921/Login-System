import sqlite3

conn = sqlite3.connect('user_db.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    age TEXT NOT NULL,
    email TEXT NOT NULL,
    two_factor_auth INTEGER NOT NULL               
)""")

# two_factor_auth
# 0 - false, 1 - True

conn.commit()
conn.close()