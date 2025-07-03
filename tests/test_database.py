"""
Testes unitários para o módulo database
"""
import pytest
import sys
from pathlib import Path

# Adicionar src ao path
current_dir = Path(__file__).parent.parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from src.database import (
    get_connection, get_tables, load_table,
    unified_search_people, search_by_designation,
    search_by_id_vivo, search_by_address, search_by_ggl_gr,
    get_dashboard_stats
)

class TestDatabaseConnection:
    """Testes para conexão com banco de dados"""
    
    def test_get_connection(self):
        """Testa se a conexão com o banco é estabelecida"""
        conn = get_connection()
        assert conn is not None
        conn.close()
    
    def test_get_tables(self):
        """Testa se as tabelas são listadas corretamente"""
        tables = get_tables()
        assert isinstance(tables, list)
        assert len(tables) > 0
        # Verificar se as tabelas principais existem
        expected_tables = ['lojas', 'inventario', 'operadoras', 'circuitos']
        for table in expected_tables:
            assert table in [t.lower() for t in tables]

class TestDatabaseQueries:
    """Testes para consultas do banco de dados"""
    
    def test_load_table(self):
        """Testa carregamento de tabela"""
        # Testar carregamento da tabela lojas
        df = load_table('lojas')
        assert df is not None
        assert len(df) > 0
        assert 'id' in df.columns
    
    def test_unified_search_people(self):
        """Testa busca unificada de pessoas"""
        # Testar busca com termo vazio
        results = unified_search_people("")
        assert isinstance(results, list)
        
        # Testar busca com termo válido
        results = unified_search_people("teste")
        assert isinstance(results, list)
    
    def test_search_by_designation(self):
        """Testa busca por designação"""
        results = search_by_designation("teste")
        assert isinstance(results, list)
    
    def test_search_by_id_vivo(self):
        """Testa busca por ID Vivo"""
        results = search_by_id_vivo("teste")
        assert isinstance(results, list)
    
    def test_search_by_address(self):
        """Testa busca por endereço"""
        results = search_by_address("teste")
        assert isinstance(results, list)
    
    def test_search_by_ggl_gr(self):
        """Testa busca por GGL/GR"""
        results = search_by_ggl_gr("teste")
        assert isinstance(results, list)
    
    def test_get_dashboard_stats(self):
        """Testa obtenção de estatísticas do dashboard"""
        stats = get_dashboard_stats()
        assert isinstance(stats, dict)
        assert 'total_lojas' in stats
        assert 'total_circuitos' in stats
        assert 'lojas_por_status' in stats
        assert 'circuitos_por_operadora' in stats
        assert 'lojas_por_uf' in stats

class TestDatabaseErrorHandling:
    """Testes para tratamento de erros"""
    
    def test_invalid_table_load(self):
        """Testa carregamento de tabela inexistente"""
        with pytest.raises(Exception):
            load_table('tabela_inexistente')
    
    def test_invalid_search_terms(self):
        """Testa busca com termos inválidos"""
        # Deve retornar lista vazia ou None, não gerar erro
        results = unified_search_people(None)
        assert results is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 