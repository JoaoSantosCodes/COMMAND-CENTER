import sqlite3
import pandas as pd
from datetime import datetime

def gerar_relatorio_estrutura():
    """
    Gera um relatório detalhado da estrutura dos dados
    """
    conn = sqlite3.connect("consulta_vd.db")
    
    # Cabeçalho do relatório
    relatorio = []
    relatorio.append("# RELATÓRIO DE ESTRUTURA DE DADOS - CONSULTAVD")
    relatorio.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    relatorio.append("=" * 80)
    relatorio.append("")
    
    # Informações gerais do banco
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    relatorio.append("## RESUMO EXECUTIVO")
    relatorio.append("")
    relatorio.append(f"**Total de tabelas:** {len(tables)}")
    
    total_registros = 0
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        total_registros += count
        relatorio.append(f"- {table_name}: {count:,} registros")
    
    relatorio.append(f"**Total de registros:** {total_registros:,}")
    relatorio.append("")
    
    # Detalhamento por tabela
    for table in tables:
        table_name = table[0]
        relatorio.append(f"## TABELA: {table_name.upper()}")
        relatorio.append("")
        
        # Contagem de registros
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        relatorio.append(f"**Total de registros:** {count:,}")
        relatorio.append("")
        
        # Estrutura da tabela
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        relatorio.append("### Estrutura das Colunas")
        relatorio.append("")
        relatorio.append("| Campo | Tipo | Not Null | Default | Primary Key |")
        relatorio.append("|-------|------|----------|---------|-------------|")
        
        for col in columns:
            cid, name, type_name, not_null, default_val, pk = col
            not_null_str = "✓" if not_null else "✗"
            pk_str = "✓" if pk else "✗"
            default_str = str(default_val) if default_val else "NULL"
            relatorio.append(f"| {name} | {type_name} | {not_null_str} | {default_str} | {pk_str} |")
        
        relatorio.append("")
        
        # Análise de dados únicos
        relatorio.append("### Análise de Dados")
        relatorio.append("")
        
        # Amostra de dados
        try:
            df_sample = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
            relatorio.append("**Amostra de dados (primeiros 5 registros):**")
            relatorio.append("")
            relatorio.append("```")
            relatorio.append(df_sample.to_string(index=False))
            relatorio.append("```")
            relatorio.append("")
        except Exception as e:
            relatorio.append(f"Erro ao gerar amostra: {e}")
            relatorio.append("")
        
        # Contagem de valores únicos para colunas importantes
        relatorio.append("**Contagem de valores únicos por coluna:**")
        relatorio.append("")
        
        for col in columns[:10]:  # Primeiras 10 colunas
            col_name = col[1]
            try:
                cursor.execute(f"SELECT COUNT(DISTINCT `{col_name}`) FROM {table_name}")
                unique_count = cursor.fetchone()[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE `{col_name}` IS NOT NULL")
                non_null_count = cursor.fetchone()[0]
                
                if non_null_count > 0:
                    percentage = (unique_count / non_null_count) * 100
                    relatorio.append(f"- **{col_name}**: {unique_count:,} valores únicos ({percentage:.1f}% de {non_null_count:,} não-nulos)")
            except Exception as e:
                relatorio.append(f"- **{col_name}**: Erro na análise")
        
        relatorio.append("")
        relatorio.append("-" * 80)
        relatorio.append("")
    
    # Relacionamentos
    relatorio.append("## RELACIONAMENTOS IDENTIFICADOS")
    relatorio.append("")
    
    # Verificar relacionamentos por People/PEOP
    try:
        cursor.execute("""
            SELECT COUNT(*) as total_inventario
            FROM inventario_planilha1 i
            INNER JOIN lojas_lojas l ON i.People = l.PEOP
        """)
        match_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM inventario_planilha1")
        total_inventario = cursor.fetchone()[0]
        
        relatorio.append(f"**Relacionamento People/PEOP:**")
        relatorio.append(f"- Registros com match: {match_count:,}")
        relatorio.append(f"- Total inventário: {total_inventario:,}")
        relatorio.append(f"- Taxa de match: {(match_count/total_inventario)*100:.1f}%")
        relatorio.append("")
    except Exception as e:
        relatorio.append(f"Erro ao analisar relacionamentos: {e}")
        relatorio.append("")
    
    # Estatísticas por região
    try:
        relatorio.append("**Lojas por Região GGL:**")
        cursor.execute("""
            SELECT REGIAO_GGL, COUNT(*) as quantidade
            FROM lojas_lojas
            WHERE REGIAO_GGL IS NOT NULL
            GROUP BY REGIAO_GGL
            ORDER BY quantidade DESC
            LIMIT 10
        """)
        regioes = cursor.fetchall()
        
        for regiao, count in regioes:
            relatorio.append(f"- {regiao}: {count:,} lojas")
        relatorio.append("")
    except Exception as e:
        relatorio.append(f"Erro ao analisar regiões: {e}")
        relatorio.append("")
    
    # Status das lojas
    try:
        relatorio.append("**Status das Lojas:**")
        cursor.execute("""
            SELECT STATUS, COUNT(*) as quantidade
            FROM lojas_lojas
            GROUP BY STATUS
            ORDER BY quantidade DESC
        """)
        status_list = cursor.fetchall()
        
        for status, count in status_list:
            relatorio.append(f"- {status}: {count:,} lojas")
        relatorio.append("")
    except Exception as e:
        relatorio.append(f"Erro ao analisar status: {e}")
        relatorio.append("")
    
    # Recomendações
    relatorio.append("## RECOMENDAÇÕES")
    relatorio.append("")
    relatorio.append("1. **Validação de Dados:**")
    relatorio.append("   - Verificar consistência entre People e PEOP")
    relatorio.append("   - Validar coordenadas geográficas")
    relatorio.append("   - Confirmar CNPJs únicos")
    relatorio.append("")
    relatorio.append("2. **Otimizações:**")
    relatorio.append("   - Criar índices para campos de busca frequente")
    relatorio.append("   - Implementar constraints para integridade")
    relatorio.append("   - Normalizar dados duplicados")
    relatorio.append("")
    relatorio.append("3. **Monitoramento:**")
    relatorio.append("   - Acompanhar crescimento dos dados")
    relatorio.append("   - Verificar qualidade dos dados regularmente")
    relatorio.append("   - Manter backup atualizado")
    relatorio.append("")
    
    # Salvar relatório
    with open("RELATORIO_ESTRUTURA_DADOS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(relatorio))
    
    print("✓ Relatório gerado: RELATORIO_ESTRUTURA_DADOS.md")
    
    # Mostrar resumo no console
    print("\n=== RESUMO DO RELATÓRIO ===")
    print(f"Total de tabelas: {len(tables)}")
    print(f"Total de registros: {total_registros:,}")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"- {table_name}: {count:,} registros")
    
    conn.close()

if __name__ == "__main__":
    gerar_relatorio_estrutura() 