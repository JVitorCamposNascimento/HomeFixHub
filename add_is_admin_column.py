import sqlite3

try:
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
    conn.commit()
    print("Coluna is_admin adicionada com sucesso.")
except sqlite3.OperationalError as e:
    print(f"Erro: {e}")
finally:
    conn.close()