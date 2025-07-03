"""
Módulo de conexão com banco de dados SQLite
"""
import sqlite3
import pandas as pd
from typing import List, Optional
from pathlib import Path
import config

def get_connection():
    """
    Obtém conexão com o banco de dados
    
    Returns:
        sqlite3.Connection: Conexão com o banco
    """
    db_path = config.get_config("database", "path")
    return sqlite3.connect(db_path)

def get_tables() -> List[str]:
    """
    Retorna lista de todas as tabelas do banco
    
    Returns:
        List[str]: Lista de nomes das tabelas
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    return tables

def load_table(table: str, limit: int = 100, offset: int = 0) -> pd.DataFrame:
    """
    Carrega dados de uma tabela específica
    
    Args:
        table (str): Nome da tabela
        limit (int): Limite de registros a carregar
        offset (int): Offset inicial
        
    Returns:
        pd.DataFrame: DataFrame com os dados da tabela
    """
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT {limit} OFFSET {offset}", conn)
    conn.close()
    return df

def get_table_info(table: str) -> dict:
    """
    Retorna informações sobre uma tabela específica
    
    Args:
        table (str): Nome da tabela
        
    Returns:
        dict: Informações da tabela (colunas, tipos, etc.)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Informações das colunas
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    
    # Contagem de registros
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'name': table,
        'columns': columns,
        'record_count': count
    }

def execute_query(query: str, params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Executa uma query SQL personalizada
    
    Args:
        query (str): Query SQL a ser executada
        params (tuple, optional): Parâmetros da query
        
    Returns:
        pd.DataFrame: Resultado da query
    """
    conn = get_connection()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

def insert_row(table: str, data: dict) -> int:
    """
    Insere um registro na tabela e retorna o id inserido
    """
    conn = get_connection()
    cursor = conn.cursor()
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    values = tuple(data.values())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, values)
    conn.commit()
    rowid = cursor.lastrowid
    conn.close()
    return rowid

def update_row(table: str, pk_col: str, pk_value: any, data: dict) -> int:
    """
    Atualiza um registro na tabela pela chave primária
    """
    conn = get_connection()
    cursor = conn.cursor()
    set_clause = ', '.join([f"{k}=?" for k in data.keys()])
    values = tuple(data.values()) + (pk_value,)
    sql = f"UPDATE {table} SET {set_clause} WHERE {pk_col} = ?"
    cursor.execute(sql, values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def delete_row(table: str, pk_col: str, pk_value: any) -> int:
    """
    Remove um registro da tabela pela chave primária
    """
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"DELETE FROM {table} WHERE {pk_col} = ?"
    cursor.execute(sql, (pk_value,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def get_primary_key_column(table: str) -> str:
    """
    Retorna o nome da coluna de chave primária da tabela
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    pk_col = None
    for col in columns:
        if col[5] == 1:  # 6a coluna = pk
            pk_col = col[1]
            break
    conn.close()
    if not pk_col:
        raise Exception(f"Tabela {table} não possui chave primária")
    return pk_col 