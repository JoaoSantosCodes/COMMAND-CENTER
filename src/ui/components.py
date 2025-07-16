"""
Módulo de componentes de interface reutilizáveis
"""
import streamlit as st
import pandas as pd
import io
from typing import Optional, List, Any
from src.ui.stamps import generate_incident_stamp
from src.database.connection import execute_query

def copy_to_clipboard(text: str, label: str = "Copiar", unique_id: str = "") -> None:
    """
    Cria um botão para copiar texto para a área de transferência
    
    Args:
        text (str): Texto a ser copiado
        label (str): Label do botão
        unique_id (str): ID único para o componente
    """
    if text:
        st.code(text, language=None)
        if st.button(f"📋 {label}", key=f"copy_{unique_id}", type="secondary"):
            st.write("✅ Copiado para a área de transferência!")

def status_badge(status: str) -> str:
    """
    Retorna HTML de badge colorida para status
    """
    status = status.upper()
    color_map = {
        'ATIVA':   ('#22c55e', '#14532d'),   # verde
        'INATIVA': ('#ef4444', '#7f1d1d'),   # vermelho
        'A INAUGURAR': ('#eab308', '#78350f'), # amarelo
        'EM MANUTENÇÃO': ('#0ea5e9', '#0c4a6e'), # azul
        'SUSPENSA': ('#a21caf', '#581c87'),  # roxo
    }
    bg, fg = color_map.get(status, ('#6b7280', '#111827'))
    return f"""
    <span style='display:inline-block; padding:0.25em 0.8em; border-radius:1em; background:{bg}; color:{fg}; font-weight:600; font-size:1em;'>
        {status.title()}
    </span>
    """

def display_status(status: str) -> str:
    """
    Retorna badge colorida e emoji para status
    """
    status_icons = {
        'ATIVA': '🟢',
        'INATIVA': '🔴',
        'A INAUGURAR': '🟡',
        'EM MANUTENÇÃO': '🔧',
        'SUSPENSA': '⏸️'
    }
    icon = status_icons.get(status, '⚪')
    return f"{icon} " + status_badge(status)

