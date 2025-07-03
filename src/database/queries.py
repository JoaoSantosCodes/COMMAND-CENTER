"""
Módulo de queries específicas do sistema ConsultaVD
"""
import pandas as pd
from src.database.connection import get_connection
from src.cache import get_cached_data, set_cached_data

def unified_search_people(people_code: str) -> pd.DataFrame:
    """
    Busca unificada por código People/PEOP em ambas as tabelas
    
    Args:
        people_code (str): Código People/PEOP a ser buscado
        
    Returns:
        pd.DataFrame: Resultados unificados da busca
    """
    # Tentar obter do cache primeiro
    cached_result = get_cached_data('unified_search_people', people_code)
    if cached_result is not None:
        return cached_result
    
    conn = get_connection()
    query = '''
    SELECT
        i.People as "People/PEOP",
        COALESCE(i.Status_Loja, l.STATUS) as Status_Loja,
        l.LOJAS,
        l.CODIGO,
        l."ENDEREÇO",
        l.BAIRRO,
        l.CIDADE,
        l.UF,
        l.CEP,
        l.TELEFONE1,
        l.TELEFONE2,
        l.CELULAR,
        l."E_MAIL" as E_MAIL,
        l."2ª_a_6ª",
        l.SAB,
        l.DOM,
        l."FUNC.",
        l.VD_NOVO,
        l.NOME_GGL,
        l.NOME_GR
    FROM inventario_planilha1 i
    LEFT JOIN lojas_lojas l ON i.People = l.PEOP
    WHERE i.People = ?
    UNION
    SELECT
        l.PEOP as "People/PEOP",
        l.STATUS as Status_Loja,
        l.LOJAS,
        l.CODIGO,
        l."ENDEREÇO",
        l.BAIRRO,
        l.CIDADE,
        l.UF,
        l.CEP,
        l.TELEFONE1,
        l.TELEFONE2,
        l.CELULAR,
        l."E_MAIL",
        l."2ª_a_6ª",
        l.SAB,
        l.DOM,
        l."FUNC.",
        l.VD_NOVO,
        l.NOME_GGL,
        l.NOME_GR
    FROM lojas_lojas l
    WHERE l.PEOP = ? AND l.PEOP NOT IN (SELECT People FROM inventario_planilha1)
    '''
    df = pd.read_sql_query(query, conn, params=(people_code, people_code))
    conn.close()
    
    # Armazenar no cache por 5 minutos
    set_cached_data(df, 300, 'unified_search_people', people_code)
    
    return df

def search_by_designation(designation: str) -> pd.DataFrame:
    """
    Busca por designação de circuito
    
    Args:
        designation (str): Designação a ser buscada
        
    Returns:
        pd.DataFrame: Resultados da busca
    """
    # Tentar obter do cache primeiro
    cached_result = get_cached_data('search_by_designation', designation)
    if cached_result is not None:
        return cached_result
    
    conn = get_connection()
    query = '''
    SELECT
        i.People as "People/PEOP",
        COALESCE(i.Status_Loja, l.STATUS) as Status_Loja,
        l.LOJAS,
        l.CODIGO,
        l."ENDEREÇO",
        l.BAIRRO,
        l.CIDADE,
        l.UF,
        l.CEP,
        l.TELEFONE1,
        l.TELEFONE2,
        l.CELULAR,
        l."E_MAIL" as E_MAIL,
        l."2ª_a_6ª",
        l.SAB,
        l.DOM,
        l."FUNC.",
        l.VD_NOVO,
        l.NOME_GGL,
        l.NOME_GR,
        i.Circuito_Designação,
        i.Novo_Circuito_Designação,
        i.Operadora
    FROM inventario_planilha1 i
    LEFT JOIN lojas_lojas l ON i.People = l.PEOP
    WHERE i.Circuito_Designação LIKE ? OR i.Novo_Circuito_Designação LIKE ?
    ORDER BY l.LOJAS
    '''
    search_term = f"%{designation}%"
    df = pd.read_sql_query(query, conn, params=(search_term, search_term))
    conn.close()
    
    # Armazenar no cache por 5 minutos
    set_cached_data(df, 300, 'search_by_designation', designation)
    
    return df

