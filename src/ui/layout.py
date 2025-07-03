import streamlit as st
import os
import config

def show_sidebar():
    logo_path = "logo.svg"
    with st.sidebar:
        if os.path.exists(logo_path):
            with open(logo_path, "r", encoding="utf-8") as f:
                svg = f.read()
            st.markdown(svg, unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align:center;'>ConsultaVD</h2>", unsafe_allow_html=True)
    st.sidebar.title("ConsultaVD")
    st.sidebar.markdown("<small>Sistema de Consulta e Edição de Dados</small>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Usuário:** `{st.session_state.get('user', 'Desconhecido')}`")
    st.sidebar.markdown(f"**Ambiente:** `{config.get_config('environment', 'debug')}`")
    st.sidebar.markdown(f"**Versão:** `2.0`")
    st.sidebar.markdown("---")

def show_main_menu():
    menu_dashboard = ["📊 Dashboard"]
    menu_busca = ["🔍 Busca Unificada", "🔎 Busca Loja > Operadora > Circuito"]
    menu_edicao = ["✏️ Edição de Dados", "📋 Auditoria", "📊 Visualizar Tabelas", "🔧 Consulta SQL Customizada"]
    menu_cache = ["🗄️ Gerenciamento de Cache"]
    menu_ajuda = ["❓ Ajuda", "ℹ️ Sobre"]
    menu_opcoes = menu_dashboard + ["---"] + menu_busca + ["---"] + menu_edicao + ["---"] + menu_cache + ["---"] + menu_ajuda
    opcoes_sem_separador = [op for op in menu_opcoes if op != "---"]
    opcao = st.sidebar.selectbox(
        "Escolha uma opção:",
        opcoes_sem_separador,
        format_func=lambda x: x
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("<small><i>© 2025 ConsultaVD</i></small>", unsafe_allow_html=True)
    return opcao

def show_footer():
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background: #18181b;
            color: #f4f4f5;
            text-align: center;
            padding: 0.5em 0 0.5em 0;
            font-size: 0.95em;
            border-top: 1px solid #27272a;
            z-index: 9999;
        }
        .footer a { color: #a5b4fc; text-decoration: underline; }
        </style>
        <div class="footer">
            © 2025 ConsultaVD &nbsp;|&nbsp; <a href='mailto:suporte@consultavd.com'>suporte@consultavd.com</a> &nbsp;|&nbsp; Versão 2.0
        </div>
    """, unsafe_allow_html=True)

def layout_base(content_func):
    show_sidebar()
    opcao = show_main_menu()
    content_func(opcao)
    show_footer() 