def display_search_results(df: pd.DataFrame, search_context: str = None, 
                          circuito_selecionado: str = None) -> None:
    """
    Exibe resultados de busca de forma formatada
    
    Args:
        df (pd.DataFrame): DataFrame com resultados
        search_context (str, optional): Contexto da busca
        circuito_selecionado (str, optional): Circuito selecionado
    """
    def safe_val(val):
        if pd.isna(val) or val is None:
            return "N/A"
        return str(val)
    
    def generate_people_carimbo(row):
        from datetime import datetime
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        people = safe_val(row.get('People/PEOP', ''))
        vd_novo = safe_val(row.get('VD_NOVO', ''))
        codigo = f"{people}/{vd_novo}" if vd_novo and vd_novo != 'N/A' else people
        loja = safe_val(row.get('LOJAS', ''))
        endereco = safe_val(row.get('ENDEREÇO', ''))
        bairro = safe_val(row.get('BAIRRO', ''))
        cidade = safe_val(row.get('CIDADE', ''))
        uf = safe_val(row.get('UF', ''))
        cep = safe_val(row.get('CEP', ''))
        status = safe_val(row.get('Status_Loja', ''))
        segsex = safe_val(row.get('2ª_a_6ª', ''))
        sab = safe_val(row.get('SAB', ''))
        dom = safe_val(row.get('DOM', ''))
        func = safe_val(row.get('FUNC.', ''))
        return f"""**CARIMBO - CONSULTA VD**\nData/Hora: {data_hora}\nPeople/PEOP: {codigo}\nLoja: {loja}\nEndereço: {endereco}\nBAIRRO:{bairro} \nCIDADE:{cidade}\nUF:{uf}\nCEP: {cep}\nStatus: {status}\n2ª a 6ª: {segsex}\nSAB: {sab}\nDOM: {dom}\nFUNC: {func}"""

    def generate_designacao_carimbo(row):
        from datetime import datetime
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        people = safe_val(row.get('People/PEOP', ''))
        vd_novo = safe_val(row.get('VD_NOVO', ''))
        codigo = f"{people}/{vd_novo}" if vd_novo and vd_novo != 'N/A' else people
        loja = safe_val(row.get('LOJAS', ''))
        endereco = safe_val(row.get('ENDEREÇO', ''))
        bairro = safe_val(row.get('BAIRRO', ''))
        cidade = safe_val(row.get('CIDADE', ''))
        uf = safe_val(row.get('UF', ''))
        cep = safe_val(row.get('CEP', ''))
        status = safe_val(row.get('Status_Loja', ''))
        segsex = safe_val(row.get('2ª_a_6ª', ''))
        sab = safe_val(row.get('SAB', ''))
        dom = safe_val(row.get('DOM', ''))
        func = safe_val(row.get('FUNC.', ''))
        circuito = safe_val(row.get('Circuito_Designação', ''))
        novo_circuito = safe_val(row.get('Novo_Circuito_Designação', ''))
        circuito_final = novo_circuito if novo_circuito and novo_circuito != 'N/A' else circuito
        if not circuito_final or circuito_final == 'N/A':
            circuito_final = circuito
        return f"**CARIMBO - CONSULTA VD**\nData/Hora: {data_hora}\nPeople/PEOP: {codigo}\nLoja: {loja}\nEndereço: {endereco}\nBAIRRO:{bairro} \nCIDADE:{cidade}\nUF:{uf}\nCEP: {cep}\nStatus: {status}\n2ª a 6ª: {segsex}\nSAB: {sab}\nDOM: {dom}\nFUNC: {func}\nCircuito: {circuito_final}"

    def generate_idvivo_carimbo(row):
        from datetime import datetime
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        # 1. De-para ID VIVO / Novo ID VIVO
        id_vivo = safe_val(row.get('ID_VIVO', ''))
        novo_id_vivo = safe_val(row.get('Novo_ID_VIVO', ''))
        id_vivo_final = novo_id_vivo if novo_id_vivo and novo_id_vivo != 'N/A' else id_vivo
        
        # 2. De-para People/PEOP / VD NOVO - lógica: People/PEOP/VD NOVO
        people_peop = safe_val(row.get('People/PEOP', ''))
        vd_novo = safe_val(row.get('VD_NOVO', ''))
        if vd_novo and vd_novo != 'N/A':
            codigo = f"{people_peop}/{vd_novo}"
        else:
            codigo = people_peop
        
        # 3. De-para Circuito Designação / Novo Circuito Designação
        circuito = safe_val(row.get('Circuito_Designação', ''))
        novo_circuito = safe_val(row.get('Novo_Circuito_Designação', ''))
        if novo_circuito and novo_circuito != 'N/A':
            designacao = novo_circuito
        elif circuito and circuito != 'N/A':
            designacao = circuito
        else:
            designacao = 'N/A'
        
        # Dados da loja
        loja = safe_val(row.get('LOJAS', ''))
        endereco = safe_val(row.get('ENDEREÇO', ''))
        bairro = safe_val(row.get('BAIRRO', ''))
        cidade = safe_val(row.get('CIDADE', ''))
        uf = safe_val(row.get('UF', ''))
        cep = safe_val(row.get('CEP', ''))
        status = safe_val(row.get('Status_Loja', ''))
        segsex = safe_val(row.get('2ª_a_6ª', ''))
        sab = safe_val(row.get('SAB', ''))
        dom = safe_val(row.get('DOM', ''))
        func = safe_val(row.get('FUNC.', ''))
        
        return f"**CARIMBO - CONSULTA VD**\nData/Hora: {data_hora}\nPeople/PEOP: {codigo}\nLoja: {loja}\nEndereço: {endereco}\nBAIRRO:{bairro} \nCIDADE:{cidade}\nUF:{uf}\nCEP: {cep}\nStatus: {status}\n2ª a 6ª: {segsex}\nSAB: {sab}\nDOM: {dom}\nFUNC: {func}\nID VIVO: {id_vivo_final}\nDesignação: {designacao}"

    if df.empty:
        st.warning("❌ Nenhum resultado encontrado.")
        return
    
    st.success(f"✅ Encontrados {len(df)} resultado(s)")
    
    # Exibir resultados
    for idx, row in df.iterrows():
        with st.expander(f"🏪 {safe_val(row.get('LOJAS', 'Loja'))} - {safe_val(row.get('People/PEOP', 'N/A'))}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Informações Básicas:**")
                st.write(f"**Código:** {safe_val(row.get('People/PEOP', 'N/A'))}")
                st.markdown(f"**Status:** {display_status(safe_val(row.get('Status_Loja', 'N/A')))}", unsafe_allow_html=True)
                st.write(f"**Cidade:** {safe_val(row.get('CIDADE', 'N/A'))} - {safe_val(row.get('UF', 'N/A'))}")
                
                if 'Circuito_Designação' in row:
                    st.write(f"**Circuito:** {safe_val(row.get('Circuito_Designação', 'N/A'))}")
                if 'Operadora' in row:
                    st.write(f"**Operadora:** {safe_val(row.get('Operadora', 'N/A'))}")
            
            with col2:
                st.markdown("**📍 Endereço:**")
                st.write(f"**Endereço:** {safe_val(row.get('ENDEREÇO', 'N/A'))}")
                st.write(f"**Bairro:** {safe_val(row.get('BAIRRO', 'N/A'))}")
                st.write(f"**CEP:** {safe_val(row.get('CEP', 'N/A'))}")
                
                st.markdown("**📞 Contatos:**")
                st.write(f"**Telefone 1:** {safe_val(row.get('TELEFONE1', 'N/A'))}")
                st.write(f"**Telefone 2:** {safe_val(row.get('TELEFONE2', 'N/A'))}")
                st.write(f"**Celular:** {safe_val(row.get('CELULAR', 'N/A'))}")
                st.write(f"**E-mail:** {safe_val(row.get('E_MAIL', 'N/A'))}")
            
            # Horários de funcionamento
            st.markdown("**🕒 Horários de Funcionamento:**")
            col_h1, col_h2, col_h3 = st.columns(3)
            with col_h1:
                st.write(f"**Seg-Sex:** {safe_val(row.get('2ª_a_6ª', 'N/A'))}")
            with col_h2:
                st.write(f"**Sábado:** {safe_val(row.get('SAB', 'N/A'))}")
            with col_h3:
                st.write(f"**Domingo:** {safe_val(row.get('DOM', 'N/A'))}")
            
            # GGL e GR
            st.markdown("**👥 Responsáveis:**")
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.write(f"**GGL:** {safe_val(row.get('NOME_GGL', 'N/A'))}")
            with col_g2:
                st.write(f"**GR:** {safe_val(row.get('NOME_GR', 'N/A'))}")
            
            # Carimbo para chamado
            st.markdown("---")
            st.markdown("**🖨️ Carimbo para Chamado:**")
            
            # Carimbo customizado para aba People/PEOP, Designação e ID VIVO
            if search_context == "People/PEOP":
                carimbo = generate_people_carimbo(row)
            elif search_context == "Designação":
                carimbo = generate_designacao_carimbo(row)
            elif search_context == "ID Vivo":
                carimbo = generate_idvivo_carimbo(row)
            else:
                sintoma = f"Loja: {safe_val(row.get('LOJAS', 'N/A'))} - {safe_val(row.get('People/PEOP', 'N/A'))}"
                abrangencia = f"{safe_val(row.get('CIDADE', 'N/A'))} - {safe_val(row.get('UF', 'N/A'))}"
                impacto = "Loja"
                descricao_impacto = f"Loja {safe_val(row.get('LOJAS', 'N/A'))} localizada em {safe_val(row.get('ENDEREÇO', 'N/A'))}, {safe_val(row.get('BAIRRO', 'N/A'))}, {safe_val(row.get('CIDADE', 'N/A'))} - {safe_val(row.get('UF', 'N/A'))}"
                horario_inicio = "00:00"
                horario_termino = "23:59"
                status = safe_val(row.get('Status_Loja', 'N/A'))
                carimbo = generate_incident_stamp(
                    sintoma, abrangencia, impacto, descricao_impacto,
                    horario_inicio, horario_termino, status
                )
            unique_key = f"{idx}_{safe_val(row.get('People/PEOP', ''))}"
            copy_to_clipboard(carimbo, "Copiar Carimbo Completo", f"stamp_{unique_key}")
            
            # Contatos para cópia rápida
            st.markdown("**📞 Contatos para Cópia Rápida:**")
            contatos = f"Telefone 1: {safe_val(row.get('TELEFONE1', 'N/A'))}\nTelefone 2: {safe_val(row.get('TELEFONE2', 'N/A'))}\nCelular: {safe_val(row.get('CELULAR', 'N/A'))}\nE-mail: {safe_val(row.get('E_MAIL', 'N/A'))}"
            copy_to_clipboard(contatos, "Copiar Contatos", f"contacts_{unique_key}")

