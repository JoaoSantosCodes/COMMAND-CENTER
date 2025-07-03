"""
Testes unitários para o módulo UI
"""
import pytest
import sys
from pathlib import Path
import pandas as pd

# Adicionar src ao path
current_dir = Path(__file__).parent.parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from src.ui import (
    copy_to_clipboard, display_status, display_search_results,
    export_dataframe, get_filter_options, safe_column_filter,
    generate_incident_stamp, validar_informativo_regras,
    validar_informativo_ia, gerar_template_informativo,
    create_dashboard_card, show_error_message, show_success_message,
    inject_responsive_css, interface_busca_loja_operadora_circuito
)

class TestUIComponents:
    """Testes para componentes UI básicos"""
    
    def test_inject_responsive_css(self):
        """Testa injeção de CSS responsivo"""
        # Esta função não retorna nada, apenas verificar se executa sem erro
        try:
            inject_responsive_css()
            assert True  # Se chegou aqui, não houve erro
        except Exception as e:
            pytest.fail(f"inject_responsive_css falhou: {e}")
    
    def test_create_dashboard_card(self):
        """Testa criação de card do dashboard"""
        # Simular dados de teste
        title = "Teste"
        value = "100"
        icon = "📊"
        color = "blue"
        
        # Verificar se a função executa sem erro
        try:
            create_dashboard_card(title, value, icon, color)
            assert True
        except Exception as e:
            pytest.fail(f"create_dashboard_card falhou: {e}")
    
    def test_show_error_message(self):
        """Testa exibição de mensagem de erro"""
        try:
            show_error_message("Teste de erro")
            assert True
        except Exception as e:
            pytest.fail(f"show_error_message falhou: {e}")
    
    def test_show_success_message(self):
        """Testa exibição de mensagem de sucesso"""
        try:
            show_success_message("Teste de sucesso")
            assert True
        except Exception as e:
            pytest.fail(f"show_success_message falhou: {e}")

class TestUIDataHandling:
    """Testes para manipulação de dados na UI"""
    
    def test_copy_to_clipboard(self):
        """Testa cópia para clipboard"""
        test_data = "Dados de teste"
        try:
            copy_to_clipboard(test_data)
            assert True
        except Exception as e:
            pytest.fail(f"copy_to_clipboard falhou: {e}")
    
    def test_display_status(self):
        """Testa exibição de status"""
        test_status = "ATIVA"
        try:
            display_status(test_status)
            assert True
        except Exception as e:
            pytest.fail(f"display_status falhou: {e}")
    
    def test_display_search_results(self):
        """Testa exibição de resultados de busca"""
        # Criar DataFrame de teste
        test_data = {
            'id': [1, 2, 3],
            'nome': ['Item 1', 'Item 2', 'Item 3'],
            'status': ['ATIVA', 'INATIVA', 'ATIVA']
        }
        df = pd.DataFrame(test_data)
        
        try:
            display_search_results(df, "Resultados de teste")
            assert True
        except Exception as e:
            pytest.fail(f"display_search_results falhou: {e}")
    
    def test_export_dataframe(self):
        """Testa exportação de DataFrame"""
        test_data = {
            'id': [1, 2, 3],
            'nome': ['Item 1', 'Item 2', 'Item 3']
        }
        df = pd.DataFrame(test_data)
        
        try:
            export_dataframe(df, "teste_export")
            assert True
        except Exception as e:
            pytest.fail(f"export_dataframe falhou: {e}")
    
    def test_get_filter_options(self):
        """Testa obtenção de opções de filtro"""
        test_data = {
            'status': ['ATIVA', 'INATIVA', 'ATIVA', 'PENDENTE']
        }
        df = pd.DataFrame(test_data)
        
        try:
            options = get_filter_options(df, 'status')
            assert isinstance(options, list)
            assert 'ATIVA' in options
            assert 'INATIVA' in options
            assert 'PENDENTE' in options
        except Exception as e:
            pytest.fail(f"get_filter_options falhou: {e}")
    
    def test_safe_column_filter(self):
        """Testa filtro seguro de colunas"""
        test_data = {
            'id': [1, 2, 3],
            'nome': ['Item 1', 'Item 2', 'Item 3'],
            'status': ['ATIVA', 'INATIVA', 'ATIVA']
        }
        df = pd.DataFrame(test_data)
        
        try:
            filtered_df = safe_column_filter(df, 'status', 'ATIVA')
            assert isinstance(filtered_df, pd.DataFrame)
            assert len(filtered_df) > 0
        except Exception as e:
            pytest.fail(f"safe_column_filter falhou: {e}")

class TestUIValidation:
    """Testes para validação na UI"""
    
    def test_validar_informativo_regras(self):
        """Testa validação de informativo por regras"""
        test_text = "Este é um informativo de teste"
        try:
            result = validar_informativo_regras(test_text)
            assert isinstance(result, dict)
            assert 'is_valid' in result
        except Exception as e:
            pytest.fail(f"validar_informativo_regras falhou: {e}")
    
    def test_validar_informativo_ia(self):
        """Testa validação de informativo por IA"""
        test_text = "Este é um informativo de teste"
        try:
            result = validar_informativo_ia(test_text)
            assert isinstance(result, dict)
            assert 'is_valid' in result
        except Exception as e:
            pytest.fail(f"validar_informativo_ia falhou: {e}")
    
    def test_gerar_template_informativo(self):
        """Testa geração de template de informativo"""
        try:
            template = gerar_template_informativo()
            assert isinstance(template, str)
            assert len(template) > 0
        except Exception as e:
            pytest.fail(f"gerar_template_informativo falhou: {e}")

class TestUIStamps:
    """Testes para carimbos e indicadores visuais"""
    
    def test_generate_incident_stamp(self):
        """Testa geração de carimbo de incidente"""
        test_data = {
            'tipo': 'CRÍTICO',
            'descricao': 'Teste de incidente',
            'prioridade': 'ALTA'
        }
        
        try:
            stamp = generate_incident_stamp(test_data)
            assert isinstance(stamp, str)
            assert len(stamp) > 0
        except Exception as e:
            pytest.fail(f"generate_incident_stamp falhou: {e}")

class TestUIGuidedSearch:
    """Testes para busca guiada"""
    
    def test_interface_busca_loja_operadora_circuito(self):
        """Testa interface de busca guiada"""
        try:
            # Esta função pode não retornar nada ou retornar um valor
            # Apenas verificar se executa sem erro
            interface_busca_loja_operadora_circuito()
            assert True
        except Exception as e:
            pytest.fail(f"interface_busca_loja_operadora_circuito falhou: {e}")

class TestUIErrorHandling:
    """Testes para tratamento de erros na UI"""
    
    def test_display_search_results_empty(self):
        """Testa exibição de resultados vazios"""
        empty_df = pd.DataFrame()
        
        try:
            display_search_results(empty_df, "Resultados vazios")
            assert True
        except Exception as e:
            pytest.fail(f"display_search_results com DataFrame vazio falhou: {e}")
    
    def test_get_filter_options_empty(self):
        """Testa obtenção de opções de filtro com dados vazios"""
        empty_df = pd.DataFrame()
        
        try:
            options = get_filter_options(empty_df, 'coluna_inexistente')
            assert isinstance(options, list)
        except Exception as e:
            pytest.fail(f"get_filter_options com dados vazios falhou: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 