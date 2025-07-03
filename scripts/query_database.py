import sqlite3
import pandas as pd

def show_database_info():
    """
    Mostra informações sobre o banco de dados
    """
    conn = sqlite3.connect("data/consulta_vd.db")
    
    print("=== INFORMAÇÕES DO BANCO DE DADOS ===")
    
    # Listar todas as tabelas
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nTabelas disponíveis:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  - {table_name}: {count} registros")
        
        # Mostrar primeiras colunas
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns[:5]]  # Primeiras 5 colunas
        print(f"    Colunas principais: {', '.join(column_names)}...")
    
    conn.close()

def query_example():
    """
    Exemplo de consultas úteis
    """
    conn = sqlite3.connect("data/consulta_vd.db")
    
    print("\n=== EXEMPLOS DE CONSULTAS ===")
    
    # Exemplo 1: Contar lojas por status
    print("\n1. Contagem de lojas por status:")
    query = """
    SELECT STATUS, COUNT(*) as quantidade
    FROM lojas_lojas
    GROUP BY STATUS
    ORDER BY quantidade DESC
    """
    df = pd.read_sql_query(query, conn)
    print(df)
    
    # Exemplo 2: Top 10 lojas com mais PDVs ativos
    print("\n2. Top 10 lojas com mais PDVs ativos:")
    query = """
    SELECT LOJAS, PDVs_ATIVOS, REGIAO_GGL, CIDADE, UF
    FROM lojas_lojas
    WHERE PDVs_ATIVOS IS NOT NULL
    ORDER BY CAST(PDVs_ATIVOS AS INTEGER) DESC
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    print(df)
    
    # Exemplo 3: Inventário por status de serviço
    print("\n3. Inventário por status de serviço:")
    query = """
    SELECT Status_Serviço, COUNT(*) as quantidade
    FROM inventario_planilha1
    GROUP BY Status_Serviço
    ORDER BY quantidade DESC
    """
    df = pd.read_sql_query(query, conn)
    print(df)
    
    # Exemplo 4: Lojas por região
    print("\n4. Lojas por região GGL:")
    query = """
    SELECT REGIAO_GGL, COUNT(*) as quantidade_lojas
    FROM lojas_lojas
    GROUP BY REGIAO_GGL
    ORDER BY quantidade_lojas DESC
    """
    df = pd.read_sql_query(query, conn)
    print(df)
    
    conn.close()

def custom_query(sql_query):
    """
    Executa uma consulta SQL personalizada
    """
    try:
        conn = sqlite3.connect("data/consulta_vd.db")
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Erro na consulta: {e}")
        return None

if __name__ == "__main__":
    show_database_info()
    query_example()
    
    print("\n=== CONSULTA PERSONALIZADA ===")
    print("Digite sua consulta SQL (ou 'sair' para encerrar):")
    
    while True:
        query = input("\nSQL> ")
        if query.lower() == 'sair':
            break
        
        if query.strip():
            result = custom_query(query)
            if result is not None:
                print(result) 