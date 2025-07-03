import sqlite3
from datetime import datetime

# Caminho do banco de dados
db_path = 'consulta_vd.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
INSERT INTO audit_log (timestamp, user, action, table_name, record_id, old_value, new_value)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    datetime.now().isoformat(),
    'admin',
    'INSERT',
    'lojas',
    '1',
    '{}',
    '{"nome": "Loja Teste", "status": "ATIVA"}'
))

conn.commit()
conn.close()

print('Registro de teste inserido na tabela audit_log.') 