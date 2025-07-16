import sqlite3

# Caminho do banco de dados (ajuste se necessário)
db_path = 'consulta_vd.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    user TEXT,
    action TEXT,
    table_name TEXT,
    record_id TEXT,
    old_value TEXT,
    new_value TEXT
);
''')

conn.commit()
conn.close()

print('Tabela audit_log criada (ou já existia).') 