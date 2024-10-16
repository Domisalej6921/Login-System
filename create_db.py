import sqlite3
import bcrypt

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

# Sample user data
sample_users = [
    {
        'username': 'user1',
        'password': 'pass1234',
        'name': 'Mike Smith',
        'age': 30,
        'email': 'mike@example.com',
        'two_factor_auth': 1  # Enable 2FA
    },
    {
        'username': 'user2',
        'password': 'pass12345',
        'name': 'Niall Dexter',
        'age': 19,
        'email': 'niall@example.com',
        'two_factor_auth': 0  # Disable 2FA
    },
    {
        'username': 'user3',
        'password': 'pass123456',
        'name': 'Nicky Helena',
        'age': 67,
        'email': 'nicky@example.com',
        'two_factor_auth': 0  # Disable 2FA
    },
]

# Insert sample users into the database
for user in sample_users:
    hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''
    INSERT INTO users (username, password, name, age, email, two_factor_auth) VALUES (?, ?, ?, ?, ?, ?)
    ''', (user['username'], hashed_password.decode('utf-8'), user['name'], user['age'], user['email'], user['two_factor_auth']))

# two_factor_auth
# 0 - false, 1 - True

conn.commit()
conn.close()