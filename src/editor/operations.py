"""
Módulo de operações de edição de dados
"""
import streamlit as st
from src.editor.audit import log_change
from src.database.connection import get_connection
from typing import List, Dict, Any, Optional

# ============================================================================
# FUNÇÕES CRUD PARA API BACKEND
# ============================================================================

def get_lojas(limit: int = 50, offset: int = 0, status: Optional[str] = None, 
              uf: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """Busca lojas com filtros e paginação"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM lojas WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        if uf:
            query += " AND uf = ?"
            params.append(uf)
        if search:
            query += " AND (nome LIKE ? OR endereco LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        if results:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in results]
        
        return []
    except Exception as e:
        print(f"Erro ao buscar lojas: {e}")
        return []

def get_circuitos(limit: int = 50, offset: int = 0, operadora: Optional[str] = None,
                  status: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """Busca circuitos com filtros e paginação"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM circuitos WHERE 1=1"
        params = []
        
        if operadora:
            query += " AND operadora = ?"
            params.append(operadora)
        if status:
            query += " AND status = ?"
            params.append(status)
        if search:
            query += " AND (designacao LIKE ? OR operadora LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        if results:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in results]
        
        return []
    except Exception as e:
        print(f"Erro ao buscar circuitos: {e}")
        return []

def get_inventario(limit: int = 50, offset: int = 0, status: Optional[str] = None,
                   search: Optional[str] = None) -> List[Dict[str, Any]]:
    """Busca inventário com filtros e paginação"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM inventario WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        if search:
            query += " AND (equipamento LIKE ? OR modelo LIKE ? OR serial LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        if results:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in results]
        
        return []
    except Exception as e:
        print(f"Erro ao buscar inventário: {e}")
        return []

def create_loja(loja_data: Dict[str, Any]) -> Dict[str, Any]:
    """Cria uma nova loja"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        fields = list(loja_data.keys())
        placeholders = ", ".join(["?" for _ in fields])
        values = list(loja_data.values())
        
        query = f"INSERT INTO lojas ({', '.join(fields)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        
        loja_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Buscar a loja criada
        return get_loja_by_id(loja_id)
    except Exception as e:
        print(f"Erro ao criar loja: {e}")
        raise

def update_loja(loja_id: int, loja_data: Dict[str, Any]) -> Dict[str, Any]:
    """Atualiza uma loja existente"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Buscar valores antigos para log
        cursor.execute("SELECT * FROM lojas WHERE id = ?", (loja_id,))
        old_data = cursor.fetchone()
        if not old_data:
            raise ValueError("Loja não encontrada")
        
        # Construir query de update
        fields = list(loja_data.keys())
        set_clause = ", ".join([f"{field} = ?" for field in fields])
        values = list(loja_data.values()) + [loja_id]
        
        query = f"UPDATE lojas SET {set_clause} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        # Log das alterações
        for field, new_value in loja_data.items():
            old_value = old_data[list(old_data.keys()).index(field)] if field in old_data else None
            log_change("lojas", loja_id, field, old_value, new_value)
        
        return get_loja_by_id(loja_id)
    except Exception as e:
        print(f"Erro ao atualizar loja: {e}")
        raise

def delete_loja(loja_id: int) -> bool:
    """Deleta uma loja"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM lojas WHERE id = ?", (loja_id,))
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Erro ao deletar loja: {e}")
        return False

def create_circuito(circuito_data: Dict[str, Any]) -> Dict[str, Any]:
    """Cria um novo circuito"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        fields = list(circuito_data.keys())
        placeholders = ", ".join(["?" for _ in fields])
        values = list(circuito_data.values())
        
        query = f"INSERT INTO circuitos ({', '.join(fields)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        
        circuito_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return get_circuito_by_id(circuito_id)
    except Exception as e:
        print(f"Erro ao criar circuito: {e}")
        raise

def update_circuito(circuito_id: int, circuito_data: Dict[str, Any]) -> Dict[str, Any]:
    """Atualiza um circuito existente"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        fields = list(circuito_data.keys())
        set_clause = ", ".join([f"{field} = ?" for field in fields])
        values = list(circuito_data.values()) + [circuito_id]
        
        query = f"UPDATE circuitos SET {set_clause} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        return get_circuito_by_id(circuito_id)
    except Exception as e:
        print(f"Erro ao atualizar circuito: {e}")
        raise