def search_by_id_vivo(id_vivo: str) -> pd.DataFrame:
    """
    Busca por ID Vivo
    
    Args:
        id_vivo (str): ID Vivo a ser buscado
        
    Returns:
        pd.DataFrame: Resultados da busca
    """
    # Tentar obter do cache primeiro
    cached_result = get_cached_data('search_by_id_vivo', id_vivo)
    if cached_result is not None:
        return cached_result
    
    conn = get_connection()
    query = '''
    SELECT
        i.People as "People/PEOP",
        COALESCE(i.Status_Loja, l.STATUS) as Status_Loja,
        l.LOJAS,
        l.CODIGO,
        l."ENDEREÇO",
        l.BAIRRO,
        l.CIDADE,
        l.UF,
        l.CEP,
        l.TELEFONE1,
        l.TELEFONE2,
        l.CELULAR,
        l."E_MAIL" as E_MAIL,
        l."2ª_a_6ª",
        l.SAB,
        l.DOM,
        l."FUNC.",
        l.VD_NOVO,
        l.NOME_GGL,
        l.NOME_GR,
        i.ID_VIVO,
        i.Novo_ID_Vivo,
        i.Operadora
    FROM inventario_planilha1 i
    LEFT JOIN lojas_lojas l ON i.People = l.PEOP
    WHERE i.ID_VIVO LIKE ? OR i.Novo_ID_Vivo LIKE ?
    ORDER BY l.LOJAS
    '''
    search_term = f"%{id_vivo}%"
    df = pd.read_sql_query(query, conn, params=(search_term, search_term))
    conn.close()
    
    # Armazenar no cache por 5 minutos
    set_cached_data(df, 300, 'search_by_id_vivo', id_vivo)
    
    return df

def search_by_address(address: str) -> pd.DataFrame:
    """
    Busca por endereço, bairro ou cidade
    
    Args:
        address (str): Endereço a ser buscado
        
    Returns:
        pd.DataFrame: Resultados da busca
    """
    # Tentar obter do cache primeiro
    cached_result = get_cached_data('search_by_address', address)
    if cached_result is not None:
        return cached_result
    
    conn = get_connection()
    query = '''
    SELECT
        l.PEOP as "People/PEOP",
        l.STATUS as Status_Loja,
        l.LOJAS,
        l.CODIGO,
        l."ENDEREÇO",
        l.BAIRRO,
        l.CIDADE,
        l.UF,
        l.CEP,
        l.TELEFONE1,
        l.TELEFONE2,
        l.CELULAR,
        l."E_MAIL",
        l."2ª_a_6ª",
        l.SAB,
        l.DOM,
        l."FUNC.",
        l.VD_NOVO,
        l.NOME_GGL,
        l.NOME_GR
    FROM lojas_lojas l
    WHERE l."ENDEREÇO" LIKE ? OR l.BAIRRO LIKE ? OR l.CIDADE LIKE ?
    ORDER BY l.LOJAS
    '''
    search_term = f"%{address}%"
    df = pd.read_sql_query(query, conn, params=(search_term, search_term, search_term))
    conn.close()
    
    # Armazenar no cache por 5 minutos
    set_cached_data(df, 300, 'search_by_address', address)
    
    return df

