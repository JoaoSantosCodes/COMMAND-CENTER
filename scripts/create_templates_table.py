import sqlite3
from datetime import datetime

# Caminho do banco de dados (ajuste se necessário)
db_path = 'consulta_vd.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL, -- 'informativo' ou 'alerta'
    nome TEXT NOT NULL,
    conteudo TEXT NOT NULL, -- JSON serializado
    criado_em TEXT NOT NULL -- timestamp ISO
);
''')

conn.commit()
conn.close()

print('Tabela templates criada (ou já existia).') 