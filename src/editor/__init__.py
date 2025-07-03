# Módulo de edição de dados
from .audit import log_change, get_audit_log
from .operations import update_lojas_record, update_inventario_record
from .fields import get_editable_fields_lojas, get_editable_fields_inventario

__all__ = [
    'log_change',
    'get_audit_log',
    'update_lojas_record',
    'update_inventario_record',
    'get_editable_fields_lojas',
    'get_editable_fields_inventario'
] 