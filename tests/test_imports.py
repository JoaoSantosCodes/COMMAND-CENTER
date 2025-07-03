import pytest

def test_import_ui_components():
    from src.ui import (
        copy_to_clipboard, display_status, display_search_results,
        export_dataframe, get_filter_options, safe_column_filter,
        generate_incident_stamp, validar_informativo_regras,
        validar_informativo_ia, gerar_template_informativo,
        create_dashboard_card, show_error_message, show_success_message,
        inject_responsive_css, interface_busca_loja_operadora_circuito
    )

def test_import_database():
    from src.database import (
        get_connection, get_tables, load_table,
        unified_search_people, search_by_designation, 
        search_by_id_vivo, search_by_address, search_by_ggl_gr,
        get_dashboard_stats
    )

def test_import_editor():
    from src.editor import (
        log_change, get_audit_log, update_lojas_record, 
        update_inventario_record, get_editable_fields_lojas,
        get_editable_fields_inventario
    ) 