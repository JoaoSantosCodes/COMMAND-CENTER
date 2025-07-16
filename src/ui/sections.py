import streamlit as st
import app_modular
from src.database.queries import get_dashboard_stats
from src.ui import (
    interface_busca_loja_operadora_circuito,
    show_cache_management,
    SectionTitle, DashboardCard, AlertMessage, Divider, TableViewer
)

def show_dashboard_section():
    SectionTitle("Dashboard", icon="📊")
    try:
        stats = get_dashboard_stats()
        # Exemplo de cards (substitua por dados reais)
        col1, col2, col3 = st.columns(3)
        with col1:
            DashboardCard("Total de Lojas", str(stats.get('total_lojas', 0)), icon="🏪", color="blue").render()
        with col2:
            DashboardCard("Total de Circuitos", str(stats.get('total_circuitos', 0)), icon="🔗", color="green").render()
        with col3:
            lojas_ativas = stats.get('lojas_por_status', {}).get('ATIVA', 0)
            DashboardCard("Lojas Ativas", str(lojas_ativas), icon="🟢", color="green").render()
    except Exception as e:
        st.error(f"Erro ao carregar estatísticas: {str(e)}")
        # Fallback com dados de exemplo
        col1, col2, col3 = st.columns(3)
        with col1:
            DashboardCard("Total de Lojas", "123", icon="🏪", color="blue").render()
        with col2:
            DashboardCard("Total de Circuitos", "456", icon="🔗", color="green").render()
        with col3:
            DashboardCard("Lojas Ativas", "100", icon="🟢", color="green").render()
    
    Divider()
    AlertMessage("Bem-vindo ao dashboard!", type="success")

def show_unified_search_section():
    SectionTitle("Busca Unificada", icon="🔍")
    app_modular.show_unified_search()
    Divider()

def show_guided_search_section():
    SectionTitle("Busca Loja > Operadora > Circuito", icon="🔎")
    interface_busca_loja_operadora_circuito()
    Divider()

def show_data_editor_section():
    SectionTitle("Edição de Dados", icon="✏️")
    app_modular.show_data_editor()
    Divider()

def show_audit_section():
    SectionTitle("Auditoria", icon="📋")
    app_modular.show_audit()
    Divider()

def show_table_viewer_section():
    SectionTitle("Visualizar Tabelas", icon="📊")
    df = app_modular.show_table_viewer(return_df=True) if hasattr(app_modular.show_table_viewer, 'return_df') else None
    if df is not None:
        TableViewer(df, caption="Tabela de exemplo")
    Divider()

def show_sql_query_section():
    SectionTitle("Consulta SQL Customizada", icon="🔧")
    app_modular.show_sql_query()
    Divider()

def show_help_section():
    SectionTitle("Ajuda", icon="❓")
    app_modular.show_help()
    Divider()

def show_about_section():
    SectionTitle("Sobre", icon="ℹ️")
    app_modular.show_about()
    Divider()

def show_cache_management_section():
    SectionTitle("Gerenciamento de Cache", icon="🗄️")
    show_cache_management()
    Divider() 