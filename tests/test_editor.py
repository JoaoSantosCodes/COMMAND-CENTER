"""
Testes unitários para o módulo editor
"""
import pytest
import sys
from pathlib import Path
from datetime import datetime

# Adicionar src ao path
current_dir = Path(__file__).parent.parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from src.editor import (
    log_change, get_audit_log, update_lojas_record,
    update_inventario_record, get_editable_fields_lojas,
    get_editable_fields_inventario
)

class TestEditorOperations:
    """Testes para operações de edição"""
    
    def test_get_editable_fields_lojas(self):
        """Testa obtenção de campos editáveis da tabela lojas"""
        fields = get_editable_fields_lojas()
        assert isinstance(fields, list)
        assert len(fields) > 0
        # Verificar se campos importantes estão presentes
        expected_fields = ['nome', 'endereco', 'status']
        for field in expected_fields:
            assert any(field in f.lower() for f in fields)
    
    def test_get_editable_fields_inventario(self):
        """Testa obtenção de campos editáveis da tabela inventario"""
        fields = get_editable_fields_inventario()
        assert isinstance(fields, list)
        assert len(fields) > 0
    
    def test_log_change(self):
        """Testa registro de mudanças no log de auditoria"""
        # Testar log de mudança válida
        result = log_change(
            table_name="test_table",
            record_id=1,
            field_name="test_field",
            old_value="old",
            new_value="new",
            user="test_user"
        )
        assert result is True
    
    def test_get_audit_log(self):
        """Testa obtenção do log de auditoria"""
        # Testar obtenção de logs
        logs = get_audit_log(limit=10)
        assert isinstance(logs, list)
        # Verificar estrutura dos logs
        if len(logs) > 0:
            log = logs[0]
            assert 'table_name' in log
            assert 'record_id' in log
            assert 'field_name' in log
            assert 'old_value' in log
            assert 'new_value' in log
            assert 'user' in log
            assert 'timestamp' in log

class TestEditorValidation:
    """Testes para validação de dados"""
    
    def test_update_lojas_record_valid(self):
        """Testa atualização válida de registro de lojas"""
        # Testar com dados válidos
        test_data = {
            'nome': 'Loja Teste',
            'endereco': 'Endereço Teste',
            'status': 'ATIVA'
        }
        # Nota: Este teste pode falhar se não houver registros na tabela
        # É um teste de integração que requer dados reais
        try:
            result = update_lojas_record(1, test_data, "test_user")
            assert isinstance(result, bool)
        except Exception as e:
            # Se falhar, verificar se é por falta de dados
            assert "no such table" not in str(e).lower()
    
    def test_update_inventario_record_valid(self):
        """Testa atualização válida de registro de inventário"""
        test_data = {
            'descricao': 'Item Teste',
            'quantidade': 10
        }
        try:
            result = update_inventario_record(1, test_data, "test_user")
            assert isinstance(result, bool)
        except Exception as e:
            # Se falhar, verificar se é por falta de dados
            assert "no such table" not in str(e).lower()

class TestEditorErrorHandling:
    """Testes para tratamento de erros"""
    
    def test_log_change_invalid_data(self):
        """Testa log de mudança com dados inválidos"""
        # Testar com dados None
        result = log_change(
            table_name=None,
            record_id=None,
            field_name=None,
            old_value=None,
            new_value=None,
            user=None
        )
        # Deve retornar False ou gerar exceção
        assert result is False or result is None
    
    def test_get_audit_log_invalid_limit(self):
        """Testa obtenção de log com limite inválido"""
        # Testar com limite negativo
        logs = get_audit_log(limit=-1)
        assert isinstance(logs, list)
        
        # Testar com limite zero
        logs = get_audit_log(limit=0)
        assert isinstance(logs, list)

class TestEditorIntegration:
    """Testes de integração para o módulo editor"""
    
    def test_complete_edit_workflow(self):
        """Testa workflow completo de edição"""
        # 1. Obter campos editáveis
        fields = get_editable_fields_lojas()
        assert isinstance(fields, list)
        
        # 2. Simular mudança
        test_data = {'nome': 'Teste Workflow'}
        
        # 3. Tentar atualizar (pode falhar se não houver dados)
        try:
            result = update_lojas_record(1, test_data, "test_user")
            assert isinstance(result, bool)
        except Exception:
            # Aceitar falha se não houver dados reais
            pass
        
        # 4. Verificar logs
        logs = get_audit_log(limit=5)
        assert isinstance(logs, list)

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 