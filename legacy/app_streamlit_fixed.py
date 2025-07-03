import streamlit as st
import pandas as pd
import sqlite3
import io
import plotly.express as px
import json
from datetime import datetime
import time
import inspect

# Configuração da página
st.set_page_config(
    page_title="Consulta VD - Sistema de Consulta e Edição",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_connection():
    return sqlite3.connect('consulta_vd.db')

def get_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    return tables

def load_table(table, limit=100):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT {limit}", conn)
    conn.close()
    return df

def unified_search_people(people_code):
    conn = get_connection()
    query = '''
    SELECT
        i.People as "People/PEOP",
        COALESCE(i.Status_Loja, l.STATUS) as Status_Loja,
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
        l."E_MAIL" as E_MAIL,
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
        l.STATUS as Status_Loja,
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

# Sistema de histórico e auditoria
def log_change(table_name, record_id, field_name, old_value, new_value, user_action="edit"):
    """Registra alterações no sistema"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "table": table_name,
        "record_id": str(record_id),
        "field": field_name,
        "old_value": str(old_value) if old_value is not None else "None",
        "new_value": str(new_value) if new_value is not None else "None",
        "action": user_action
    }
    
    # Salvar em arquivo de log
    try:
        with open("audit_log.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        st.error(f"Erro ao salvar log: {e}")

def get_audit_log(limit=50):
    """Carrega o histórico de alterações"""
    try:
        with open("audit_log.json", "r", encoding="utf-8") as f:
            lines = f.readlines()
            logs = [json.loads(line.strip()) for line in lines[-limit:]]
            return logs
    except FileNotFoundError:
        return []
    except Exception as e:
        st.error(f"Erro ao carregar log: {e}")
        return []

# Funções de edição
def update_lojas_record(peop_code, field, new_value):
    """Atualiza registro na tabela lojas_lojas com log"""
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

def update_inventario_record(people_code, field, new_value):
    """Atualiza registro na tabela inventario_planilha1 com log"""
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

def get_editable_fields_lojas():
    return [
        'LOJAS', 'ENDEREÇO', 'BAIRRO', 'CIDADE', 'UF', 'CEP',
        'TELEFONE1', 'TELEFONE2', 'CELULAR', 'E_MAIL', '2ª_a_6ª',
        'SAB', 'DOM', 'FUNC.', 'VD_NOVO', 'NOME_GGL', 'NOME_GR'
    ]

def get_editable_fields_inventario():
    return [
        'Status_Loja', 'Operadora', 'ID_VIVO', 'Novo_ID_Vivo',
        'Circuito_Designação', 'Novo_Circuito_Designação'
    ]

# Funções de busca adicionais
def search_by_designation(designation):
    conn = get_connection()
    query = '''
    SELECT
        i.People as "People/PEOP",
        COALESCE(i.Status_Loja, l.STATUS) as Status_Loja,
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
        l."E_MAIL" as E_MAIL,
        l."2ª_a_6ª",
        l.SAB,
        l.DOM,
        l."FUNC.",
        l.VD_NOVO,
        l.NOME_GGL,
        l.NOME_GR,
        i."Circuito_Designação",
        i."Novo_Circuito_Designação"
    FROM inventario_planilha1 i
    LEFT JOIN lojas_lojas l ON i.People = l.PEOP
    WHERE i."Circuito_Designação" LIKE ? OR i."Novo_Circuito_Designação" LIKE ?
    '''
    df = pd.read_sql_query(query, conn, params=(f'%{designation}%', f'%{designation}%'))
    conn.close()
    return df

def search_by_id_vivo(id_vivo):
    conn = get_connection()
    query = '''
    SELECT
        i.People as "People/PEOP",
        COALESCE(i.Status_Loja, l.STATUS) as Status_Loja,
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
        l."E_MAIL" as E_MAIL,
        l."2ª_a_6ª",
        l.SAB,
        l.DOM,
        l."FUNC.",
        l.VD_NOVO,
        l.NOME_GGL,
        l.NOME_GR,
        i.ID_VIVO,
        i.Novo_ID_Vivo
    FROM inventario_planilha1 i
    LEFT JOIN lojas_lojas l ON i.People = l.PEOP
    WHERE i.ID_VIVO LIKE ? OR i.Novo_ID_Vivo LIKE ?
    '''
    df = pd.read_sql_query(query, conn, params=(f'%{id_vivo}%', f'%{id_vivo}%'))
    conn.close()
    return df

def search_by_address(address):
    conn = get_connection()
    query = '''
    SELECT
        i.People as "People/PEOP",
        COALESCE(i.Status_Loja, l.STATUS) as Status_Loja,
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
        l."E_MAIL" as E_MAIL,
        l."2ª_a_6ª",
        l.SAB,
        l.DOM,
        l."FUNC.",
        l.VD_NOVO,
        l.NOME_GGL,
        l.NOME_GR
    FROM inventario_planilha1 i
    LEFT JOIN lojas_lojas l ON i.People = l.PEOP
    WHERE l."ENDEREÇO" LIKE ? OR l.BAIRRO LIKE ? OR l.CIDADE LIKE ?
    UNION
    SELECT
        l.PEOP as "People/PEOP",
        l.STATUS as Status_Loja,
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
    WHERE l.PEOP NOT IN (SELECT People FROM inventario_planilha1)
    AND (l."ENDEREÇO" LIKE ? OR l.BAIRRO LIKE ? OR l.CIDADE LIKE ?)
    '''
    df = pd.read_sql_query(query, conn, params=(f'%{address}%', f'%{address}%', f'%{address}%', f'%{address}%', f'%{address}%'))
    conn.close()
    return df

# Função para copiar texto para clipboard
def copy_to_clipboard(text, label="Copiar", unique_id=""):
    """Função para copiar texto com chave única"""
    # Usar timestamp + hash para garantir chave única
    unique_key = f"copy_{hash(text)}_{hash(unique_id)}_{int(time.time() * 1000) % 10000}"
    if st.button(f"📋 {label}", key=unique_key):
        st.write("✅ Copiado!")

# Função para exibir status com cores
def display_status(status):
    if status == "ATIVA":
        return f"🟢 {status}"
    elif status == "INATIVA":
        return f"🔴 {status}"
    elif "INAUGURAR" in str(status).upper():
        return f"🟡 {status}"
    else:
        return f"⚪ {status}"

# Função para exibir resultados de busca
def display_search_results(df, search_context=None, circuito_selecionado=None):
    def safe_val(val):
        return val if val and str(val).strip() not in ('nan', 'None') else '—'

    if df.empty:
        st.warning('Nenhum registro encontrado.')
        return

    # Criar uma lista de opções para o selectbox
    opcoes = [
        f"{safe_val(row.get('People/PEOP'))} - {safe_val(row.get('LOJAS'))} - {safe_val(row.get('ENDEREÇO'))}" for _, row in df.iterrows()
    ]
    selected_idx = st.selectbox('Selecione um registro para ver detalhes:', range(len(opcoes)), format_func=lambda i: opcoes[i])
    row = df.iloc[selected_idx]

    # Detectar contexto de busca (passar parâmetro opcional search_context)
    if search_context is None:
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)
        for f in outer_frames:
            if 'tab5' in f.code_context[0] if f.code_context else '':
                search_context = 'circuito'
            if 'tab1' in f.code_context[0] if f.code_context else '':
                search_context = 'people'

    # Lógica de de-para para campos principais
    vd_novo = safe_val(row.get('VD_NOVO'))
    people_peop = safe_val(row.get('People/PEOP'))
    # Sempre mostrar o código correto
    if people_peop != '—':
        people_vd = people_peop
    elif vd_novo != '—':
        people_vd = vd_novo
    else:
        people_vd = '—'
    novo_circuito = safe_val(row.get('NOVO_CIRCUITO_DESIGNACAO'))
    circuito_designacao = safe_val(row.get('CIRCUITO_DESIGNACAO'))
    # Se veio um valor explicitamente selecionado, use ele
    if circuito_selecionado is not None:
        circuito_final = str(circuito_selecionado)
    else:
        circuito_final = novo_circuito if novo_circuito != '—' else circuito_designacao
    
    novo_id_vivo = safe_val(row.get('NOVO_ID_VIVO'))
    id_vivo = safe_val(row.get('ID_VIVO'))
    id_vivo_final = novo_id_vivo if novo_id_vivo != '—' else id_vivo
    
    operadora = safe_val(row.get('OPERADORA'))

    # Exibir dados em cards organizados
    st.markdown("### 📋 Detalhes do Registro")
    
    # Card 1: Dados Principais
    with st.expander("🏢 Dados Principais", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**People/PEOP/VD NOVO:** {people_vd}")
            st.markdown(f"**Status:** {display_status(safe_val(row.get('Status_Loja')))}")
            st.markdown(f"**Loja:** {safe_val(row.get('LOJAS'))}")
            st.markdown(f"**Código:** {safe_val(row.get('CODIGO'))}")
            # Exibir Circuito Designação apenas se contexto for circuito
            if search_context == 'circuito':
                st.markdown(f"**Circuito Designação:** {circuito_final}")
            if operadora.upper() == 'VIVO':
                st.markdown(f"**ID Vivo:** {id_vivo_final}")
        with col2:
            st.markdown(f"**Endereço:** {safe_val(row.get('ENDEREÇO'))}")
            st.markdown(f"**Bairro:** {safe_val(row.get('BAIRRO'))}")
            st.markdown(f"**Cidade:** {safe_val(row.get('CIDADE'))}")
            st.markdown(f"**UF:** {safe_val(row.get('UF'))}")
            st.markdown(f"**CEP:** {safe_val(row.get('CEP'))}")

    # Card 2: Contatos e Operação
    with st.expander("📞 Contatos e Operação", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Telefones:**")
            celular = safe_val(row.get('CELULAR'))
            telefone1 = safe_val(row.get('TELEFONE1'))
            telefone2 = safe_val(row.get('TELEFONE2'))
            
            if celular != '—':
                st.markdown(f"📱 Celular (Corporativo): {celular}")
                copy_to_clipboard(celular, "Copiar Celular", "celular")
            if telefone1 != '—':
                st.markdown(f"📞 Telefone 1 (VoIP sem fio): {telefone1}")
                copy_to_clipboard(telefone1, "Copiar Telefone 1", "tel1")
            if telefone2 != '—':
                st.markdown(f"📞 Telefone 2 (VoIP com fio): {telefone2}")
                copy_to_clipboard(telefone2, "Copiar Telefone 2", "tel2")
        with col2:
            st.markdown("**E-mail:**")
            email = safe_val(row.get('E_MAIL'))
            if email != '—':
                st.markdown(f"📧 {email}")
                copy_to_clipboard(email, "Copiar E-mail", "email")
            
            st.markdown("**Horários de Funcionamento:**")
            st.markdown(f"**2ª a 6ª:** {safe_val(row.get('2ª_a_6ª'))}")
            st.markdown(f"**Sábado:** {safe_val(row.get('SAB'))}")
            st.markdown(f"**Domingo:** {safe_val(row.get('DOM'))}")

    # Novo bloco: Contato Gerencial
    with st.expander("🧑‍💼 Contato Gerencial", expanded=True):
        nome_ggl = safe_val(row.get('NOME_GGL'))
        nome_gr = safe_val(row.get('NOME_GR'))
        # Buscar contatos na tabela lojas_ggl_gr
        conn = get_connection()
        contato_ggl = contato_gr = None
        if nome_ggl != '—':
            try:
                contato_ggl = pd.read_sql_query('SELECT * FROM lojas_ggl_gr WHERE NOME_GGL = ? LIMIT 1', conn, params=(nome_ggl,))
            except Exception:
                contato_ggl = None
        if nome_gr != '—':
            try:
                contato_gr = pd.read_sql_query('SELECT * FROM lojas_ggl_gr WHERE NOME_GR = ? LIMIT 1', conn, params=(nome_gr,))
            except Exception:
                contato_gr = None
        conn.close()
        colg1, colg2 = st.columns(2)
        with colg1:
            st.markdown("**GGL:**")
            st.markdown(f"{nome_ggl}")
            if contato_ggl is not None and not contato_ggl.empty:
                tel_ggl = safe_val(contato_ggl.iloc[0].get('CELULAR'))
                email_ggl = safe_val(contato_ggl.iloc[0].get('E_MAIL'))
                if tel_ggl != '—':
                    st.markdown(f"📞 {tel_ggl}")
                    copy_to_clipboard(tel_ggl, "Copiar Telefone GGL", "telggl")
                if email_ggl != '—':
                    st.markdown(f"📧 {email_ggl}")
                    copy_to_clipboard(email_ggl, "Copiar E-mail GGL", "emailggl")
        with colg2:
            st.markdown("**GR:**")
            st.markdown(f"{nome_gr}")
            if contato_gr is not None and not contato_gr.empty:
                tel_gr = safe_val(contato_gr.iloc[0].get('CELULAR.1'))
                email_gr = safe_val(contato_gr.iloc[0].get('EMAIL'))
                if tel_gr != '—':
                    st.markdown(f"📞 {tel_gr}")
                    copy_to_clipboard(tel_gr, "Copiar Telefone GR", "telgr")
                if email_gr != '—':
                    st.markdown(f"📧 {email_gr}")
                    copy_to_clipboard(email_gr, "Copiar E-mail GR", "emailgr")

    # Card 3: Carimbo para Chamado
    with st.expander("🖨️ Carimbo para Chamado", expanded=True):
        # Carimbo diferente para aba People/PEOP
        if search_context == 'people':
            carimbo = f"""
**CARIMBO - CONSULTA VD**
Data/Hora: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}
People/PEOP/VD NOVO: {people_vd}
Loja: {safe_val(row.get('LOJAS'))}
Endereço: {safe_val(row.get('ENDEREÇO'))}, {safe_val(row.get('BAIRRO'))} - {safe_val(row.get('CIDADE'))}/{safe_val(row.get('UF'))}
CEP: {safe_val(row.get('CEP'))}
2ª a 6ª: {safe_val(row.get('2ª_a_6ª'))}
Sábado: {safe_val(row.get('SAB'))}
Domingo: {safe_val(row.get('DOM'))}
Status: {safe_val(row.get('Status_Loja'))}
"""
        else:
            carimbo = f"""
**CARIMBO - CONSULTA VD**
Data/Hora: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}
People/PEOP/VD NOVO: {people_vd}
Loja: {safe_val(row.get('LOJAS'))}
Endereço: {safe_val(row.get('ENDEREÇO'))}, {safe_val(row.get('BAIRRO'))} - {safe_val(row.get('CIDADE'))}/{safe_val(row.get('UF'))}
CEP: {safe_val(row.get('CEP'))}
2ª a 6ª: {safe_val(row.get('2ª_a_6ª'))}
Sábado: {safe_val(row.get('SAB'))}
Domingo: {safe_val(row.get('DOM'))}
Status: {safe_val(row.get('Status_Loja'))}
"""
            if circuito_final != '—':
                carimbo += f"Circuito Designação: {circuito_final}\n"
            if operadora.upper() == 'VIVO':
                carimbo += f"ID Vivo: {id_vivo_final}\n"
        st.text_area("Carimbo:", carimbo, height=300, key=f"carimbo_{hash(carimbo)}")
        copy_to_clipboard(carimbo, "Copiar Carimbo Completo", "carimbo")

# Função utilitária para exportação
def export_dataframe(df, filename_prefix="resultado"):
    csv = df.to_csv(index=False).encode('utf-8')
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    st.download_button(
        label="⬇️ Exportar para CSV",
        data=csv,
        file_name=f"{filename_prefix}.csv",
        mime="text/csv",
        key=f"export_csv_{filename_prefix}"
    )
    st.download_button(
        label="⬇️ Exportar para Excel",
        data=excel_buffer,
        file_name=f"{filename_prefix}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"export_xlsx_{filename_prefix}"
    )

# Função utilitária para obter opções únicas de filtro
def get_filter_options(table, column):
    """Obtém opções únicas para filtros de forma segura"""
    try:
        conn = get_connection()
        query = f'SELECT DISTINCT "{column}" FROM {table} WHERE "{column}" IS NOT NULL AND "{column}" != "" ORDER BY 1'
        options = pd.read_sql_query(query, conn)[column].dropna().astype(str).tolist()
        conn.close()
        return options
    except Exception as e:
        st.error(f"Erro ao carregar opções de filtro: {e}")
        return []

# Função para verificar se coluna existe no DataFrame
def safe_column_filter(df, column, values):
    """Filtra DataFrame por coluna apenas se ela existir"""
    if column in df.columns and values:
        return df[df[column].isin(values)]
    return df

# Função para gerar carimbo de incidente
def generate_incident_stamp(sintoma, abrangencia, impacto, descricao_impacto, horario_inicio, horario_termino, status):
    """Gera carimbo formatado para WhatsApp"""
    carimbo = f"""⚠ Informativo incidente:
Sintoma: {sintoma}
Abrangência: {abrangencia}
Impacto: {impacto}
Descrição do impacto: {descricao_impacto}
Horário do início do incidente: {horario_inicio}
Horário do término do incidente: {horario_termino}
Status: {status}"""
    return carimbo

# Sistema de Validação de Informativos
def validar_informativo_regras(texto):
    """Validação baseada em regras (sempre disponível)"""
    problemas = []
    sugestoes = []
    pontuacao = 10
    
    # Verificar campos obrigatórios
    campos_obrigatorios = {
        "loja": ["loja", "store", "filial"],
        "circuito": ["circuito", "circuit", "designação"],
        "operadora": ["operadora", "operator", "vivo", "oi", "claro", "tim"],
        "descrição": ["descrição", "descricao", "description", "problema", "incidente"]
    }
    
    texto_lower = texto.lower()
    
    for campo, palavras_chave in campos_obrigatorios.items():
        if not any(palavra in texto_lower for palavra in palavras_chave):
            problemas.append(f"Campo '{campo}' não encontrado ou não claro")
            pontuacao -= 2
            sugestoes.append(f"Adicione informações sobre {campo}")
    
    # Verificar tamanho
    if len(texto) < 50:
        problemas.append("Informativo muito curto (mínimo 50 caracteres)")
        pontuacao -= 3
        sugestoes.append("Expanda a descrição do incidente")
    elif len(texto) > 1000:
        problemas.append("Informativo muito longo (máximo 1000 caracteres)")
        pontuacao -= 1
        sugestoes.append("Seja mais conciso")
    
    # Verificar estrutura
    if not any(char in texto for char in ['.', '!', '?']):
        problemas.append("Falta pontuação adequada")
        pontuacao -= 1
        sugestoes.append("Use pontuação para melhor clareza")
    
    # Verificar palavras técnicas
    palavras_tecnicas = ["falha", "interrupção", "instabilidade", "lentidão", "indisponível"]
    if not any(palavra in texto_lower for palavra in palavras_tecnicas):
        sugestoes.append("Considere usar termos técnicos mais específicos")
    
    return {
        "pontuacao": max(0, pontuacao),
        "problemas": problemas,
        "sugestoes": sugestoes,
        "status": "✅ Bom" if pontuacao >= 7 else "⚠️ Precisa melhorar" if pontuacao >= 4 else "❌ Precisa revisão"
    }

def validar_informativo_ia(texto):
    """Validação com IA (quando disponível)"""
    try:
        import openai
        # Verificar se API key está configurada
        if not hasattr(st.secrets, "openai_api_key"):
            return {"disponivel": False, "erro": "API key não configurada"}
        
        client = openai.OpenAI(api_key=st.secrets.openai_api_key)
        prompt = f"""
        Analise este informativo de incidente técnico e forneça uma análise estruturada:
        
        INFORMATIVO: {texto}
        
        Responda em formato JSON:
        {{
            \"clareza\": \"pontuação de 1-10\",
            \"completude\": \"pontuação de 1-10\", 
            \"problemas_identificados\": [\"lista de problemas\"],
            \"sugestoes_melhoria\": [\"lista de sugestões\"],
            \"campos_faltando\": [\"campos que podem estar faltando\"],
            \"qualidade_geral\": \"excelente/bom/regular/ruim\"
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        import json
        resultado = json.loads(response.choices[0].message.content)
        resultado["disponivel"] = True
        return resultado
        
    except Exception as e:
        return {"disponivel": False, "erro": str(e)}

def gerar_template_informativo(tipo_incidente):
    """Gera templates baseados no tipo de incidente"""
    templates = {
        "falha_circuito": """
**INCIDENTE: Falha no Circuito**
- **Loja:** [Nome da Loja]
- **Circuito:** [Designação do Circuito]
- **Operadora:** [Nome da Operadora]
- **Descrição:** Circuito apresentando [tipo de falha] desde [horário]
- **Impacto:** [Descrição do impacto]
- **Ações tomadas:** [Lista de ações]
- **Status:** [Status atual]
        """,
        "instabilidade": """
**INCIDENTE: Instabilidade de Conexão**
- **Loja:** [Nome da Loja]
- **Circuito:** [Designação do Circuito]
- **Operadora:** [Nome da Operadora]
- **Descrição:** Conexão instável com [sintomas específicos]
- **Período:** [Horário de início]
- **Frequência:** [Com que frequência ocorre]
- **Ações:** [Medidas tomadas]
        """,
        "lentidao": """
**INCIDENTE: Lentidão na Conexão**
- **Loja:** [Nome da Loja]
- **Circuito:** [Designação do Circuito]
- **Operadora:** [Nome da Operadora]
- **Descrição:** Conexão lenta com velocidade reduzida
- **Velocidade atual:** [Velocidade medida]
- **Velocidade contratada:** [Velocidade esperada]
- **Impacto:** [Como afeta as operações]
        """
    }
    return templates.get(tipo_incidente, "Template não encontrado")

# Interface principal
st.title("🏪 Sistema de Consulta e Edição VD")

# Sidebar
st.sidebar.header("🧭 Navegação")

menu = [
    "🔍 Consultas",
    "📊 Dashboard",
    "🔎 Busca Unificada",
    "📢 Informativos",
    "🛠️ Administração",
    "📝 Edição de Dados",
    "🕵️ Auditoria",
    "📋 Visualizar Tabelas",
    "🧰 Utilitários",
    "❓ Ajuda",
    "ℹ️ Sobre"
]

opcao = st.sidebar.radio(
    "Escolha uma opção:",
    menu,
    index=menu.index("🔎 Busca Unificada")
)

# Lógica: ignore títulos/separadores
if opcao in ["🔍 Consultas", "🛠️ Administração", "🧰 Utilitários"]:
    st.sidebar.info("Selecione uma opção abaixo do título.")
    st.stop()

# Renderização da página com base na opção selecionada
if opcao == "📊 Dashboard":
    st.subheader("📊 Dashboard Resumido")
    conn = get_connection()
    df_lojas = pd.read_sql_query('SELECT * FROM lojas_lojas', conn)
    conn.close()

    # --- Validações e Alertas ---
    alertas = []
    # Lojas sem GGL ou GR
    try:
        sem_ggl = df_lojas[df_lojas['NOME_GGL'].isnull() | (df_lojas['NOME_GGL'].astype(str).str.strip() == '')]
        sem_gr = df_lojas[df_lojas['NOME_GR'].isnull() | (df_lojas['NOME_GR'].astype(str).str.strip() == '')]
        if not sem_ggl.empty:
            alertas.append(f"⚠️ {len(sem_ggl)} loja(s) sem GGL cadastrado.")
        if not sem_gr.empty:
            alertas.append(f"⚠️ {len(sem_gr)} loja(s) sem GR cadastrado.")
    except KeyError:
        pass  # Colunas podem não existir
    
    # Duplicidade de PEOP
    try:
        duplicados = df_lojas['PEOP'][df_lojas['PEOP'].duplicated(keep=False)]
        if not duplicados.empty:
            alertas.append(f"❌ {duplicados.nunique()} código(s) PEOP duplicado(s) na base.")
    except KeyError:
        pass  # Coluna PEOP pode não existir
    
    # Campos obrigatórios vazios
    obrigatorios = ['STATUS', 'LOJAS', 'UF']
    for campo in obrigatorios:
        try:
            vazios = df_lojas[df_lojas[campo].isnull() | (df_lojas[campo].astype(str).str.strip() == '')]
            if not vazios.empty:
                alertas.append(f"⚠️ {len(vazios)} registro(s) com campo '{campo}' vazio.")
        except KeyError:
            pass  # Campo pode não existir
    
    # Lojas ativas sem telefone
    try:
        ativas_sem_tel = df_lojas[
            (df_lojas['STATUS'] == 'ATIVA') & 
            ((df_lojas['TELEFONE1'].isnull()) | (df_lojas['TELEFONE1'].astype(str).str.strip() == ''))
        ]
        if not ativas_sem_tel.empty:
            alertas.append(f"⚠️ {len(ativas_sem_tel)} loja(s) ativa(s) sem Telefone 1 cadastrado.")
    except KeyError:
        pass  # Campos podem não existir
    # Exibir alertas
    if alertas:
        for alerta in alertas:
            st.warning(alerta)
    else:
        st.success("Nenhuma inconsistência crítica encontrada.")

    # Cards de totais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Lojas Ativas", int((df_lojas['STATUS'] == 'ATIVA').sum()))
    with col2:
        st.metric("Lojas Inativas", int((df_lojas['STATUS'] == 'INATIVA').sum()))
    with col3:
        st.metric("A Inaugurar", int((df_lojas['STATUS'] == 'A INAUGURAR').sum()))
    with col4:
        st.metric("Total de Lojas", len(df_lojas))
    st.markdown("---")
    # Gráfico de lojas por status
    st.markdown("#### Lojas por Status")
    status_counts = df_lojas['STATUS'].value_counts().reset_index()
    status_counts.columns = ['STATUS', 'count']
    fig_status = px.bar(status_counts, x='STATUS', y='count', title="Distribuição por Status")
    st.plotly_chart(fig_status, use_container_width=True)
    
    # Gráfico de lojas por GGL
    st.markdown("#### Lojas por Região GGL (Top 10)")
    ggl_counts = df_lojas['NOME_GGL'].value_counts().head(10).reset_index()
    ggl_counts.columns = ['NOME_GGL', 'count']
    fig_ggl = px.bar(ggl_counts, x='NOME_GGL', y='count', title="Top 10 GGLs")
    st.plotly_chart(fig_ggl, use_container_width=True)
    
    # Gráfico de lojas por GR
    st.markdown("#### Lojas por Região GR (Top 10)")
    gr_counts = df_lojas['NOME_GR'].value_counts().head(10).reset_index()
    gr_counts.columns = ['NOME_GR', 'count']
    fig_gr = px.bar(gr_counts, x='NOME_GR', y='count', title="Top 10 GRs")
    st.plotly_chart(fig_gr, use_container_width=True)
    
    # Gráfico de lojas por UF
    st.markdown("#### Lojas por UF")
    uf_counts = df_lojas['UF'].value_counts().reset_index()
    uf_counts.columns = ['UF', 'count']
    fig_uf = px.pie(uf_counts, values='count', names='UF', title="Distribuição por UF")
    st.plotly_chart(fig_uf, use_container_width=True)
    # Gráfico de lojas por Operadora (se disponível)
    st.markdown("#### Lojas por Operadora (Inventário)")
    conn = get_connection()
    df_inv = pd.read_sql_query('SELECT Operadora FROM inventario_planilha1 WHERE Operadora IS NOT NULL AND Operadora != ""', conn)
    conn.close()
    if not df_inv.empty:
        operadora_counts = df_inv['Operadora'].value_counts().reset_index()
        operadora_counts.columns = ['Operadora', 'count']
        fig_op = px.bar(operadora_counts, x='Operadora', y='count', title="Lojas por Operadora")
        st.plotly_chart(fig_op, use_container_width=True)
    else:
        st.info("Sem dados de operadora no inventário.")

elif opcao == "🔎 Busca Unificada":
    st.subheader("🔎 Busca Unificada")
    
    # Criar abas para diferentes tipos de busca
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔍 People/PEOP", "🏷️ Designação", "🆔 ID Vivo", "📍 Endereço", "🔗 Operadora > Loja > Circuito", "🔍 GGL e GR"])
    
    with tab1:
        st.markdown("### Busca por Código People/PEOP")
        people_code = st.text_input("Código People/PEOP:", placeholder="Ex: L1854", key="people_search")
        
        if people_code:
            df_unificado = unified_search_people(people_code)
            if not df_unificado.empty:
                st.success(f"✅ {len(df_unificado)} registro(s) encontrado(s)")
                display_search_results(df_unificado, search_context='people')
                export_dataframe(df_unificado, filename_prefix="unificado_resultado")
            else:
                st.warning("❌ Nenhum registro encontrado")
    
    with tab2:
        st.markdown("### Busca por Designação de Circuito")
        designation = st.text_input("Designação:", placeholder="Ex: VIVO, CLARO, OI", key="designation_search")
        # Filtros avançados
        colf1, colf2, colf3 = st.columns(3)
        with colf1:
            status_opt = get_filter_options('lojas_lojas', 'STATUS')
            status_sel = st.multiselect("Status da Loja:", status_opt, key="status_filter")
        with colf2:
            regiao_opt = get_filter_options('lojas_lojas', 'REGIAO_GGL')
            regiao_sel = st.multiselect("Região GGL:", regiao_opt, key="regiao_filter")
        with colf3:
            uf_opt = get_filter_options('lojas_lojas', 'UF')
            uf_sel = st.multiselect("UF:", uf_opt, key="uf_filter")
        if designation or status_sel or regiao_sel or uf_sel:
            df_designation = search_by_designation(designation)
            # Aplicar filtros no DataFrame de forma segura
            if status_sel:
                df_designation = safe_column_filter(df_designation, 'Status_Loja', status_sel)
            if regiao_sel:
                df_designation = safe_column_filter(df_designation, 'NOME_GGL', regiao_sel)
            if uf_sel:
                df_designation = safe_column_filter(df_designation, 'UF', uf_sel)
            if not df_designation.empty:
                st.success(f"✅ {len(df_designation)} registro(s) encontrado(s)")
                display_search_results(df_designation)
                export_dataframe(df_designation, filename_prefix="designacao_resultado")
            else:
                st.warning("❌ Nenhum registro encontrado")
        else:
            st.info("Preencha pelo menos um campo ou filtro para buscar.")
    
    with tab3:
        st.markdown("### Busca por ID Vivo")
        id_vivo = st.text_input("ID Vivo:", placeholder="Ex: 12345", key="id_vivo_search")
        
        if id_vivo:
            df_id_vivo = search_by_id_vivo(id_vivo)
            if not df_id_vivo.empty:
                st.success(f"✅ {len(df_id_vivo)} registro(s) encontrado(s)")
                display_search_results(df_id_vivo)
                export_dataframe(df_id_vivo, filename_prefix="idvivo_resultado")
            else:
                st.warning("❌ Nenhum registro encontrado")
    
    with tab4:
        st.markdown("### Busca por Endereço")
        address = st.text_input("Endereço, Bairro ou Cidade:", placeholder="Ex: Rua das Flores, Centro, São Paulo", key="address_search")
        
        if address:
            df_address = search_by_address(address)
            if not df_address.empty:
                st.success(f"✅ {len(df_address)} registro(s) encontrado(s)")
                display_search_results(df_address)
                export_dataframe(df_address, filename_prefix="endereco_resultado")
            else:
                st.warning("❌ Nenhum registro encontrado")

    with tab5:
        st.markdown("### Busca Guiada por Loja, Operadora e Circuito/Designação")
        # Campo de busca de loja
        busca_loja = st.text_input("Busque a Loja (nome ou código):", "")
        conn = get_connection()
        lojas = pd.read_sql_query('SELECT DISTINCT People, LOJAS FROM inventario_planilha1 LEFT JOIN lojas_lojas ON inventario_planilha1.People = lojas_lojas.PEOP ORDER BY LOJAS', conn)
        conn.close()
        # Filtrar lojas pelo texto digitado
        if busca_loja.strip():
            lojas_filtradas = lojas[lojas['LOJAS'].str.contains(busca_loja, case=False, na=False) | lojas['People'].astype(str).str.contains(busca_loja, case=False, na=False)]
        else:
            lojas_filtradas = lojas.iloc[:0]  # vazio até digitar
        opcoes_loja = [f"{row['People']} - {row['LOJAS']}" for _, row in lojas_filtradas.iterrows()]
        idx_loja = st.selectbox("Selecione a Loja:", range(len(opcoes_loja)), format_func=lambda i: opcoes_loja[i]) if opcoes_loja else None
        if idx_loja is not None:
            people_sel = lojas_filtradas.iloc[idx_loja]['People']
            # Buscar operadoras disponíveis para a loja
            conn = get_connection()
            operadoras = pd.read_sql_query('SELECT DISTINCT Operadora FROM inventario_planilha1 WHERE People = ? AND Operadora IS NOT NULL AND Operadora != ""', conn, params=(people_sel,))['Operadora'].sort_values().tolist()
            conn.close()
            operadora_sel = st.selectbox("Selecione a Operadora:", operadoras) if operadoras else None
            if operadora_sel:
                # Buscar circuitos/designações para a loja e operadora
                conn = get_connection()
                circuitos = pd.read_sql_query('''SELECT DISTINCT "Circuito_Designação", "Novo_Circuito_Designação" FROM inventario_planilha1 WHERE People = ? AND Operadora = ?''', conn, params=(people_sel, operadora_sel))
                conn.close()
                circuitos_list = pd.unique(pd.concat([circuitos["Circuito_Designação"], circuitos["Novo_Circuito_Designação"]]).dropna())
                circuito_sel = st.selectbox("Selecione o Circuito/Designação:", circuitos_list) if len(circuitos_list) > 0 else None
                if circuito_sel:
                    # Buscar detalhes do circuito selecionado
                    conn = get_connection()
                    df_circ = pd.read_sql_query('''SELECT * FROM inventario_planilha1 LEFT JOIN lojas_lojas ON inventario_planilha1.People = lojas_lojas.PEOP WHERE inventario_planilha1.People = ? AND inventario_planilha1.Operadora = ? AND (inventario_planilha1."Circuito_Designação" = ? OR inventario_planilha1."Novo_Circuito_Designação" = ?)''', conn, params=(people_sel, operadora_sel, circuito_sel, circuito_sel))
                    conn.close()
                    if not df_circ.empty:
                        st.success(f"{len(df_circ)} registro(s) encontrado(s)")
                        display_search_results(df_circ, search_context='circuito', circuito_selecionado=circuito_sel)
                        export_dataframe(df_circ, filename_prefix="circuito_resultado")
                    else:
                        st.warning("Nenhum registro encontrado para o circuito/designação selecionado.")

    with tab6:
        st.markdown("### Validação de GGL e GR")
        nome_ggl = st.text_input("Nome do GGL:", key="ggl_search")
        nome_gr = st.text_input("Nome do GR:", key="gr_search")
        if nome_ggl or nome_gr:
            conn = get_connection()
            # Buscar lojas vinculadas normalmente
            query_lojas = '''
                SELECT * FROM lojas_lojas
                WHERE (? = '' OR NOME_GGL LIKE ?) AND (? = '' OR NOME_GR LIKE ?)
            '''
            df_ggl_gr = pd.read_sql_query(query_lojas, conn, params=(nome_ggl, f'%{nome_ggl}%', nome_gr, f'%{nome_gr}%'))
            # Buscar contato do GGL/GR na tabela de contatos
            query_contato = '''SELECT * FROM lojas_ggl_gr WHERE (? = '' OR NOME_GGL LIKE ?) OR (? = '' OR NOME_GR LIKE ?)'''
            df_contato = pd.read_sql_query(query_contato, conn, params=(nome_ggl, f'%{nome_ggl}%', nome_gr, f'%{nome_gr}%'))
            conn.close()
            # Exibir contato do GGL
            if nome_ggl:
                contato_ggl = df_contato[df_contato['NOME_GGL'].str.contains(nome_ggl, case=False, na=False)]
                if not contato_ggl.empty:
                    row = contato_ggl.iloc[0]
                    st.info(f"**Contato do GGL:**  \nNome: {row.get('NOME_GGL', '-')}", icon="📞")
                    st.write(f"Telefone: {row.get('CELULAR', '-')}")
                    st.write(f"E-mail: {row.get('E_MAIL', '-')}")
            # Exibir contato do GR
            if nome_gr:
                contato_gr = df_contato[df_contato['NOME_GR'].str.contains(nome_gr, case=False, na=False)]
                if not contato_gr.empty:
                    row = contato_gr.iloc[0]
                    st.info(f"**Contato do GR:**  \nNome: {row.get('NOME_GR', '-')}", icon="📞")
                    st.write(f"Telefone: {row.get('CELULAR.1', '-')}")
                    st.write(f"E-mail: {row.get('EMAIL', '-')}")
            if not df_ggl_gr.empty:
                st.success(f"{len(df_ggl_gr)} registro(s) encontrado(s)")
                export_dataframe(df_ggl_gr, filename_prefix="ggl_gr_resultado")
                st.dataframe(df_ggl_gr, use_container_width=True)
            else:
                st.warning("Nenhum registro encontrado para os critérios informados.")
        else:
            st.info("Preencha pelo menos um dos campos para buscar GGL ou GR.")

elif opcao == "📢 Informativos":
    st.title("📢 Sistema de Informativos")
    
    # Abas para diferentes funcionalidades
    tab_info1, tab_info2, tab_info3 = st.tabs(["🤖 Validação com IA", "📋 Templates", "📊 Histórico"])
    
    with tab_info1:
        st.subheader("🤖 Validação Inteligente de Informativos")
        
        # Campo para o informativo
        informativo = st.text_area(
            "Digite o informativo:",
            height=200,
            placeholder="Descreva o incidente aqui..."
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Validar com Regras", type="primary"):
                if informativo.strip():
                    with st.spinner("Analisando..."):
                        resultado_regras = validar_informativo_regras(informativo)
                        
                        st.success("✅ Análise baseada em regras concluída!")
                        
                        # Exibir pontuação
                        st.metric("Pontuação", f"{resultado_regras['pontuacao']}/10")
                        
                        # Status
                        if resultado_regras['status'] == "✅ Bom":
                            st.success(resultado_regras['status'])
                        elif resultado_regras['status'] == "⚠️ Precisa melhorar":
                            st.warning(resultado_regras['status'])
                        else:
                            st.error(resultado_regras['status'])
                        
                        # Problemas encontrados
                        if resultado_regras['problemas']:
                            st.subheader("🚨 Problemas Identificados")
                            for problema in resultado_regras['problemas']:
                                st.error(f"• {problema}")
                        
                        # Sugestões
                        if resultado_regras['sugestoes']:
                            st.subheader("💡 Sugestões de Melhoria")
                            for sugestao in resultado_regras['sugestoes']:
                                st.info(f"• {sugestao}")
                else:
                    st.error("Digite um informativo para validar")
        
        with col2:
            if st.button("🤖 Validar com IA Avançada"):
                if informativo.strip():
                    with st.spinner("Analisando com IA..."):
                        resultado_ia = validar_informativo_ia(informativo)
                        
                        if resultado_ia.get("disponivel"):
                            st.success("✅ Análise com IA concluída!")
                            
                            # Exibir resultados da IA
                            col_ia1, col_ia2 = st.columns(2)
                            with col_ia1:
                                st.metric("Clareza", f"{resultado_ia.get('clareza', 'N/A')}/10")
                            with col_ia2:
                                st.metric("Completude", f"{resultado_ia.get('completude', 'N/A')}/10")
                            
                            # Qualidade geral
                            qualidade = resultado_ia.get('qualidade_geral', 'N/A')
                            if qualidade == 'excelente':
                                st.success(f"🎯 Qualidade: {qualidade.title()}")
                            elif qualidade == 'bom':
                                st.info(f"👍 Qualidade: {qualidade.title()}")
                            elif qualidade == 'regular':
                                st.warning(f"⚠️ Qualidade: {qualidade.title()}")
                            else:
                                st.error(f"❌ Qualidade: {qualidade.title()}")
                            
                            # Problemas da IA
                            if resultado_ia.get('problemas_identificados'):
                                st.subheader("🚨 Análise da IA")
                                for problema in resultado_ia['problemas_identificados']:
                                    st.error(f"• {problema}")
                            
                            # Sugestões da IA
                            if resultado_ia.get('sugestoes_melhoria'):
                                st.subheader("💡 Sugestões da IA")
                                for sugestao in resultado_ia['sugestoes_melhoria']:
                                    st.info(f"• {sugestao}")
                        else:
                            st.warning("⚠️ IA não disponível")
                            st.info(f"Motivo: {resultado_ia.get('erro', 'Configuração necessária')}")
                            st.info("💡 Use a validação baseada em regras (sempre disponível)")
                else:
                    st.error("Digite um informativo para validar")
    
    with tab_info2:
        st.subheader("📋 Templates Inteligentes")
        
        tipo_incidente = st.selectbox(
            "Selecione o tipo de incidente:",
            ["falha_circuito", "instabilidade", "lentidao"],
            format_func=lambda x: {
                "falha_circuito": "🔴 Falha no Circuito",
                "instabilidade": "🟡 Instabilidade de Conexão", 
                "lentidao": "🟠 Lentidão na Conexão"
            }[x]
        )
        
        if st.button("📄 Gerar Template"):
            template = gerar_template_informativo(tipo_incidente)
            st.text_area("Template Gerado:", template, height=300)
            
            if st.button("📋 Copiar Template"):
                st.success("Template copiado para área de transferência!")
    
    with tab_info3:
        st.subheader("📊 Histórico de Validações")
        
        # Simular histórico (em produção, seria salvo no banco)
        st.info("📈 Funcionalidade em desenvolvimento")
        st.info("Aqui será exibido o histórico de validações realizadas")
        
        # Placeholder para futuras implementações
        col_hist1, col_hist2, col_hist3 = st.columns(3)
        with col_hist1:
            st.metric("Total de Validações", "0")
        with col_hist2:
            st.metric("Média de Pontuação", "0.0")
        with col_hist3:
            st.metric("Última Validação", "N/A")

elif opcao == "📝 Edição de Dados":
    st.subheader("✏️ Edição de Dados")
    st.info("Selecione uma tabela e um registro para editar.")
    
    # Seleção da tabela
    tables = get_tables()
    selected_table = st.selectbox("Selecione a tabela:", tables)
    
    if selected_table:
        # Carregar dados
        df = load_table(selected_table, limit=50)
        
        if not df.empty:
            st.write(f"**Tabela: {selected_table}** ({len(df)} registros)")
            
            # Determinar coluna ID
            if 'People' in df.columns:
                id_column = 'People'
            elif 'PEOP' in df.columns:
                id_column = 'PEOP'
            else:
                id_column = df.columns[0]
            
            # Seleção do registro
            record_ids = df[id_column].dropna().unique()
            selected_id = st.selectbox(f"Selecione o {id_column}:", record_ids)
            
            if selected_id:
                # Filtrar registro
                record = df[df[id_column] == selected_id].iloc[0]
                
                st.markdown("---")
                st.markdown(f"### 📝 Editando: {id_column} = {selected_id}")
                
                # Determinar campos editáveis
                if selected_table == 'lojas_lojas':
                    editable_fields = get_editable_fields_lojas()
                    update_func = update_lojas_record
                elif selected_table == 'inventario_planilha1':
                    editable_fields = get_editable_fields_inventario()
                    update_func = update_inventario_record
                else:
                    editable_fields = [col for col in df.columns if col != id_column]
                    update_func = None
                
                # Interface de edição
                st.markdown("#### Campos Editáveis")
                
                updated_values = {}
                
                for field in editable_fields:
                    if field in record:
                        current_value = record[field] if pd.notnull(record[field]) else ""
                        
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            st.write(f"**{field}:**")
                        
                        with col2:
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
                            st.rerun()
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

elif opcao == "🕵️ Auditoria":
    st.subheader("📋 Histórico e Auditoria")
    
    # Filtros para o histórico
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_table = st.selectbox("Filtrar por Tabela:", ["Todas"] + get_tables())
    with col2:
        filter_action = st.selectbox("Filtrar por Ação:", ["Todas", "edit", "create", "delete"])
    with col3:
        limit_logs = st.slider("Quantidade de registros:", 10, 200, 50)
    
    # Carregar logs
    logs = get_audit_log(limit_logs)
    
    if logs:
        # Aplicar filtros
        if filter_table != "Todas":
            logs = [log for log in logs if log.get("table") == filter_table]
        if filter_action != "Todas":
            logs = [log for log in logs if log.get("action") == filter_action]
        
        if logs:
            st.success(f"📊 {len(logs)} alterações encontradas")
            
            # Exibir logs em formato de tabela
            log_df = pd.DataFrame(logs)
            log_df['timestamp'] = pd.to_datetime(log_df['timestamp']).dt.strftime('%d/%m/%Y %H:%M:%S')
            log_df = log_df.rename(columns={
                'timestamp': 'Data/Hora',
                'table': 'Tabela',
                'record_id': 'ID do Registro',
                'field': 'Campo',
                'old_value': 'Valor Anterior',
                'new_value': 'Novo Valor',
                'action': 'Ação'
            })
            
            st.dataframe(log_df, use_container_width=True)
            
            # Estatísticas
            st.markdown("### 📈 Estatísticas")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Alterações", len(logs))
            with col2:
                tables_count = log_df['Tabela'].value_counts()
                st.metric("Tabelas Afetadas", len(tables_count))
            with col3:
                fields_count = log_df['Campo'].value_counts()
                st.metric("Campos Alterados", len(fields_count))
            
            # Gráfico de alterações por tabela
            if len(tables_count) > 0:
                st.markdown("#### Alterações por Tabela")
                fig_tables = px.bar(x=tables_count.index, y=tables_count.values, 
                                   title="Alterações por Tabela")
                st.plotly_chart(fig_tables, use_container_width=True)
            
            # Exportar histórico
            export_dataframe(log_df, filename_prefix="auditoria_historico")
        else:
            st.warning("Nenhuma alteração encontrada com os filtros aplicados.")
    else:
        st.info("📝 Nenhum histórico de alterações encontrado. As alterações serão registradas automaticamente.")

elif opcao == "📋 Visualizar Tabelas":
    st.subheader("📊 Visualizar Tabelas")
    
    tables = get_tables()
    selected_table = st.selectbox("Selecione uma tabela:", tables)
    
    if selected_table:
        limit = st.slider("Limite de registros:", min_value=10, max_value=100, value=50, step=10)
        df = load_table(selected_table, limit)
        
        st.write(f"**Tabela: {selected_table}**")
        st.write(f"Total de registros carregados: {len(df)}")
        st.dataframe(df, use_container_width=True)
        export_dataframe(df, filename_prefix=f"{selected_table}_resultado")

elif opcao == "❓ Ajuda":
    st.subheader("📚 Ajuda e Documentação")
    
    # Criar abas para diferentes tipos de ajuda
    help_tab1, help_tab2, help_tab3, help_tab4 = st.tabs(["🚀 Guia Rápido", "❓ FAQ", "📖 Tutoriais", "🔧 Solução de Problemas"])
    
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
        
        with st.expander("Como exportar resultados?", expanded=False):
            st.markdown("""
            **Resposta:** Em qualquer busca com resultados:
            1. Após exibir os resultados
            2. Clique em "⬇️ Exportar para Excel" ou "⬇️ Exportar para CSV"
            3. O arquivo será baixado automaticamente
            """)
        
        with st.expander("O que significa cada status de loja?", expanded=False):
            st.markdown("""
            **Resposta:**
            - 🟢 **ATIVA**: Loja em funcionamento normal
            - 🔴 **INATIVA**: Loja fechada ou desativada
            - 🟡 **A INAUGURAR**: Loja em processo de abertura
            - ⚪ **Outros**: Status específicos da operação
            """)
    
    with help_tab3:
        st.markdown("### 📖 Tutoriais Detalhados")
        
        st.markdown("#### Tutorial 1: Busca Guiada por Loja")
        st.markdown("""
        1. **Acesse** a aba "🔗 Operadora > Loja > Circuito"
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
        
        st.markdown("#### Tutorial 3: Uso do Dashboard")
        st.markdown("""
        1. **Acesse** o Dashboard no menu principal
        2. **Analise** os cards de totais (ativas, inativas, etc)
        3. **Visualize** os gráficos de distribuição
        4. **Identifique** alertas de inconsistências
        5. **Aja** sobre os problemas identificados
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
        
        st.markdown("#### Problema: Gráficos não carregam")
        st.markdown("""
        **Possíveis causas:**
        - Dados insuficientes para gerar gráficos
        - Problema de conexão com banco
        - Erro na estrutura dos dados
        
        **Soluções:**
        1. Verifique se há dados na tabela
        2. Recarregue a página
        3. Consulte o administrador
        """)
        
        st.markdown("#### Contato para Suporte")
        st.markdown("""
        Se os problemas persistirem:
        - **E-mail**: suporte@empresa.com
        - **Telefone**: (11) 1234-5678
        - **Horário**: Segunda a sexta, 8h às 18h
        """)

elif opcao == "ℹ️ Sobre":
    st.subheader("ℹ️ Sobre o Sistema")
    st.markdown("""
    ### Sistema de Consulta e Edição VD
    
    **Funcionalidades:**
    - 🔎 **Busca Unificada**: Pesquisa por código People/PEOP, designação, ID Vivo e endereço
    - ✏️ **Edição de Dados**: Edição inline com salvamento automático
    - 📊 **Visualização**: Visualização completa das tabelas
    
    **Tabelas Disponíveis:**
    - `inventario_planilha1`: Dados do inventário
    - `lojas_lojas`: Dados das lojas
    
    **Desenvolvido para:** Sistema de consulta e manutenção de dados VD
    """)

# Footer
st.markdown("---")
st.markdown("*Sistema de Consulta VD - Desenvolvido para otimizar processos de consulta e edição de dados*") 