def delete_circuito(circuito_id: int) -> bool:
    """Deleta um circuito"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM circuitos WHERE id = ?", (circuito_id,))
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Erro ao deletar circuito: {e}")
        return False

def create_inventario_item(item_data: Dict[str, Any]) -> Dict[str, Any]:
    """Cria um novo item de inventário"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        fields = list(item_data.keys())
        placeholders = ", ".join(["?" for _ in fields])
        values = list(item_data.values())
        
        query = f"INSERT INTO inventario ({', '.join(fields)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return get_inventario_item_by_id(item_id)
    except Exception as e:
        print(f"Erro ao criar item de inventário: {e}")
        raise

def update_inventario_item(item_id: int, item_data: Dict[str, Any]) -> Dict[str, Any]:
    """Atualiza um item de inventário existente"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        fields = list(item_data.keys())
        set_clause = ", ".join([f"{field} = ?" for field in fields])
        values = list(item_data.values()) + [item_id]
        
        query = f"UPDATE inventario SET {set_clause} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        return get_inventario_item_by_id(item_id)
    except Exception as e:
        print(f"Erro ao atualizar item de inventário: {e}")
        raise

def delete_inventario_item(item_id: int) -> bool:
    """Deleta um item de inventário"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM inventario WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Erro ao deletar item de inventário: {e}")
        return False

# Funções auxiliares
def get_loja_by_id(loja_id: int) -> Optional[Dict[str, Any]]:
    """Busca uma loja por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lojas WHERE id = ?", (loja_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, result))
        return None
    except Exception as e:
        print(f"Erro ao buscar loja por ID: {e}")
        return None

def get_circuito_by_id(circuito_id: int) -> Optional[Dict[str, Any]]:
    """Busca um circuito por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM circuitos WHERE id = ?", (circuito_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, result))
        return None
    except Exception as e:
        print(f"Erro ao buscar circuito por ID: {e}")
        return None

def get_inventario_item_by_id(item_id: int) -> Optional[Dict[str, Any]]:
    """Busca um item de inventário por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventario WHERE id = ?", (item_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, result))
        return None
    except Exception as e:
        print(f"Erro ao buscar item de inventário por ID: {e}")
        return None

# ============================================================================
# FUNÇÕES ORIGINAIS DO MÓDULO
# ============================================================================

def update_lojas_record(peop_code: str, field: str, new_value: str) -> bool:
    """
    Atualiza registro na tabela lojas_lojas com log
    
    Args:
        peop_code (str): Código PEOP do registro
        field (str): Campo a ser atualizado
        new_value (str): Novo valor
        
    Returns:
        bool: True se atualizado com sucesso, False caso contrário
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Buscar valor anterior para o log
        cursor.execute(f'SELECT "{field}" FROM lojas_lojas WHERE PEOP = ?', (peop_code,))
        result = cursor.fetchone()
        old_value = result[0] if result else None
        
        # Atualizar registro
        cursor.execute(f'UPDATE lojas_lojas SET "{field}" = ? WHERE PEOP = ?', (new_value, peop_code))
        conn.commit()
        conn.close()
        
        # Registrar no log
        log_change("lojas_lojas", peop_code, field, old_value, new_value)
        
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False

