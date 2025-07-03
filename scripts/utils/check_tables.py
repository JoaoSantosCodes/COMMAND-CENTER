import sqlite3

conn = sqlite3.connect('data/consulta_vd.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print("Tabelas encontradas:", tables)

for table in tables:
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    print(f"\nTabela {table}:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")

conn.close() 