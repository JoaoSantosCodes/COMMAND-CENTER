import pandas as pd
import sqlite3
import os
from pathlib import Path

def excel_to_sqlite():
    """
    Converte planilhas Excel para um banco SQLite
    """
    # Nome do banco SQLite
    db_name = "consulta_vd.db"
    
    # Conectar ao banco SQLite (cria se não existir)
    conn = sqlite3.connect(db_name)
    
    try:
        # 1. Processar Inventario.xlsx
        print("Processando Inventario.xlsx...")
        if os.path.exists("Inventario.xlsx"):
            # Ler todas as abas da planilha
            excel_file = pd.ExcelFile("Inventario.xlsx")
            
            for sheet_name in excel_file.sheet_names:
                print(f"  - Processando aba: {sheet_name}")
                df = pd.read_excel("Inventario.xlsx", sheet_name=sheet_name)
                
                # Limpar nomes das colunas (remover espaços e caracteres especiais)
                df.columns = [col.strip().replace(' ', '_').replace('-', '_').replace('/', '_') 
                             for col in df.columns]
                
                # Salvar no SQLite
                table_name = f"inventario_{sheet_name.lower().replace(' ', '_')}"
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"    ✓ Tabela '{table_name}' criada com {len(df)} registros")
        
        # 2. Processar Relação de Lojas.xlsx
        print("\nProcessando Relação de Lojas.xlsx...")
        if os.path.exists("Relação de Lojas.xlsx"):
            # Ler todas as abas da planilha
            excel_file = pd.ExcelFile("Relação de Lojas.xlsx")
            
            for sheet_name in excel_file.sheet_names:
                print(f"  - Processando aba: {sheet_name}")
                df = pd.read_excel("Relação de Lojas.xlsx", sheet_name=sheet_name)
                
                # Limpar nomes das colunas
                df.columns = [col.strip().replace(' ', '_').replace('-', '_').replace('/', '_') 
                             for col in df.columns]
                
                # Salvar no SQLite
                table_name = f"lojas_{sheet_name.lower().replace(' ', '_')}"
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"    ✓ Tabela '{table_name}' criada com {len(df)} registros")
        
        # 3. Mostrar informações do banco criado
        print(f"\n✓ Banco SQLite '{db_name}' criado com sucesso!")
        
        # Listar todas as tabelas criadas
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\nTabelas criadas:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} registros")
            
            # Mostrar estrutura da tabela
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"    Colunas: {', '.join([col[1] for col in columns])}")
        
    except Exception as e:
        print(f"Erro ao processar as planilhas: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    excel_to_sqlite() 