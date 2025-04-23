import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("UPDATE users SET is_admin = 1 WHERE email = ?", ('adminl@gmail.com',))
conn.commit()
conn.close()
print("Usuário atualizado como administrador.")