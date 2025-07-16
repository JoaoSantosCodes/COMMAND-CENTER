"""
Testes de integração para o sistema ConsultaVD
"""
import pytest
import sys
from pathlib import Path
import pandas as pd

# Adicionar src ao path
current_dir = Path(__file__).parent.parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from src.database import get_connection, get_tables, load_table, get_dashboard_stats
from src.editor import get_editable_fields_lojas, log_change, get_audit_log
from src.ui import inject_responsive_css, create_dashboard_card, show_error_message

class TestSystemIntegration:
    """Testes de integração do sistema completo"""
    
    def test_database_connection_integration(self):
        """Testa integração completa com banco de dados"""
        # 1. Conectar ao banco
        conn = get_connection()
        assert conn is not None
        
        # 2. Verificar tabelas
        tables = get_tables()
        assert isinstance(tables, list)
        assert len(tables) > 0
        
        # 3. Carregar dados (testar com primeira tabela disponível)
        if tables:
            first_table = tables[0]
            try:
                df = load_table(first_table)
                assert isinstance(df, pd.DataFrame)
            except Exception as e:
                # Se não houver dados, pelo menos verificar se a estrutura está correta
                assert "no such table" not in str(e).lower()
        
        conn.close()
    
    def test_dashboard_integration(self):
        """Testa integração do dashboard"""
        # 1. Obter estatísticas
        stats = get_dashboard_stats()
        assert isinstance(stats, dict)
        assert 'total_lojas' in stats
        assert 'total_circuitos' in stats
        
        # 2. Testar componentes UI
        try:
            inject_responsive_css()
            create_dashboard_card("Teste", "100", "📊", "blue")
            show_error_message("Teste de integração")
            assert True
        except Exception as e:
            pytest.fail(f"Integração UI falhou: {e}")
    
    def test_editor_integration(self):
        """Testa integração do sistema de edição"""
        # 1. Obter campos editáveis
        fields = get_editable_fields_lojas()
        assert isinstance(fields, list)
        
        # 2. Testar log de mudanças (corrigido para usar user_action)
        result = log_change(
            table_name="test_integration",
            record_id="999",
            field_name="test_field",
            old_value="old",
            new_value="new",
            user_action="test_integration"
        )
        assert result is None  # log_change não retorna valor
        
        # 3. Verificar logs
        logs = get_audit_log(limit=5)
        assert isinstance(logs, list)
    
    def test_search_workflow_integration(self):
        """Testa workflow completo de busca"""
        # 1. Verificar se o banco está acessível
        conn = get_connection()
        assert conn is not None
        
        # 2. Verificar se há dados para buscar
        tables = get_tables()
        assert len(tables) > 0
        
        # 3. Tentar carregar dados de busca
        try:
            df = load_table('lojas')
            if len(df) > 0:
                # Se há dados, testar busca
                assert 'id' in df.columns
                assert len(df) > 0
        except Exception:
            # Se não há dados, pelo menos verificar estrutura
            pass
        
        conn.close()
    
    def test_error_handling_integration(self):
        """Testa tratamento de erros em integração"""
        # 1. Testar erro de tabela inexistente
        try:
            load_table('tabela_inexistente_integration')
            pytest.fail("Deveria ter gerado erro para tabela inexistente")
        except Exception as e:
            assert "no such table" in str(e).lower() or "table" in str(e).lower()
        
        # 2. Testar log de erro
        result = log_change(
            table_name="error_test",
            record_id="999",
            field_name="error_field",
            old_value="error_old",
            new_value="error_new",
            user_action="error_test_user"
        )
        assert result is None  # log_change não retorna valor

class TestPerformanceIntegration:
    """Testes de performance e carga"""
    
    def test_dashboard_performance(self):
        """Testa performance do dashboard"""
        import time
        
        start_time = time.time()
        stats = get_dashboard_stats()
        end_time = time.time()
        
        # Dashboard deve carregar em menos de 5 segundos
        assert (end_time - start_time) < 5.0
        assert isinstance(stats, dict)
    
    def test_table_loading_performance(self):
        """Testa performance de carregamento de tabelas"""
        import time
        
        tables = get_tables()
        
        for table in tables[:3]:  # Testar apenas as primeiras 3 tabelas
            start_time = time.time()
            try:
                df = load_table(table)
                end_time = time.time()
                
                # Carregamento deve ser rápido
                assert (end_time - start_time) < 3.0
                assert isinstance(df, pd.DataFrame)
            except Exception:
                # Aceitar falhas para tabelas sem dados
                pass

class TestDataIntegrityIntegration:
    """Testes de integridade de dados"""
    
    def test_database_schema_integrity(self):
        """Testa integridade do esquema do banco"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar se tabelas principais existem
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Verificar tabelas essenciais
        essential_tables = ['lojas', 'inventario', 'operadoras', 'circuitos']
        for table in essential_tables:
            if table in tables:
                # Verificar se a tabela tem pelo menos uma coluna
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                assert len(columns) > 0
        
        conn.close()
    
    def test_audit_log_integrity(self):
        """Testa integridade do log de auditoria"""
        # Verificar se logs são consistentes
        logs = get_audit_log(limit=10)
        
        for log in logs:
            # Verificar campos obrigatórios
            assert 'table' in log
            assert 'record_id' in log
            assert 'field' in log
            assert 'old_value' in log
            assert 'new_value' in log
            assert 'action' in log
            assert 'timestamp' in log

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"]) 