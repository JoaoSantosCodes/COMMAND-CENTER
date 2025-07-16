import sqlite3
import os

DB_PATH = os.path.join('data', 'consulta_vd.db')

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    nome TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    criado_em TEXT NOT NULL
);
'''

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()
    print('Tabela templates criada ou já existente.')

if __name__ == '__main__':
    main() 