def update_inventario_record(people_code: str, field: str, new_value: str) -> bool:
    """
    Atualiza registro na tabela inventario_planilha1 com log
    
    Args:
        people_code (str): Código People do registro
        field (str): Campo a ser atualizado
        new_value (str): Novo valor
        
    Returns:
        bool: True se atualizado com sucesso, False caso contrário
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Buscar valor anterior para o log
        cursor.execute(f'SELECT "{field}" FROM inventario_planilha1 WHERE People = ?', (people_code,))
        result = cursor.fetchone()
        old_value = result[0] if result else None
        
        # Atualizar registro
        cursor.execute(f'UPDATE inventario_planilha1 SET "{field}" = ? WHERE People = ?', (new_value, people_code))
        conn.commit()
        conn.close()
        
        # Registrar no log
        log_change("inventario_planilha1", people_code, field, old_value, new_value)
        
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
        return False

def get_record_by_id(table: str, record_id: str) -> dict:
    """
    Busca um registro específico por ID
    
    Args:
        table (str): Nome da tabela
        record_id (str): ID do registro
        
    Returns:
        dict: Dados do registro ou None se não encontrado
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if table == "lojas_lojas":
            cursor.execute("SELECT * FROM lojas_lojas WHERE PEOP = ?", (record_id,))
        elif table == "inventario_planilha1":
            cursor.execute("SELECT * FROM inventario_planilha1 WHERE People = ?", (record_id,))
        else:
            return None
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Converter para dict
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, result))
        
        return None
    except Exception as e:
        st.error(f"Erro ao buscar registro: {e}")
        return None

def validate_field_value(table: str, field: str, value: str) -> tuple[bool, str]:
    """
    Valida um valor de campo antes da atualização
    
    Args:
        table (str): Nome da tabela
        field (str): Nome do campo
        value (str): Valor a ser validado
        
    Returns:
        tuple[bool, str]: (é_válido, mensagem_erro)
    """
    # Validações básicas
    if value is None or value == "":
        return True, ""  # Campos vazios são permitidos
    
    # Validações específicas por campo
    if field == "CEP":
        # Validar formato de CEP (apenas números)
        if not value.replace("-", "").isdigit() or len(value.replace("-", "")) != 8:
            return False, "CEP deve ter 8 dígitos numéricos"
    
    elif field == "TELEFONE1" or field == "TELEFONE2" or field == "CELULAR":
        # Validar formato de telefone
        clean_phone = value.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        if not clean_phone.isdigit() or len(clean_phone) < 10:
            return False, "Telefone deve ter pelo menos 10 dígitos"
    
    elif field == "E_MAIL":
        # Validação básica de email
        if "@" not in value or "." not in value:
            return False, "Email deve ter formato válido"
    
    elif field == "UF":
        # Validar UF (2 letras)
        if len(value) != 2 or not value.isalpha():
            return False, "UF deve ter 2 letras"
    
    return True, ""

def batch_update_records(table: str, updates: list) -> dict:
    """
    Atualiza múltiplos registros em lote
    
    Args:
        table (str): Nome da tabela
        updates (list): Lista de tuplas (id, field, new_value)
        
    Returns:
        dict: Resultado da operação em lote
    """
    results = {
        'success': 0,
        'errors': 0,
        'error_messages': []
    }
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        for record_id, field, new_value in updates:
            try:
                # Validar valor
                is_valid, error_msg = validate_field_value(table, field, new_value)
                if not is_valid:
                    results['errors'] += 1
                    results['error_messages'].append(f"Registro {record_id}: {error_msg}")
                    continue
                
                # Buscar valor anterior
                if table == "lojas_lojas":
                    cursor.execute(f'SELECT "{field}" FROM lojas_lojas WHERE PEOP = ?', (record_id,))
                else:
                    cursor.execute(f'SELECT "{field}" FROM inventario_planilha1 WHERE People = ?', (record_id,))
                
                result = cursor.fetchone()
                old_value = result[0] if result else None
                
                # Atualizar
                if table == "lojas_lojas":
                    cursor.execute(f'UPDATE lojas_lojas SET "{field}" = ? WHERE PEOP = ?', (new_value, record_id))
                else:
                    cursor.execute(f'UPDATE inventario_planilha1 SET "{field}" = ? WHERE People = ?', (new_value, record_id))
                
                # Log da alteração
                log_change(table, record_id, field, old_value, new_value)
                results['success'] += 1
                
            except Exception as e:
                results['errors'] += 1
                results['error_messages'].append(f"Registro {record_id}: {str(e)}")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        results['errors'] += 1
        results['error_messages'].append(f"Erro geral: {str(e)}")
    
    return results 