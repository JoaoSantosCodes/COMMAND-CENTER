# Módulo de banco de dados
from .connection import get_connection, get_tables, load_table
from .queries import unified_search_people, search_by_designation, search_by_id_vivo, search_by_address, search_by_ggl_gr, get_dashboard_stats

__all__ = [
    'get_connection',
    'get_tables', 
    'load_table',
    'unified_search_people',
    'search_by_designation',
    'search_by_id_vivo',
    'search_by_address',
    'search_by_ggl_gr',
    'get_dashboard_stats'
] 