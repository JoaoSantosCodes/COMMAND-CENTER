"""
Módulo de auditoria e log de alterações
"""
import json
import streamlit as st
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import config

def log_change(user: str, action: str, table: str, record_id: str, 
               old_value: dict = None, new_value: dict = None):
    """
    Registra mudança no log de auditoria
    
    Args:
        user (str): Usuário que fez a mudança
        action (str): Tipo de ação (INSERT, UPDATE, DELETE)
        table (str): Tabela afetada
        record_id (str): ID do registro
        old_value (dict, optional): Valor anterior
        new_value (dict, optional): Novo valor
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "action": action,
        "table": table,
        "record_id": record_id,
        "old_value": old_value,
        "new_value": new_value
    }
    
    log_file = Path("logs/audit_log.json")
    log_file.parent.mkdir(exist_ok=True)
    
    try:
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Erro ao salvar log: {e}")

def get_audit_log(limit: int = 100) -> list:
    """
    Obtém log de auditoria
    
    Args:
        limit (int): Limite de registros
        
    Returns:
        list: Lista de logs
    """
    log_file = Path("logs/audit_log.json")
    
    if not log_file.exists():
        return []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        
        return logs[-limit:] if limit else logs
        
    except Exception as e:
        print(f"Erro ao ler log: {e}")
        return []

def get_audit_log_filtered(table_name: str = None, 
                          start_date: str = None, 
                          end_date: str = None,
                          limit: int = 50) -> List[Dict[str, Any]]:
    """
    Carrega logs de auditoria com filtros
    
    Args:
        table_name (str, optional): Filtrar por tabela
        start_date (str, optional): Data inicial (ISO format)
        end_date (str, optional): Data final (ISO format)
        limit (int): Limite de registros
        
    Returns:
        List[Dict[str, Any]]: Lista de logs filtrados
    """
    logs = get_audit_log(limit=1000)  # Carregar mais para filtrar
    
    # Aplicar filtros
    if table_name:
        logs = [log for log in logs if log.get('table') == table_name]
    
    if start_date:
        logs = [log for log in logs if log.get('timestamp', '') >= start_date]
    
    if end_date:
        logs = [log for log in logs if log.get('timestamp', '') <= end_date]
    
    return logs[-limit:]  # Retornar apenas o limite solicitado

def export_audit_log(filename: str = "audit_log_export.csv") -> str:
    """
    Exporta logs de auditoria para CSV
    
    Args:
        filename (str): Nome do arquivo de exportação
        
    Returns:
        str: Caminho do arquivo exportado
    """
    import pandas as pd
    
    logs = get_audit_log(limit=10000)
    if not logs:
        return ""
    
    df = pd.DataFrame(logs)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp', ascending=False)
    
    df.to_csv(filename, index=False, encoding='utf-8')
    return filename

def get_audit_summary() -> Dict[str, Any]:
    """
    Retorna resumo das auditorias
    
    Returns:
        Dict[str, Any]: Resumo das auditorias
    """
    logs = get_audit_log(limit=10000)
    
    if not logs:
        return {
            'total_changes': 0,
            'tables_modified': [],
            'recent_changes': 0,
            'most_modified_fields': []
        }
    
    # Total de alterações
    total_changes = len(logs)
    
    # Tabelas modificadas
    tables = set(log['table'] for log in logs)
    
    # Alterações recentes (últimas 24h)
    recent_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    recent_changes = len([
        log for log in logs 
        if datetime.fromisoformat(log['timestamp']) >= recent_time
    ])
    
    # Campos mais modificados
    field_counts = {}
    for log in logs:
        field = log.get('field', '')
        field_counts[field] = field_counts.get(field, 0) + 1
    
    most_modified = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        'total_changes': total_changes,
        'tables_modified': list(tables),
        'recent_changes': recent_changes,
        'most_modified_fields': most_modified
    } 