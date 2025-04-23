import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("SELECT email, is_admin FROM users")
users = c.fetchall()
for user in users:
    print(f"Email: {user[0]}, Admin: {user[1]}")
conn.close()