#!/usr/bin/env python3
"""
Teste da estrutura modular do ConsultaVD
Versão 2.0 - Modular
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import importlib
import sqlite3
import pandas as pd

# Definir current_dir como a raiz do projeto
current_dir = Path(__file__).parent.parent.resolve()
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"* {title}")
    print("="*60)

def print_step(step):
    """Imprime passo do teste"""
    print(f"\n- {step}")
    print("-" * 40)

def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"OK {message}")

def print_error(message):
    """Imprime mensagem de erro"""
    print(f"ERRO {message}")

def test_file_structure():
    """Testa estrutura de arquivos"""
    print_step("Testando estrutura de arquivos")
    
    required_files = [
        "src/__init__.py",
        "src/database/__init__.py",
        "src/database/connection.py",
        "src/database/queries.py",
        "src/editor/__init__.py",
        "src/editor/audit.py",
        "src/editor/operations.py",
        "src/editor/fields.py",
        "src/ui/__init__.py",
        "src/ui/components.py",
        "src/ui/stamps.py",
        "src/ui/validation.py",
        "config.py",
        "app_modular.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (current_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        for file_path in missing_files:
            print_error(f"Arquivo faltando: {file_path}")
        return False
    else:
        print_success("Todos os arquivos necessarios estao presentes")
        return True

def test_module_imports():
    """Testa imports dos módulos"""
    print_step("Testando imports dos modulos")
    
    modules_to_test = [
        "src.database",
        "src.editor", 
        "src.ui",
        "config"
    ]
    
    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print_success(f"Modulo {module_name} importado com sucesso")
        except ImportError as e:
            print_error(f"Erro ao importar {module_name}: {e}")
            return False
    
    return True

def test_config():
    """Testa configurações"""
    print_step("Testando configuracoes")
    
    try:
        import config
        
        # Testar validação
        is_valid, errors = config.validate_config()
        if is_valid:
            print_success("Validacao de configuracoes: Valido")
        else:
            print_error(f"Configuracoes invalidas: {errors}")
            return False
        
        # Testar configurações específicas
        db_path = config.get_config("database", "path")
        if db_path:
            print_success(f"Configuracao database: {db_path}")
        
        page_title = config.get_config("streamlit", "page_title")
        if page_title:
            print_success(f"Configuracao streamlit: {page_title}")
        
        return True
        
    except Exception as e:
        print_error(f"Erro ao testar configuracoes: {e}")
        return False

def test_database():
    """Testa operações do banco"""
    print_step("Testando operacoes do banco de dados")
    
    try:
        from src.database import get_connection, get_tables, load_table
        
        # Testar conexão
        conn = get_connection()
        if conn:
            print_success("Conexao com banco estabelecida")
        
        # Testar listagem de tabelas
        tables = get_tables()
        if tables:
            print_success(f"Tabelas encontradas: {tables}")
        
        # Testar carregamento de tabela
        df = load_table("lojas_lojas", limit=5)
        if df is not None and len(df) > 0:
            print_success(f"Carregamento de tabela: {len(df)} registros")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Erro ao testar banco: {e}")
        return False

def test_search():
    """Testa operações de busca"""
    print_step("Testando operacoes de busca")
    
    try:
        from src.database import unified_search_people, search_by_designation
        
        # Testar busca unificada
        df_unified = unified_search_people("teste")
        if df_unified is not None:
            print_success(f"Busca unificada: {len(df_unified)} resultados")
        
        # Testar busca por designação
        df_designation = search_by_designation("teste")
        if df_designation is not None:
            print_success(f"Busca por designacao: {len(df_designation)} resultados")
        
        return True
        
    except Exception as e:
        print_error(f"Erro ao testar busca: {e}")
        return False

def test_editor():
    """Testa operações do editor"""
    print_step("Testando operacoes do editor")
    
    try:
        from src.editor import get_editable_fields_lojas, get_editable_fields_inventario, get_audit_log
        
        # Testar campos editáveis
        fields_lojas = get_editable_fields_lojas()
        if fields_lojas:
            print_success(f"Campos editaveis lojas: {len(fields_lojas)}")
        
        fields_inventario = get_editable_fields_inventario()
        if fields_inventario:
            print_success(f"Campos editaveis inventario: {len(fields_inventario)}")
        
        # Testar logs de auditoria
        logs = get_audit_log()
        if logs is not None:
            print_success(f"Logs de auditoria: {len(logs)} registros")
        
        return True
        
    except Exception as e:
        print_error(f"Erro ao testar editor: {e}")
        return False

def test_ui():
    """Testa componentes de UI"""
    print_step("Testando componentes de UI")
    
    try:
        from src.ui import display_status, generate_network_stamp, validar_informativo_regras
        
        # Testar formatação de status (sem imprimir o HTML completo)
        status_html = display_status("ATIVA")
        if status_html and "background" in status_html:
            print_success("Formatacao de status: OK")
        else:
            print_error("Formatacao de status falhou")
            return False
        
        # Testar geração de carimbo (usando generate_network_stamp que tem menos parâmetros)
        stamp = generate_network_stamp("Teste Circuito", "VIVO", "ATIVO", "Loja Teste")
        if stamp and len(stamp) > 100:
            print_success(f"Geracao de carimbo: {len(stamp)} caracteres")
        else:
            print_error("Geracao de carimbo falhou")
            return False
        
        # Testar validação de informativo
        points = validar_informativo_regras("Teste de informativo")
        if points is not None:
            print_success(f"Validacao de informativo: {points} pontos")
        else:
            print_error("Validacao de informativo falhou")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Erro ao testar UI: {e}")
        return False

def main():
    """Função principal de teste"""
    print_header("Iniciando testes da estrutura modular do ConsultaVD")
    
    tests = [
        ("Estrutura de arquivos", test_file_structure),
        ("Imports dos modulos", test_module_imports),
        ("Configuracoes", test_config),
        ("Operacoes do banco", test_database),
        ("Operacoes de busca", test_search),
        ("Operacoes do editor", test_editor),
        ("Componentes de UI", test_ui)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Relatório final
    print_header("RESUMO DOS TESTES")
    
    passed = 0
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSOU")
            passed += 1
        else:
            print_error(f"{test_name}: FALHOU")
    
    print(f"\nResultado: {passed}/{len(results)} testes passaram")
    
    if passed == len(results):
        print("Todos os testes passaram! Sistema modular esta funcionando corretamente.")
        return True
    else:
        print("Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 