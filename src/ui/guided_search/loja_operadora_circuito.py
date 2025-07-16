import streamlit as st
import pandas as pd
from src.database.connection import get_connection
from src.ui.components import display_search_results, export_dataframe

def get_lojas_filtradas(busca_loja):
    conn = get_connection()
    lojas = pd.read_sql_query(
        'SELECT DISTINCT People, LOJAS FROM inventario_planilha1 LEFT JOIN lojas_lojas ON inventario_planilha1.People = lojas_lojas.PEOP ORDER BY LOJAS', conn)
    conn.close()
    if busca_loja.strip():
        return lojas[lojas['LOJAS'].str.contains(busca_loja, case=False, na=False) | lojas['People'].astype(str).str.contains(busca_loja, case=False, na=False)]
    return lojas.iloc[:0]

def get_operadoras_para_loja(people_sel):
    conn = get_connection()
    operadoras = pd.read_sql_query(
        'SELECT DISTINCT Operadora FROM inventario_planilha1 WHERE People = ? AND Operadora IS NOT NULL AND Operadora != ""',
        conn, params=(people_sel,))['Operadora'].sort_values().tolist()
    conn.close()
    return operadoras

def get_circuitos_para_loja_operadora(people_sel, operadora_sel):
    conn = get_connection()
    circuitos = pd.read_sql_query(
        'SELECT DISTINCT "Circuito_Designação", "Novo_Circuito_Designação" FROM inventario_planilha1 WHERE People = ? AND Operadora = ?',
        conn, params=(people_sel, operadora_sel))
    conn.close()
    return pd.unique(pd.concat([circuitos["Circuito_Designação"], circuitos["Novo_Circuito_Designação"]]).dropna())

def get_detalhes_circuito(people_sel, operadora_sel, circuito_sel):
    conn = get_connection()
    df_circ = pd.read_sql_query(
        '''SELECT * FROM inventario_planilha1 LEFT JOIN lojas_lojas ON inventario_planilha1.People = lojas_lojas.PEOP
           WHERE inventario_planilha1.People = ? AND inventario_planilha1.Operadora = ?
           AND (inventario_planilha1."Circuito_Designação" = ? OR inventario_planilha1."Novo_Circuito_Designação" = ?)''',
        conn, params=(people_sel, operadora_sel, circuito_sel, circuito_sel))
    conn.close()
    return df_circ

def interface_busca_loja_operadora_circuito():
    st.title("🔎 Busca Loja > Operadora > Circuito")
    busca_loja = st.text_input("Busque a Loja (nome ou código):", "")
    lojas_filtradas = get_lojas_filtradas(busca_loja)
    opcoes_loja = [f"{row['People']} - {row['LOJAS']}" for _, row in lojas_filtradas.iterrows()]
    idx_loja = st.selectbox("Selecione a Loja:", range(len(opcoes_loja)), format_func=lambda i: opcoes_loja[i]) if opcoes_loja else None
    if idx_loja is not None:
        people_sel = lojas_filtradas.iloc[idx_loja]['People']
        operadoras = get_operadoras_para_loja(people_sel)
        operadora_sel = st.selectbox("Selecione a Operadora:", operadoras) if operadoras else None
        if operadora_sel:
            circuitos_list = get_circuitos_para_loja_operadora(people_sel, operadora_sel)
            circuito_sel = st.selectbox("Selecione o Circuito/Designação:", circuitos_list) if len(circuitos_list) > 0 else None
            if circuito_sel:
                df_circ = get_detalhes_circuito(people_sel, operadora_sel, circuito_sel)
                if not df_circ.empty:
                    st.success(f"{len(df_circ)} registro(s) encontrado(s)")
                    display_search_results(df_circ, search_context='circuito', circuito_selecionado=circuito_sel)
                    export_dataframe(df_circ, filename_prefix="circuito_resultado")
                else:
                    st.warning("Nenhum registro encontrado para o circuito/designação selecionado.") 