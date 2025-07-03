"""
Aplicação principal do ConsultaVD usando arquitetura modular
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
from pathlib import Path
import os

# Adicionar src ao path para importar módulos
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

# Importar módulos SEM try/except
from src.database import (
    get_connection, get_tables, load_table,
    unified_search_people, search_by_designation, 
    search_by_id_vivo, search_by_address, search_by_ggl_gr,
    get_dashboard_stats
)
from src.editor import (
    log_change, get_audit_log, update_lojas_record, 
    update_inventario_record, get_editable_fields_lojas,
    get_editable_fields_inventario
)
from src.ui import (
    copy_to_clipboard, display_status, display_search_results,
    export_dataframe, get_filter_options, safe_column_filter,
    generate_incident_stamp, validar_informativo_regras,
    validar_informativo_ia, gerar_template_informativo,
    create_dashboard_card, show_error_message, show_success_message,
    inject_responsive_css, interface_busca_loja_operadora_circuito,
    show_cache_management, show_cache_performance_metrics,
    show_sidebar, show_main_menu, show_footer, layout_base
)
import config

def main_content(opcao):
    # Importar as seções aqui para evitar importação circular
    from src.ui.sections import (
        show_dashboard_section, show_unified_search_section, show_guided_search_section,
        show_data_editor_section, show_audit_section, show_table_viewer_section, show_sql_query_section,
        show_help_section, show_about_section, show_cache_management_section
    )
    
    if opcao == "📊 Dashboard":
        show_dashboard_section()
    elif opcao == "🔍 Busca Unificada":
        show_unified_search_section()
    elif opcao == "🔎 Busca Loja > Operadora > Circuito":
        show_guided_search_section()
    elif opcao == "✏️ Edição de Dados":
        show_data_editor_section()
    elif opcao == "📋 Auditoria":
        show_audit_section()
    elif opcao == "📊 Visualizar Tabelas":
        show_table_viewer_section()
    elif opcao == "🔧 Consulta SQL Customizada":
        show_sql_query_section()
    elif opcao == "🗄️ Gerenciamento de Cache":
        show_cache_management_section()
    elif opcao == "❓ Ajuda":
        show_help_section()
    elif opcao == "ℹ️ Sobre":
        show_about_section()

if __name__ == "__main__":
    st.set_page_config(
        page_title=config.get_config("streamlit", "page_title"),
        page_icon=config.get_config("streamlit", "page_icon"),
        layout=config.get_config("streamlit", "layout"),
        initial_sidebar_state=config.get_config("streamlit", "initial_sidebar_state")
    )
    inject_responsive_css()
    is_valid, errors = config.validate_config()
    if not is_valid:
        st.error("❌ Erros de configuração encontrados:")
        for error in errors:
            st.error(f"- {error}")
        st.stop()
    layout_base(main_content)

def show_dashboard():
    """Exibe o dashboard principal"""
    st.markdown("""
        <style>
        .dashboard-card .stMetric {
            background: #f5f7fa;
            border-radius: 12px;
            padding: 1.2em 0.5em 1.2em 0.5em;
            margin-bottom: 0.5em;
            box-shadow: 0 2px 8px #0001;
        }
        .dashboard-title {
            font-size: 2.2em;
            font-weight: 700;
            margin-bottom: 0.2em;
        }
        .dashboard-breadcrumb {
            color: #888;
            font-size: 1em;
            margin-bottom: 0.5em;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="dashboard-breadcrumb">Início &gt; Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-title">📊 Dashboard - ConsultaVD</div>', unsafe_allow_html=True)
    st.markdown("---")

    try:
        # Obter estatísticas
        stats = get_dashboard_stats()

        # Cards principais
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            create_dashboard_card(
                "Total de Lojas",
                f"{stats['total_lojas']:,}",
                "🏪",
                "blue"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            create_dashboard_card(
                "Total de Circuitos",
                f"{stats['total_circuitos']:,}",
                "🔗",
                "green"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            lojas_ativas = stats['lojas_por_status'].get('ATIVA', 0)
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            create_dashboard_card(
                "Lojas Ativas",
                f"{lojas_ativas:,}",
                "🟢",
                "green"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Lojas por Status")
            if stats['lojas_por_status']:
                df_status = pd.DataFrame(
                    list(stats['lojas_por_status'].items()),
                    columns=['Status', 'Quantidade']
                )
                fig = px.pie(df_status, values='Quantidade', names='Status', 
                           title='Distribuição por Status', hole=0.45)
                fig.update_traces(textinfo='percent+label', pull=[0.05]*len(df_status))
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("📡 Circuitos por Operadora")
            if stats['circuitos_por_operadora']:
                df_operadora = pd.DataFrame(
                    list(stats['circuitos_por_operadora'].items()),
                    columns=['Operadora', 'Quantidade']
                )
                fig = px.bar(df_operadora, x='Operadora', y='Quantidade',
                           title='Circuitos por Operadora', color='Operadora', color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("🗺️ Lojas por UF (Top 10)")
        if stats['lojas_por_uf']:
            df_uf = pd.DataFrame(
                list(stats['lojas_por_uf'].items()),
                columns=['UF', 'Quantidade']
            ).head(10)  # Top 10
            fig = px.bar(df_uf, x='UF', y='Quantidade',
                       title='Top 10 - Lojas por UF', color='UF', color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("⚠️ Alertas e Informações")
        if stats['total_lojas'] > 0:
            taxa_ativas = (stats['lojas_por_status'].get('ATIVA', 0) / stats['total_lojas']) * 100
            if taxa_ativas < 80:
                st.warning(f"⚠️ Taxa de lojas ativas baixa: {taxa_ativas:.1f}%")
            else:
                st.success(f"✅ Taxa de lojas ativas: {taxa_ativas:.1f}%")

        st.markdown("---")
        st.subheader("ℹ️ Informações do Sistema")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Banco de dados:** {config.get_config('database', 'name')}")
            st.info(f"**Ambiente:** {config.get_config('environment', 'debug')}")
        with col2:
            st.info(f"**Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            st.info(f"**Versão:** 2.0 (Modular)")

    except Exception as e:
        show_error_message(f"Erro ao carregar dashboard: {str(e)}")

    show_footer()

def show_unified_search():
    """Exibe a busca unificada"""
    st.markdown("""
        <style>
        .search-tabs .stTabs [data-baseweb="tab"] {
            font-size: 1.1em;
            font-weight: 600;
            padding: 0.7em 1.2em;
        }
        .search-section {
            background: #23272f;
            border-radius: 10px;
            padding: 1.5em 1em 1.5em 1em;
            margin-bottom: 1.2em;
            box-shadow: 0 1px 6px #0001;
        }
        .search-title {
            font-size: 1.5em;
            font-weight: 700;
            margin-bottom: 0.2em;
        }
        .search-desc {
            color: #888;
            font-size: 1em;
            margin-bottom: 1em;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="dashboard-breadcrumb">Início &gt; Busca Unificada</div>', unsafe_allow_html=True)
    st.markdown('<div class="search-title">🔍 Busca Unificada</div>', unsafe_allow_html=True)
    st.markdown('<div class="search-desc">Encontre rapidamente informações por People/PEOP, Designação, ID Vivo, Endereço, GGL/GR ou utilize a busca guiada.</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Abas de busca
    with st.container():
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🔍 People/PEOP", "🔗 Designação", "📱 ID Vivo", 
            "📍 Endereço", "🔎 Busca Loja > Operadora > Circuito", "👥 GGL e GR"
        ])

    with tab1:
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.subheader("🔍 Busca por People/PEOP")
        with st.form(key="form_people_search"):
            people_code = st.text_input("Digite o código People/PEOP:", key="people_search")
            submit_people = st.form_submit_button("🔍 Buscar")
        if submit_people:
            if people_code:
                with st.spinner("Buscando..."):
                    df = unified_search_people(people_code)
                    if df is not None and not df.empty:
                        display_search_results(df, "People/PEOP")
                        export_dataframe(df, "busca_people")
                    else:
                        st.info("Nenhum resultado encontrado para o código informado.")
            else:
                st.warning("Digite um código People/PEOP")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.subheader("🔗 Busca por Designação")
        designation = st.text_input("Digite a designação do circuito:", key="designation_search")
        if st.button("🔍 Buscar", key="btn_designation"):
            if designation:
                with st.spinner("Buscando..."):
                    df = search_by_designation(designation)
                    if df is not None and not df.empty:
                        display_search_results(df, "Designação")
                        export_dataframe(df, "busca_designation")
                    else:
                        st.info("Nenhum resultado encontrado para a designação informada.")
            else:
                st.warning("Digite uma designação")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.subheader("📱 Busca por ID Vivo")
        id_vivo = st.text_input("Digite o ID Vivo:", key="id_vivo_search")
        if st.button("🔍 Buscar", key="btn_id_vivo"):
            if id_vivo:
                with st.spinner("Buscando..."):
                    df = search_by_id_vivo(id_vivo)
                    st.write(df)  # DEBUG: Exibe o DataFrame retornado
                    if df is not None and not df.empty:
                        # Montar listas únicas de designação e loja
                        def get_designacao(row):
                            novo_circ = row.get('Novo_Circuito_Designação', '')
                            circ = row.get('Circuito_Designação', '')
                            return novo_circ if novo_circ and novo_circ != 'N/A' else circ
                        def get_loja(row):
                            people = row.get('People/PEOP', '')
                            vd_novo = row.get('VD_NOVO', '')
                            loja = row.get('LOJAS', '')
                            if vd_novo and vd_novo != 'N/A':
                                return f"{people}/{vd_novo} - {loja}"
                            else:
                                return f"{people} - {loja}"
                        opcoes_designacao = sorted(set([get_designacao(row) for _, row in df.iterrows() if get_designacao(row)]))
                        opcoes_loja = sorted(set([get_loja(row) for _, row in df.iterrows() if get_loja(row)]))
                        # Seletores
                        designacao_sel = st.selectbox("Selecione a Designação:", opcoes_designacao, key="sel_designacao") if opcoes_designacao else None
                        loja_sel = st.selectbox("Selecione a Loja:", opcoes_loja, key="sel_loja") if opcoes_loja else None
                        # Filtrar linha correspondente
                        if designacao_sel and loja_sel:
                            def match_row(row):
                                return get_designacao(row) == designacao_sel and get_loja(row) == loja_sel
                            df_sel = df[df.apply(match_row, axis=1)]
                            if not df_sel.empty:
                                display_search_results(df_sel, "ID Vivo")
                                export_dataframe(df_sel, "busca_id_vivo")
                            else:
                                st.info("Nenhum registro encontrado para a combinação selecionada.")
                        else:
                            st.info("Selecione a Designação e a Loja para visualizar o resultado.")
                    else:
                        st.info("Nenhum resultado encontrado para o ID Vivo informado.")
            else:
                st.warning("Digite um ID Vivo")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.subheader("📍 Busca por Endereço")
        address = st.text_input("Digite endereço, bairro ou cidade:", key="address_search")
        if st.button("🔍 Buscar", key="btn_address"):
            if address:
                with st.spinner("Buscando..."):
                    df = search_by_address(address)
                    if df is not None and not df.empty:
                        display_search_results(df, "Endereço")
                        export_dataframe(df, "busca_endereco")
                    else:
                        st.info("Nenhum resultado encontrado para o endereço informado.")
            else:
                st.warning("Digite um endereço, bairro ou cidade")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.subheader("🔎 Busca Loja > Operadora > Circuito")
        interface_busca_loja_operadora_circuito()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab6:
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.subheader("👥 Busca por GGL e GR")
        ggl_gr = st.text_input("Digite o nome do GGL ou GR:", key="ggl_gr_search")
        if st.button("🔍 Buscar", key="btn_ggl_gr"):
            if ggl_gr:
                with st.spinner("Buscando..."):
                    df = search_by_ggl_gr(ggl_gr)
                    if df is not None and not df.empty:
                        display_search_results(df, "GGL/GR")
                        export_dataframe(df, "busca_ggl_gr")
                    else:
                        st.info("Nenhum resultado encontrado para o nome informado.")
            else:
                st.warning("Digite o nome do GGL ou GR")
        st.markdown('</div>', unsafe_allow_html=True)

    show_footer()

def show_data_editor():
    """Exibe a tela de edição de dados"""
    st.markdown("""
        <style>
        .editor-section {
            background: #f8fafc;
            border-radius: 10px;
            padding: 1.5em 1em 1.5em 1em;
            margin-bottom: 1.2em;
            box-shadow: 0 1px 6px #0001;
        }
        .editor-title {
            font-size: 1.5em;
            font-weight: 700;
            margin-bottom: 0.2em;
        }
        .editor-desc {
            color: #888;
            font-size: 1em;
            margin-bottom: 1em;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="dashboard-breadcrumb">Início &gt; Edição de Dados</div>', unsafe_allow_html=True)
    st.markdown('<div class="editor-title">✏️ Edição de Dados</div>', unsafe_allow_html=True)
    st.markdown('<div class="editor-desc">Edite registros das tabelas principais do sistema. Utilize os filtros para encontrar rapidamente o que deseja alterar.</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="editor-section">', unsafe_allow_html=True)
    # Selecionar tabela
    table = st.selectbox("Selecione a tabela:", ["lojas_lojas", "inventario_planilha1"])
    
    # Selecionar registro
    record_id = st.text_input("Digite o código People/PEOP do registro:")
    
    if st.button("🔍 Carregar Registro"):
        if record_id:
            with st.spinner("Carregando..."):
                # Buscar registro
                if table == "lojas_lojas":
                    df = unified_search_people(record_id)
                else:
                    df = unified_search_people(record_id)
                
                if not df.empty:
                    st.success("✅ Registro encontrado!")
                    
                    # Exibir dados atuais
                    st.subheader("📋 Dados Atuais")
                    st.dataframe(df, use_container_width=True)
                    
                    # Editor de campos
                    st.subheader("✏️ Editar Campos")
                    
                    if table == "lojas_lojas":
                        editable_fields = get_editable_fields_lojas()
                    else:
                        editable_fields = get_editable_fields_inventario()
                    
                    # Criar formulário de edição
                    with st.form("edit_form"):
                        updates = {}
                        
                        for field in editable_fields:
                            current_value = df.iloc[0].get(field, "")
                            new_value = st.text_input(
                                f"**{field}:**",
                                value=str(current_value) if current_value else "",
                                key=f"edit_{field}"
                            )
                            if new_value != str(current_value):
                                updates[field] = new_value
                        
                        submitted = st.form_submit_button("💾 Salvar Alterações")
                        
                        if submitted and updates:
                            with st.spinner("Salvando..."):
                                success_count = 0
                                for field, new_value in updates.items():
                                    if table == "lojas_lojas":
                                        success = update_lojas_record(record_id, field, new_value)
                                    else:
                                        success = update_inventario_record(record_id, field, new_value)
                                    
                                    if success:
                                        success_count += 1
                                
                                if success_count == len(updates):
                                    show_success_message(f"✅ {success_count} campo(s) atualizado(s) com sucesso!")
                                else:
                                    st.warning(f"⚠️ {len(updates) - success_count} campo(s) não puderam ser atualizados")
                else:
                    st.warning("❌ Registro não encontrado")
        else:
            st.warning("Digite um código People/PEOP")
    st.markdown('</div>', unsafe_allow_html=True)

    show_footer()

def show_audit():
    """Exibe a tela de auditoria"""
    st.markdown("""
        <style>
        .audit-section {
            background: #f8fafc;
            border-radius: 10px;
            padding: 1.5em 1em 1.5em 1em;
            margin-bottom: 1.2em;
            box-shadow: 0 1px 6px #0001;
        }
        .audit-title {
            font-size: 1.5em;
            font-weight: 700;
            margin-bottom: 0.2em;
        }
        .audit-desc {
            color: #888;
            font-size: 1em;
            margin-bottom: 1em;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="dashboard-breadcrumb">Início &gt; Auditoria</div>', unsafe_allow_html=True)
    st.markdown('<div class="audit-title">📋 Auditoria</div>', unsafe_allow_html=True)
    st.markdown('<div class="audit-desc">Consulte o histórico de alterações e ações realizadas no sistema. Use filtros para refinar a busca.</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="audit-section">', unsafe_allow_html=True)
    # Obter logs
    logs = get_audit_log(limit=100)
    
    if logs:
        st.subheader(f"📊 Histórico de Alterações ({len(logs)} registros)")
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            tables = list(set(log['table'] for log in logs))
            selected_table = st.selectbox("Filtrar por tabela:", ["Todas"] + tables)
        
        with col2:
            limit = st.slider("Limite de registros:", 10, 100, 50)
        
        # Aplicar filtros
        filtered_logs = logs[-limit:]
        if selected_table != "Todas":
            filtered_logs = [log for log in filtered_logs if log['table'] == selected_table]
        
        # Exibir logs
        for log in reversed(filtered_logs):
            with st.expander(f"📝 {log['field']} - {log['timestamp'][:19]}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Tabela:** {log['table']}")
                    st.write(f"**Registro:** {log['record_id']}")
                    st.write(f"**Campo:** {log['field']}")
                
                with col2:
                    st.write(f"**Valor Anterior:** {log['old_value']}")
                    st.write(f"**Novo Valor:** {log['new_value']}")
                    st.write(f"**Ação:** {log['action']}")
        
        # Estatísticas
        st.subheader("📈 Estatísticas")
        
        # Campos mais modificados
        field_counts = {}
        for log in logs:
            field = log['field']
            field_counts[field] = field_counts.get(field, 0) + 1
        
        if field_counts:
            most_modified = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            st.write("**Campos mais modificados:**")
            for field, count in most_modified:
                st.write(f"- {field}: {count} alterações")
    else:
        st.info("📋 Nenhum registro de auditoria encontrado")
    st.markdown('</div>', unsafe_allow_html=True)

    show_footer()

def show_table_viewer():
    """Exibe o visualizador de tabelas"""
    st.title("📊 Visualizar Tabelas")
    
    # Selecionar tabela
    tables = get_tables()
    selected_table = st.selectbox("Selecione a tabela:", tables)
    
    if selected_table:
        # Configurações de visualização
        col1, col2 = st.columns(2)
        
        with col1:
            limit = st.slider("Limite de registros:", 10, 1000, 100)
        
        with col2:
            if st.button("🔄 Carregar"):
                with st.spinner("Carregando dados..."):
                    df = load_table(selected_table, limit)
                    
                    st.subheader(f"📊 Tabela: {selected_table}")
                    st.write(f"Total de registros carregados: {len(df)}")
                    
                    # Filtros dinâmicos
                    if not df.empty:
                        st.subheader("🔍 Filtros")
                        
                        # Selecionar coluna para filtrar
                        filter_column = st.selectbox("Filtrar por:", df.columns.tolist())
                        
                        if filter_column:
                            # Obter valores únicos
                            unique_values = df[filter_column].dropna().unique().tolist()
                            selected_values = st.multiselect(
                                f"Selecionar valores de {filter_column}:",
                                unique_values
                            )
                            
                            # Aplicar filtro
                            if selected_values:
                                df_filtered = df[df[filter_column].isin(selected_values)]
                                st.write(f"Registros filtrados: {len(df_filtered)}")
                                st.dataframe(df_filtered, use_container_width=True)
                                export_dataframe(df_filtered, f"{selected_table}_filtrado")
                            else:
                                st.dataframe(df, use_container_width=True)
                                export_dataframe(df, selected_table)
                        else:
                            st.dataframe(df, use_container_width=True)
                            export_dataframe(df, selected_table)

def show_sql_query():
    """Exibe a consulta SQL customizada"""
    st.title("🔧 Consulta SQL Customizada")
    
    st.warning("⚠️ **Atenção:** Use apenas consultas SELECT para segurança")
    
    # Editor SQL
    sql_query = st.text_area(
        "Digite sua consulta SQL:",
        height=200,
        placeholder="SELECT * FROM lojas_lojas LIMIT 10"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Executar"):
            if sql_query:
                if sql_query.strip().upper().startswith('SELECT'):
                    try:
                        with st.spinner("Executando consulta..."):
                            from database.connection import execute_query
                            df = execute_query(sql_query)
                            
                            if not df.empty:
                                st.success(f"✅ Consulta executada com sucesso! ({len(df)} registros)")
                                st.dataframe(df, use_container_width=True)
                                export_dataframe(df, "consulta_sql")
                            else:
                                st.info("ℹ️ Consulta executada, mas nenhum resultado encontrado")
                    except Exception as e:
                        show_error_message(f"Erro na consulta: {str(e)}")
                else:
                    st.error("❌ Apenas consultas SELECT são permitidas por segurança")
            else:
                st.warning("Digite uma consulta SQL")
    
    with col2:
        if st.button("📋 Exemplos"):
            st.subheader("📋 Exemplos de Consultas")
            
            examples = [
                ("Contar lojas por status", "SELECT STATUS, COUNT(*) as quantidade FROM lojas_lojas GROUP BY STATUS ORDER BY quantidade DESC"),
                ("Top 10 lojas", "SELECT LOJAS, CIDADE, UF FROM lojas_lojas LIMIT 10"),
                ("Circuitos por operadora", "SELECT Operadora, COUNT(*) as quantidade FROM inventario_planilha1 GROUP BY Operadora"),
                ("Lojas por UF", "SELECT UF, COUNT(*) as quantidade FROM lojas_lojas GROUP BY UF ORDER BY quantidade DESC")
            ]
            
            for title, query in examples:
                with st.expander(title):
                    st.code(query, language="sql")
                    if st.button(f"Usar: {title}", key=f"example_{title}"):
                        st.session_state.sql_query = query

def show_help():
    """Exibe a ajuda"""
    st.title("❓ Ajuda e Documentação")
    
    # Criar abas para diferentes tipos de ajuda
    help_tab1, help_tab2, help_tab3, help_tab4 = st.tabs([
        "🚀 Guia Rápido", "❓ FAQ", "📖 Tutoriais", "🔧 Solução de Problemas"
    ])
    
    with help_tab1:
        st.markdown("### 🚀 Guia Rápido - ConsultaVD")
        
        st.markdown("""
        **Bem-vindo ao ConsultaVD!** Este sistema permite consultar e gerenciar dados de lojas e circuitos.
        
        #### 📋 Principais Funcionalidades:
        
        **1. Dashboard** 📊
        - Visualização rápida de estatísticas
        - Gráficos de distribuição por status, região e UF
        - Alertas de inconsistências nos dados
        
        **2. Busca Unificada** 🔍
        - **People/PEOP**: Busca por código de loja
        - **Designação**: Busca por tipo de circuito (VIVO, CLARO, OI)
        - **ID Vivo**: Busca específica para operadora VIVO
        - **Endereço**: Busca por endereço, bairro ou cidade
        - **Busca Guiada**: Navegação por Loja > Operadora > Circuito
        - **GGL e GR**: Validação de gerentes regionais
        
        **3. Edição de Dados** ✏️
        - Edição direta de registros
        - Validação automática de campos
        - Histórico de alterações
        
        **4. Auditoria** 📋
        - Histórico completo de alterações
        - Filtros por tabela e período
        - Exportação de logs
        
        **5. Exportação** ⬇️
        - Exportar resultados para Excel/CSV
        - Copiar carimbos para chamados
        - Copiar contatos facilmente
        """)
    
    with help_tab2:
        st.markdown("### ❓ Perguntas Frequentes (FAQ)")
        
        with st.expander("Como fazer uma busca por loja?", expanded=False):
            st.markdown("""
            **Resposta:** Use a aba "People/PEOP" na Busca Unificada:
            1. Digite o código da loja (ex: L1854)
            2. Clique em buscar
            3. Selecione o registro desejado
            4. Visualize os detalhes completos
            """)
        
        with st.expander("Como gerar um carimbo para chamado?", expanded=False):
            st.markdown("""
            **Resposta:** Após encontrar um registro:
            1. Selecione o registro na lista
            2. Expanda a seção "🖨️ Carimbo para Chamado"
            3. O carimbo é gerado automaticamente
            4. Clique em "📋 Copiar Carimbo Completo"
            """)
        
        with st.expander("Como editar dados de uma loja?", expanded=False):
            st.markdown("""
            **Resposta:** Use a aba "Edição de Dados":
            1. Selecione a tabela (lojas_lojas ou inventario_planilha1)
            2. Escolha o registro pelo código People/PEOP
            3. Edite os campos desejados
            4. Clique em "Salvar Alterações"
            5. A alteração será registrada no histórico
            """)
    
    with help_tab3:
        st.markdown("### 📖 Tutoriais Detalhados")
        
        st.markdown("#### Tutorial 1: Busca Guiada por Loja")
        st.markdown("""
        1. **Acesse** a aba "🔎 Busca Loja > Operadora > Circuito"
        2. **Digite** o nome ou código da loja no campo de busca
        3. **Selecione** a loja desejada na lista
        4. **Escolha** a operadora (VIVO, CLARO, OI)
        5. **Selecione** o circuito/designação específico
        6. **Visualize** os detalhes completos do circuito
        """)
        
        st.markdown("#### Tutorial 2: Validação de GGL/GR")
        st.markdown("""
        1. **Acesse** a aba "🔍 GGL e GR"
        2. **Digite** o nome do GGL ou GR
        3. **Visualize** o contato (telefone e e-mail)
        4. **Veja** todas as lojas vinculadas ao GGL/GR
        5. **Exporte** a lista se necessário
        """)
    
    with help_tab4:
        st.markdown("### 🔧 Solução de Problemas")
        
        st.markdown("#### Problema: Nenhum resultado encontrado")
        st.markdown("""
        **Possíveis causas:**
        - Código digitado incorretamente
        - Loja não cadastrada no sistema
        - Dados desatualizados
        
        **Soluções:**
        1. Verifique a grafia do código
        2. Tente buscar por parte do nome da loja
        3. Use a busca por endereço
        4. Consulte o administrador do sistema
        """)
        
        st.markdown("#### Problema: Erro ao editar dados")
        st.markdown("""
        **Possíveis causas:**
        - Campo obrigatório vazio
        - Formato de dados incorreto
        - Problema de conexão com banco
        
        **Soluções:**
        1. Preencha todos os campos obrigatórios
        2. Verifique o formato dos dados
        3. Recarregue a página
        4. Tente novamente em alguns minutos
        """)

    show_footer()

def show_about():
    """Exibe informações sobre o sistema"""
    st.title("ℹ️ Sobre o Sistema")
    
    st.markdown("""
    ### Sistema de Consulta e Edição VD - Versão 2.0 (Modular)
    
    **Funcionalidades:**
    - 🔎 **Busca Unificada**: Pesquisa por código People/PEOP, designação, ID Vivo e endereço
    - ✏️ **Edição de Dados**: Edição inline com salvamento automático
    - 📊 **Visualização**: Visualização completa das tabelas
    - 📋 **Auditoria**: Sistema completo de logs de alterações
    - 🔧 **Consulta SQL**: Execução de queries personalizadas
    - 📈 **Dashboard**: Estatísticas e gráficos em tempo real
    
    **Tabelas Disponíveis:**
    - `inventario_planilha1`: Dados do inventário
    - `lojas_lojas`: Dados das lojas
    
    **Arquitetura:**
    - **Modular**: Código organizado em componentes reutilizáveis
    - **Configurável**: Sistema de configuração centralizado
    - **Auditável**: Log completo de todas as alterações
    - **Responsivo**: Interface adaptável a diferentes dispositivos
    
    **Desenvolvido para:** Sistema de consulta e manutenção de dados VD
    
    **Versão:** 2.0 (Modular)
    **Data:** Dezembro 2024
    """)

    show_footer()

def show_cache_management():
    """Exibe interface de gerenciamento do cache"""
    st.markdown("""
        <style>
        .cache-section {
            background: #f8fafc;
            border-radius: 10px;
            padding: 1.5em 1em 1.5em 1em;
            margin-bottom: 1.2em;
            box-shadow: 0 1px 6px #0001;
        }
        .cache-title {
            font-size: 1.5em;
            font-weight: 700;
            margin-bottom: 0.2em;
        }
        .cache-desc {
            color: #888;
            font-size: 1em;
            margin-bottom: 1em;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="dashboard-breadcrumb">Início &gt; Gerenciamento de Cache</div>', unsafe_allow_html=True)
    st.markdown('<div class="cache-title">🗄️ Gerenciamento de Cache</div>', unsafe_allow_html=True)
    st.markdown('<div class="cache-desc">Visualize estatísticas, limpe ou desabilite o cache para garantir performance e integridade dos dados.</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="cache-section">', unsafe_allow_html=True)
    from src.ui.cache_management import show_cache_management as show_cache_ui
    show_cache_ui()
    st.markdown('</div>', unsafe_allow_html=True)

    show_footer() 