def export_dataframe(df: pd.DataFrame, filename_prefix: str = "resultado") -> None:
    """
    Cria botões de exportação para DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame a ser exportado
        filename_prefix (str): Prefixo do nome do arquivo
    """
    if df.empty:
        return
    
    st.markdown("**⬇️ Exportar Resultados:**")
    col1, col2 = st.columns(2)
    
    with col1:
        # Exportar para Excel
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Resultados', index=False)
        excel_data = excel_buffer.getvalue()
        
        st.download_button(
            label="📊 Exportar para Excel",
            data=excel_data,
            file_name=f"{filename_prefix}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col2:
        # Exportar para CSV
        csv = df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="📄 Exportar para CSV",
            data=csv,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv"
        )

def get_filter_options(table: str, column: str) -> List[str]:
    """
    Obtém opções únicas para filtro de coluna
    """
    try:
        query = f"SELECT DISTINCT `{column}` FROM {table} WHERE `{column}` IS NOT NULL ORDER BY `{column}`"
        df = execute_query(query)
        return df[column].tolist()
    except Exception:
        return []

def safe_column_filter(df: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    """
    Aplica filtro seguro em coluna do DataFrame
    """
    if not values:
        return df
    try:
        return df[df[column].isin(values)]
    except Exception:
        return df

def create_dashboard_card(title: str, value: Any, icon: str = "📊", 
                         color: str = "blue", help_text: str = None) -> None:
    """
    Cria um card de dashboard
    """
    st.markdown(f"""
    <div style="
        background-color: {color}20;
        border: 1px solid {color}40;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">{icon}</div>
        <div style="font-size: 1.5em; font-weight: bold; color: {color}; margin-bottom: 5px;">
            {value}
        </div>
        <div style="font-size: 1em; color: #666;">{title}</div>
        {f'<div style="font-size: 0.8em; color: #888; margin-top: 5px;">{help_text}</div>' if help_text else ''}
    </div>
    """, unsafe_allow_html=True)

def create_progress_bar(current: int, total: int, label: str = "Progresso") -> None:
    """
    Cria uma barra de progresso
    """
    if total > 0:
        progress = current / total
        st.progress(progress)
        st.caption(f"{label}: {current}/{total} ({progress:.1%})")

def show_error_message(error: str, title: str = "❌ Erro") -> None:
    """
    Exibe mensagem de erro formatada
    """
    st.error(f"**{title}**\n\n{error}")

def show_success_message(message: str, title: str = "✅ Sucesso") -> None:
    """
    Exibe mensagem de sucesso formatada
    """
    st.success(f"**{title}**\n\n{message}")

def show_info_message(message: str, title: str = "ℹ️ Informação") -> None:
    """
    Exibe mensagem informativa formatada
    """
    st.info(f"**{title}**\n\n{message}")

# Componente de Card para Dashboard
class DashboardCard:
    def __init__(self, title, value, icon=None, color="blue"):
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color

    def render(self):
        color_map = {
            "blue": "#3b82f6",
            "green": "#22c55e",
            "red": "#ef4444",
            "yellow": "#eab308",
            "gray": "#64748b"
        }
        icon_html = f"<span style='font-size:1.5em;'>{self.icon}</span>" if self.icon else ""
        st.markdown(f"""
        <div style='background:{color_map.get(self.color, '#3b82f6')};padding:1.2em 0.5em 1.2em 0.5em;border-radius:12px;margin-bottom:0.5em;box-shadow:0 2px 8px #0001;text-align:center;'>
            <div style='font-size:2em;font-weight:700;'>{icon_html} {self.value}</div>
            <div style='font-size:1.1em;color:#f4f4f5;font-weight:500;margin-top:0.2em;'>{self.title}</div>
        </div>
        """, unsafe_allow_html=True)

# Componente de Alerta Customizado
def AlertMessage(message, type="info"):
    color = {
        "info": "#2563eb",
        "success": "#22c55e",
        "warning": "#eab308",
        "error": "#ef4444"
    }.get(type, "#2563eb")
    st.markdown(f"""
    <div style='background:{color};color:#fff;padding:0.8em 1em;border-radius:8px;margin:0.5em 0;font-weight:500;'>
        {message}
    </div>
    """, unsafe_allow_html=True)

# Componente de Título de Seção
def SectionTitle(title, icon=None):
    icon_html = f"<span style='font-size:1.2em;margin-right:0.3em;'>{icon}</span>" if icon else ""
    st.markdown(f"<h2 style='margin-top:1em;margin-bottom:0.5em;'>{icon_html}{title}</h2>", unsafe_allow_html=True)

# Componente de Divisor
def Divider():
    st.markdown("<hr style='border:1px solid #e5e7eb;margin:1.5em 0;' />", unsafe_allow_html=True)

# Componente de Visualização de Tabela
def TableViewer(df, caption=None):
    if caption:
        st.caption(caption)
    st.dataframe(df, use_container_width=True)