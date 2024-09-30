import sqlite3

conn = sqlite3.connect('user_db.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    age TEXT NOT NULL,
    email TEXT NOT NULL
)""")

cursor.execute("""
INSERT INTO users (username, password, name, age, email) VALUES
    ('user1', 'pass123', 'Mike Smith', 30, 'mike@example.com'),
    ('user2', 'pass1234', 'Niall Dexter', 19, 'niall@example.com'),
    ('user3', 'pass12345', 'Nicky Helana', 67, 'nicky@example.com')
""")

conn.commit()
conn.close()