def search_by_ggl_gr(name: str) -> pd.DataFrame:
    """
    Busca por GGL ou GR
    
    Args:
        name (str): Nome do GGL ou GR
        
    Returns:
        pd.DataFrame: Resultados da busca
    """
    # Tentar obter do cache primeiro
    cached_result = get_cached_data('search_by_ggl_gr', name)
    if cached_result is not None:
        return cached_result
    
    conn = get_connection()
    query = '''
    SELECT
        l.PEOP as "People/PEOP",
        l.STATUS as Status_Loja,
        l.LOJAS,
        l.CODIGO,
        l."ENDEREÇO",
        l.BAIRRO,
        l.CIDADE,
        l.UF,
        l.CEP,
        l.TELEFONE1,
        l.TELEFONE2,
        l.CELULAR,
        l."E_MAIL",
        l."2ª_a_6ª",
        l.SAB,
        l.DOM,
        l."FUNC.",
        l.VD_NOVO,
        l.NOME_GGL,
        l.NOME_GR
    FROM lojas_lojas l
    WHERE l.NOME_GGL LIKE ? OR l.NOME_GR LIKE ?
    ORDER BY l.LOJAS
    '''
    search_term = f"%{name}%"
    df = pd.read_sql_query(query, conn, params=(search_term, search_term))
    conn.close()
    
    # Armazenar no cache por 5 minutos
    set_cached_data(df, 300, 'search_by_ggl_gr', name)
    
    return df

def get_dashboard_stats() -> dict:
    """
    Retorna estatísticas para o dashboard
    
    Returns:
        dict: Estatísticas do sistema
    """
    # Tentar obter do cache primeiro (cache mais longo para estatísticas)
    cached_result = get_cached_data('get_dashboard_stats')
    if cached_result is not None:
        return cached_result
    
    conn = get_connection()
    stats = {}
    
    # Total de lojas
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM lojas_lojas")
    stats['total_lojas'] = cursor.fetchone()[0]
    
    # Lojas por status
    cursor.execute("""
        SELECT STATUS, COUNT(*) as count 
        FROM lojas_lojas 
        GROUP BY STATUS 
        ORDER BY count DESC
    """)
    stats['lojas_por_status'] = dict(cursor.fetchall())
    
    # Total de circuitos
    cursor.execute("SELECT COUNT(*) FROM inventario_planilha1")
    stats['total_circuitos'] = cursor.fetchone()[0]
    
    # Circuitos por operadora
    cursor.execute("""
        SELECT Operadora, COUNT(*) as count 
        FROM inventario_planilha1 
        WHERE Operadora IS NOT NULL
        GROUP BY Operadora 
        ORDER BY count DESC
    """)
    stats['circuitos_por_operadora'] = dict(cursor.fetchall())
    
    # Lojas por UF
    cursor.execute("""
        SELECT UF, COUNT(*) as count 
        FROM lojas_lojas 
        WHERE UF IS NOT NULL
        GROUP BY UF 
        ORDER BY count DESC
    """)
    stats['lojas_por_uf'] = dict(cursor.fetchall())
    
    conn.close()
    
    # Armazenar no cache por 10 minutos (estatísticas mudam menos frequentemente)
    set_cached_data(stats, 600, 'get_dashboard_stats')
    
    return stats 

def search_circuits_by_operator(operadora: str) -> pd.DataFrame:
    """
    Busca todas as lojas e circuitos de uma operadora específica.
    """
    # Tentar obter do cache primeiro
    cached_result = get_cached_data('search_circuits_by_operator', operadora)
    if cached_result is not None:
        return cached_result
    
    conn = get_connection()
    query = '''
    SELECT i.People as "People/PEOP", l.LOJAS, i.Operadora, i.Circuito_Designação, i.Novo_Circuito_Designação
    FROM inventario_planilha1 i
    LEFT JOIN lojas_lojas l ON i.People = l.PEOP
    WHERE i.Operadora LIKE ?
    ORDER BY l.LOJAS
    '''
    search_term = f"%{operadora}%"
    df = pd.read_sql_query(query, conn, params=(search_term,))
    conn.close()
    
    # Armazenar no cache por 5 minutos
    set_cached_data(df, 300, 'search_circuits_by_operator', operadora)
    
    return df 