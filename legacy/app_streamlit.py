import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# PRIMEIRO comando visual: set_page_config
st.set_page_config(
    page_title="Consulta VD - Sistema de Consulta e Edição",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado - agora pode vir aqui
st.markdown('''
<link href="https://fonts.googleapis.com/css?family=Nunito:400,700,900&display=swap" rel="stylesheet">
<style>
h1, .stTitle, .stMarkdown h1 {
    font-family: 'Nunito Black', 'Nunito', sans-serif !important;
    font-size: 30pt !important;
    font-weight: 900 !important;
    color: #222;
}
h2, .stMarkdown h2 {
    font-family: 'Nunito', sans-serif !important;
    font-size: 20pt !important;
    font-weight: 700 !important;
    color: #222;
}
.stMarkdown h3, h3 {
    font-family: 'Nunito', sans-serif !important;
    font-size: 18pt !important;
    font-weight: 700 !important;
    color: #222;
}
body, .stApp, .stTextInput input, .stButton button {
    font-family: 'Nunito', sans-serif !important;
}
.stMarkdown, .stTextInput label, .stTextInput input, .stButton button {
    font-size: 13pt !important;
}
[data-testid="column"] > div {
    background: #f8fafc;
    border-radius: 12px;
    box-shadow: 0 2px 8px #0001;
    padding: 24px 18px 18px 18px;
    margin-bottom: 16px;
    border: 1.5px solid #e5e7eb;
}
.card1-vd { background: #222; color: #fff; }
.card2-vd { background: #ef4444; color: #fff; }
.card3-vd { background: #60a5fa; color: #222; }
.card4-vd { background: #38bdf8; color: #222; }
.card5-vd { background: #f9a8d4; color: #222; }
.card6-vd { background: #fde68a; color: #222; }
.stButton button {
    background: #222 !important;
    color: #fff !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 8px 24px !important;
    font-size: 15pt !important;
    margin-top: 8px;
}
.stButton button:hover {
    background: #ef4444 !important;
    color: #fff !important;
}
.stTextInput input {
    background: #fff !important;
    border: 1.5px solid #60a5fa !important;
    border-radius: 6px !important;
    padding: 6px 10px !important;
    font-size: 13pt !important;
    color: #222 !important;
}
.stTextInput label {
    font-weight: 700 !important;
    color: #222 !important;
}
</style>
''', unsafe_allow_html=True)

# Configuração da página
st.title("ConsultaVD - Visualização de Dados")

DB_PATH = "consulta_vd.db"

# Função para conectar ao banco
def get_connection():
    return sqlite3.connect(DB_PATH)

# Listar tabelas disponíveis
def get_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

# Carregar dados de uma tabela
def load_table(table, limit=1000):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT {limit}", conn)
    conn.close()
    return df

# Pesquisa unificada por People/PEOP
def unified_search_people(people_code):
    conn = get_connection()
    query = f'''
    SELECT
        i.People as "People/PEOP",
        i.Status_Loja,
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
    FROM inventario_planilha1 i
    LEFT JOIN lojas_lojas l ON i.People = l.PEOP
    WHERE i.People = ?
    UNION
    SELECT
        l.PEOP as "People/PEOP",
        NULL as Status_Loja,
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
    return df

# Funções para edição e salvamento
def update_lojas_record(peop_code, field, new_value):
    """Atualiza um campo na tabela lojas_lojas"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Escapar o nome da coluna se necessário
        if field in ['ENDEREÇO', 'E_MAIL', '2ª_a_6ª', 'FUNC.']:
            field_escaped = f'"{field}"'
        else:
            field_escaped = field
        
        query = f"UPDATE lojas_lojas SET {field_escaped} = ? WHERE PEOP = ?"
        cursor.execute(query, (new_value, peop_code))
        conn.commit()
        conn.close()
        return True, "Campo atualizado com sucesso!"
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Erro ao atualizar: {str(e)}"

def update_inventario_record(people_code, field, new_value):
    """Atualiza um campo na tabela inventario_planilha1"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Escapar o nome da coluna se necessário
        if field in ['Circuito_Designação', 'Novo_Circuito_Designação']:
            field_escaped = f'"{field}"'
        else:
            field_escaped = field
        
        query = f"UPDATE inventario_planilha1 SET {field_escaped} = ? WHERE People = ?"
        cursor.execute(query, (new_value, people_code))
        conn.commit()
        conn.close()
        return True, "Campo atualizado com sucesso!"
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Erro ao atualizar: {str(e)}"

def get_editable_fields_lojas():
    """Retorna campos editáveis da tabela lojas_lojas"""
    return [
        'LOJAS', 'ENDEREÇO', 'BAIRRO', 'CIDADE', 'UF', 'CEP',
        'TELEFONE1', 'TELEFONE2', 'CELULAR', 'E_MAIL', '2ª_a_6ª',
        'SAB', 'DOM', 'FUNC.', 'VD_NOVO', 'NOME_GGL', 'NOME_GR'
    ]

def get_editable_fields_inventario():
    """Retorna campos editáveis da tabela inventario_planilha1"""
    return [
        'Status_Loja', 'Operadora', 'ID_VIVO', 'Novo_ID_Vivo',
        'Circuito_Designação', 'Novo_Circuito_Designação'
    ]

# Consulta SQL customizada
def run_custom_query(query):
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        conn.close()
        return None, str(e)

# Sidebar
st.sidebar.header("Navegação")
opcao = st.sidebar.radio("Escolha uma opção:", ["Busca Unificada People/PEOP", "Edição de Dados", "Visualizar Tabelas", "Consulta SQL Customizada", "Sobre"])

if 'people_code' not in st.session_state:
    st.session_state['people_code'] = ''
if 'operadora_sel' not in st.session_state:
    st.session_state['operadora_sel'] = ''
if 'edit_mode' not in st.session_state:
    st.session_state['edit_mode'] = False

if opcao == "Busca Unificada People/PEOP":
    st.subheader("🔎 Pesquisa Unificada por People/PEOP")
    st.info("Digite o código People/PEOP para buscar informações unificadas das duas tabelas.")
    
    with st.form(key="form_busca_people"):
        people_code = st.text_input("Código People/PEOP:", value=st.session_state['people_code'], placeholder="Ex: 12345")
        submit = st.form_submit_button("Buscar")
    
    if submit and people_code:
        st.session_state['people_code'] = people_code
        st.session_state['operadora_sel'] = ''  # Limpa operadora ao buscar novo código

    people_code = st.session_state['people_code']
    if people_code:
        df_unificado = unified_search_people(people_code)
        if not df_unificado.empty:
            st.success(f"{len(df_unificado)} registro(s) encontrado(s) para o código {people_code}")
            
            # Botão para alternar modo de edição
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("✏️ Modo Edição" if not st.session_state['edit_mode'] else "👁️ Modo Visualização"):
                    st.session_state['edit_mode'] = not st.session_state['edit_mode']
                    st.rerun()
            
            with col2:
                if st.session_state['edit_mode']:
                    st.info("🔧 **Modo Edição Ativo** - Clique nos campos para editar e salvar automaticamente")
                else:
                    st.info("👁️ **Modo Visualização** - Clique em 'Modo Edição' para editar campos")
            
            st.dataframe(df_unificado, use_container_width=True)

            row = df_unificado.iloc[0]
            def get_val(col):
                return row[col] if col in row and pd.notnull(row[col]) else "Não encontrado"

            horario = get_val('2ª_a_6ª')
            if isinstance(horario, str):
                horario_fmt = horario.upper().replace('AS', 'ÀS').replace('AS', 'ÀS')
            else:
                horario_fmt = horario

            # --- Filtro de Operadora e Detalhes do Inventário ---
            conn = get_connection()
            df_inv = pd.read_sql_query(
                "SELECT Operadora, ID_VIVO, Novo_ID_Vivo, Circuito_Designação, Novo_Circuito_Designação FROM inventario_planilha1 WHERE People = ?",
                conn, params=(people_code,)
            )
            conn.close()
            operadoras = df_inv['Operadora'].dropna().unique().tolist() if not df_inv.empty else []
            op_row = None
            if operadoras:
                st.markdown("---")
                st.markdown("#### Filtrar por Operadora (Inventário)")
                if st.session_state['operadora_sel'] not in operadoras:
                    st.session_state['operadora_sel'] = operadoras[0]
                operadora_sel = st.selectbox("Selecione a Operadora:", operadoras, index=operadoras.index(st.session_state['operadora_sel']) if st.session_state['operadora_sel'] in operadoras else 0, key="operadora_selectbox")
                st.session_state['operadora_sel'] = operadora_sel
                df_op = df_inv[df_inv['Operadora'] == operadora_sel]
                st.markdown(f"**Detalhes para Operadora: {operadora_sel}**")
                st.dataframe(df_op, use_container_width=True)
                if not df_op.empty:
                    op_row = df_op.iloc[0]
            else:
                st.info("Nenhuma operadora encontrada para esse People/PEOP no inventário.")

            # Função para pegar do inventário se disponível, senão do unificado
            def get_val_op(col, fallback_col=None):
                if op_row is not None and col in op_row and pd.notnull(op_row[col]):
                    return op_row[col]
                if fallback_col and fallback_col in row and pd.notnull(row[fallback_col]):
                    return row[fallback_col]
                if col in row and pd.notnull(row[col]):
                    return row[col]
                return "Não encontrado"

            # Carimbo visual com contraste melhorado
            carimbo_html = f'''
            <div style="border:2px solid #444;padding:0;margin:24px 0 8px 0;max-width:600px;font-family:sans-serif;">
                <div style="background:#222;color:#fff;font-weight:bold;text-align:center;padding:6px 0;">CARIMBO DE ABERTURA DE CHAMADO POR E-MAIL</div>
                <table style="width:100%;border-collapse:collapse;font-size:15px;">
                    <tr>
                        <td style="background:#dbeafe;font-weight:bold;padding:4px 8px;width:120px;color:#222;">VD</td>
                        <td style="background:#f1f5f9;padding:4px 8px;color:#222;">{get_val('People/PEOP')}</td>
                    </tr>
                    <tr>
                        <td style="background:#67e8f9;font-weight:bold;padding:4px 8px;color:#222;">OPERADORA</td>
                        <td style="background:#fff;padding:4px 8px;color:#222;">{get_val_op('Operadora')}</td>
                    </tr>
                    <tr>
                        <td style="background:#67e8f9;font-weight:bold;padding:4px 8px;color:#222;">DESIGNAÇÃO</td>
                        <td style="background:#fff;padding:4px 8px;color:#222;">{get_val_op('Circuito_Designação')}</td>
                    </tr>
                    <tr>
                        <td style="background:#67e8f9;font-weight:bold;padding:4px 8px;color:#222;">ID VANTIVE</td>
                        <td style="background:#fff;padding:4px 8px;color:#222;">{get_val_op('ID_VIVO')}</td>
                    </tr>
                    <tr>
                        <td style="background:#67e8f9;font-weight:bold;padding:4px 8px;color:#222;">NOVO ID VIVO</td>
                        <td style="background:#fff;padding:4px 8px;color:#222;">{get_val_op('Novo_ID_Vivo')}</td>
                    </tr>
                    <tr>
                        <td style="background:#67e8f9;font-weight:bold;padding:4px 8px;color:#222;">NOVO CIRCUITO/DESIGNAÇÃO</td>
                        <td style="background:#fff;padding:4px 8px;color:#222;">{get_val_op('Novo_Circuito_Designação')}</td>
                    </tr>
                    <tr>
                        <td style="background:#67e8f9;font-weight:bold;padding:4px 8px;color:#222;">ENDEREÇO</td>
                        <td style="background:#fff;padding:4px 8px;color:#222;">{get_val('ENDEREÇO')}</td>
                    </tr>
                    <tr>
                        <td style="background:#67e8f9;font-weight:bold;padding:4px 8px;color:#222;">CIDADE</td>
                        <td style="background:#fff;padding:4px 8px;color:#222;">{get_val('CIDADE')}</td>
                    </tr>
                    <tr>
                        <td style="background:#67e8f9;font-weight:bold;padding:4px 8px;color:#222;">FILIAL</td>
                        <td style="background:#fff;padding:4px 8px;color:#222;">{get_val('LOJAS')}</td>
                    </tr>
                    <tr>
                        <td style="background:#fde68a;font-weight:bold;padding:4px 8px;color:#222;">HORARIO DE FUNCIONAMENTO</td>
                        <td style="background:#fffde7;padding:4px 8px;color:#222;">{horario_fmt}</td>
                    </tr>
                    <tr>
                        <td colspan="2" style="background:#ef4444;color:#fff;font-weight:bold;text-align:center;padding:6px 0;">
                            CONTATO COMMAND CENTER<br>
                            Telefone: (11) 3274-7527<br>
                            E-mail: central.comando@dpsp.com.br
                        </td>
                    </tr>
                </table>
            </div>
            <div style="background:#f1f5f9;padding:8px 12px;margin-bottom:16px;font-size:14px;color:#222;">
                <b>MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS</b><br>
                LOJA VD {get_val('People/PEOP')} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: {horario_fmt} | SAB 24 HORAS | DOM 24 HORAS
            </div>
            '''
            st.markdown(carimbo_html, unsafe_allow_html=True)

            # Carimbo em texto puro para copiar
            carimbo_txt = f'''
CARIMBO DE ABERTURA DE CHAMADO POR E-MAIL

VD: {get_val('People/PEOP')}
OPERADORA: {get_val_op('Operadora')}
DESIGNAÇÃO: {get_val_op('Circuito_Designação')}
ID VANTIVE: {get_val_op('ID_VIVO')}
NOVO ID VIVO: {get_val_op('Novo_ID_Vivo')}
NOVO CIRCUITO/DESIGNAÇÃO: {get_val_op('Novo_Circuito_Designação')}
ENDEREÇO: {get_val('ENDEREÇO')}
CIDADE: {get_val('CIDADE')}
FILIAL: {get_val('LOJAS')}
HORARIO DE FUNCIONAMENTO: {horario_fmt}

CONTATO COMMAND CENTER
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br

MENSAGEM DE ABERTURA DE CHAMADO NOS PORTAIS
LOJA VD {get_val('People/PEOP')} FAVOR LIGAR PARA CONFIRMAR A NORMALIZAÇÃO E LIBERAÇÃO DE ACESSO COM A CENTRAL DE COMANDO | HORÁRIO DE FUNCIONAMENTO: {horario_fmt} | SAB 24 HORAS | DOM 24 HORAS
            '''
            
            if st.button("📋 Copiar Carimbo"):
                st.write("Carimbo copiado para a área de transferência!")
                st.code(carimbo_txt, language=None)

            # Edição inline na Busca Unificada - layout melhorado
            if st.session_state['edit_mode']:
                st.markdown('---')
                st.markdown('### ✏️ Edição Inline dos Campos Principais')
                # Definir campos de cada card
                card1_fields = [
                    'People/PEOP', 'Status_Loja', 'LOJAS', 'CODIGO', 'ENDEREÇO',
                    'BAIRRO', 'CIDADE', 'UF', 'CEP', '2ª_a_6ª', 'VD_NOVO'
                ]
                card2_fields = [
                    'TELEFONE1', 'TELEFONE2', 'CELULAR', 'E_MAIL', 'SAB', 'DOM',
                    'FUNC.', 'NOME_GGL', 'NOME_GR'
                ]
                peop_code = row['People/PEOP']
                # Descobrir origem do dado (se existe no inventario ou só loja)
                conn = get_connection()
                cur = conn.cursor()
                cur.execute('SELECT 1 FROM inventario_planilha1 WHERE People = ?', (peop_code,))
                is_inventario = cur.fetchone() is not None
                conn.close()
                updated_values = {}
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('#### Dados Principais')
                    for field in card1_fields:
                        if field in row:
                            current_value = row[field] if pd.notnull(row[field]) else ""
                            new_value = st.text_input(f"{field}", value=str(current_value), key=f"edit_inline_{field}_{peop_code}")
                            if new_value != str(current_value):
                                updated_values[field] = new_value
                with col2:
                    st.markdown('#### Contatos e Operação')
                    for field in card2_fields:
                        if field in row:
                            current_value = row[field] if pd.notnull(row[field]) else ""
                            new_value = st.text_input(f"{field}", value=str(current_value), key=f"edit_inline_{field}_{peop_code}")
                            if new_value != str(current_value):
                                updated_values[field] = new_value
                # Salvar alterações
                if updated_values:
                    st.markdown('---')
                    if st.button('💾 Salvar Alterações Inline'):
                        success_count = 0
                        error_messages = []
                        editable_fields_inv = get_editable_fields_inventario()
                        for field, new_value in updated_values.items():
                            if is_inventario and field in editable_fields_inv:
                                success, message = update_inventario_record(peop_code, field, new_value)
                            else:
                                success, message = update_lojas_record(peop_code, field, new_value)
                            if success:
                                success_count += 1
                            else:
                                error_messages.append(f"{field}: {message}")
                        if success_count == len(updated_values):
                            st.success(f"✅ {success_count} campo(s) atualizado(s) com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"❌ Erro ao atualizar alguns campos:")
                            for error in error_messages:
                                st.error(error)
        else:
            st.warning(f"Nenhum registro encontrado para o código {people_code}")

elif opcao == "Edição de Dados":
    st.subheader("✏️ Edição de Dados")
    st.info("Selecione uma tabela e um registro para editar os campos.")
    
    # Seleção da tabela
    tables = get_tables()
    selected_table = st.selectbox("Selecione a tabela:", tables)
    
    if selected_table:
        # Carregar dados da tabela
        df = load_table(selected_table, limit=100)
        
        if not df.empty:
            st.write(f"**Tabela: {selected_table}** ({len(df)} registros)")
            
            # Seleção do registro
            if 'People' in df.columns:
                id_column = 'People'
            elif 'PEOP' in df.columns:
                id_column = 'PEOP'
            else:
                id_column = df.columns[0]  # Primeira coluna como ID
            
            record_ids = df[id_column].dropna().unique()
            selected_id = st.selectbox(f"Selecione o {id_column}:", record_ids)
            
            if selected_id:
                # Filtrar o registro selecionado
                record = df[df[id_column] == selected_id].iloc[0]
                
                st.markdown("---")
                st.markdown(f"### 📝 Editando: {id_column} = {selected_id}")
                
                # Determinar campos editáveis baseado na tabela
                if selected_table == 'lojas_lojas':
                    editable_fields = get_editable_fields_lojas()
                    update_func = update_lojas_record
                    id_field = 'PEOP'
                elif selected_table == 'inventario_planilha1':
                    editable_fields = get_editable_fields_inventario()
                    update_func = update_inventario_record
                    id_field = 'People'
                else:
                    editable_fields = [col for col in df.columns if col != id_column]
                    update_func = None
                    id_field = id_column
                
                # Interface de edição
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Campos Editáveis")
                    
                with col2:
                    st.markdown("#### Valores Atuais")
                
                # Criar campos de edição
                updated_values = {}
                
                for i, field in enumerate(editable_fields):
                    if field in record:
                        current_value = record[field] if pd.notnull(record[field]) else ""
                        
                        with col1:
                            st.write(f"**{field}:**")
                        
                        with col2:
                            # Campo de edição
                            new_value = st.text_input(
                                f"Editar {field}",
                                value=str(current_value),
                                key=f"edit_{field}_{selected_id}",
                                label_visibility="collapsed"
                            )
                            
                            if new_value != str(current_value):
                                updated_values[field] = new_value
                
                # Botão de salvar
                if updated_values and update_func:
                    st.markdown("---")
                    if st.button("💾 Salvar Alterações", type="primary"):
                        success_count = 0
                        error_messages = []
                        
                        for field, new_value in updated_values.items():
                            success, message = update_func(selected_id, field, new_value)
                            if success:
                                success_count += 1
                            else:
                                error_messages.append(f"{field}: {message}")
                        
                        if success_count == len(updated_values):
                            st.success(f"✅ {success_count} campo(s) atualizado(s) com sucesso!")
                            st.rerun()  # Recarregar dados
                        else:
                            st.error(f"❌ Erro ao atualizar alguns campos:")
                            for error in error_messages:
                                st.error(error)
                
                elif updated_values:
                    st.warning("⚠️ Edição não disponível para esta tabela")
                
                # Exibir registro atual
                st.markdown("---")
                st.markdown("#### 📊 Registro Atual")
                st.dataframe(pd.DataFrame([record]), use_container_width=True)

elif opcao == "Visualizar Tabelas":
    st.subheader("📊 Visualizar Tabelas")
    
    tables = get_tables()
    selected_table = st.selectbox("Selecione uma tabela:", tables)
    
    if selected_table:
        limit = st.slider("Limite de registros:", min_value=10, max_value=1000, value=100, step=10)
        df = load_table(selected_table, limit)
        
        st.write(f"**Tabela: {selected_table}**")
        st.write(f"Total de registros carregados: {len(df)}")
        
        # Estatísticas básicas
        st.write("**Estatísticas:**")
        st.write(f"- Colunas: {len(df.columns)}")
        st.write(f"- Registros: {len(df)}")
        
        st.dataframe(df, use_container_width=True)

elif opcao == "Consulta SQL Customizada":
    st.subheader("🔧 Consulta SQL Customizada")
    st.info("Digite sua consulta SQL personalizada.")
    
    query = st.text_area("SQL Query:", height=150, placeholder="SELECT * FROM lojas_lojas LIMIT 10")
    
    if st.button("Executar Query"):
        if query.strip():
            df, error = run_custom_query(query)
            if error:
                st.error(f"Erro na query: {error}")
            else:
                st.success(f"Query executada com sucesso! {len(df)} registros encontrados.")
                st.dataframe(df, use_container_width=True)
        else:
            st.warning("Digite uma query SQL válida.")

elif opcao == "Sobre":
    st.subheader("ℹ️ Sobre o Sistema")
    st.markdown("""
    ### Sistema de Consulta e Edição VD
    
    **Funcionalidades:**
    - 🔎 **Busca Unificada**: Pesquisa por código People/PEOP em ambas as tabelas
    - ✏️ **Edição de Dados**: Edição inline com salvamento automático
    - 📊 **Visualização**: Visualização completa das tabelas
    - 🔧 **SQL Customizado**: Consultas SQL personalizadas
    - 🏷️ **Carimbo**: Geração automática de carimbos para chamados
    
    **Tabelas Disponíveis:**
    - `inventario_planilha1`: Dados do inventário
    - `lojas_lojas`: Dados das lojas
    
    **Desenvolvido para:** Sistema de consulta e manutenção de dados VD
    """)

# Footer
st.markdown("---")
st.markdown("*Sistema de Consulta VD - Desenvolvido para otimizar processos de consulta e edição de dados*") 