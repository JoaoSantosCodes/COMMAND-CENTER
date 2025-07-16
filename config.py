"""
Configuração central do sistema ConsultaVD
"""
import os
from pathlib import Path

# Configurações do banco de dados
DATABASE_CONFIG = {
    "path": "data/consulta_vd.db",  # Atualizado para nova estrutura
    "backup_path": "data/backup/",
    "max_connections": 10,
    "timeout": 30
}

# Configurações das planilhas
EXCEL_FILES = {
    "inventario": "data/Inventario.xlsx",
    "lojas": "data/Relação de Lojas.xlsx"
}

# Configurações da aplicação Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Consulta VD - Sistema de Consulta e Edição",
    "page_icon": "🏪",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configurações de auditoria
AUDIT_CONFIG = {
    "log_file": "audit_log.json",
    "max_log_entries": 10000,
    "backup_interval_days": 7
}

# Configurações de exportação
EXPORT_CONFIG = {
    "default_limit": 100,
    "max_export_records": 10000,
    "supported_formats": ["xlsx", "csv"]
}

# Configurações de validação
VALIDATION_CONFIG = {
    "min_text_length": 10,
    "max_text_length": 5000,
    "required_fields": {
        "lojas_lojas": ["PEOP", "LOJAS"],
        "inventario_planilha1": ["People"]
    }
}

# Configurações de interface
UI_CONFIG = {
    "theme": {
        "primary_color": "#1f77b4",
        "secondary_color": "#ff7f0e",
        "success_color": "#2ca02c",
        "warning_color": "#d62728",
        "info_color": "#9467bd"
    },
    "dashboard": {
        "cards_per_row": 3,
        "default_chart_height": 400
    }
}

# Configurações de busca
SEARCH_CONFIG = {
    "max_results": 100,
    "fuzzy_search": True,
    "search_timeout": 30
}

# Configurações de carimbos
STAMP_CONFIG = {
    "default_template": "incident",
    "include_timestamp": True,
    "auto_format": True
}

# Configurações de desenvolvimento
DEV_CONFIG = {
    "debug_mode": os.getenv("DEBUG", "False").lower() == "true",
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "enable_profiling": os.getenv("ENABLE_PROFILING", "False").lower() == "true"
}

# Configurações de segurança
SECURITY_CONFIG = {
    "max_login_attempts": 3,
    "session_timeout_minutes": 60,
    "password_min_length": 8
}

# Configurações de backup
BACKUP_CONFIG = {
    "auto_backup": True,
    "backup_interval_hours": 24,
    "max_backup_files": 10,
    "backup_directory": "backups"
}

# Configurações de notificações
NOTIFICATION_CONFIG = {
    "email_notifications": False,
    "smtp_server": "",
    "smtp_port": 587,
    "smtp_username": "",
    "smtp_password": ""
}

# Configurações de relatórios
REPORT_CONFIG = {
    "default_format": "pdf",
    "include_charts": True,
    "include_summary": True,
    "max_records_per_page": 50
}

# Configurações de cache
CACHE_CONFIG = {
    "enable_cache": True,
    "cache_ttl_seconds": 300,
    "max_cache_size_mb": 100
}

# Configurações de API (futuro)
API_CONFIG = {
    "enable_api": False,
    "api_version": "v1",
    "rate_limit_requests": 100,
    "rate_limit_window": 3600
}

# Configurações de integração
INTEGRATION_CONFIG = {
    "enable_external_apis": False,
    "timeout_seconds": 30,
    "retry_attempts": 3
}

# Configurações de monitoramento
MONITORING_CONFIG = {
    "enable_metrics": True,
    "metrics_interval_seconds": 60,
    "alert_threshold": 0.9
}

# Configurações de localização
LOCALE_CONFIG = {
    "default_language": "pt_BR",
    "date_format": "%d/%m/%Y",
    "time_format": "%H:%M",
    "currency": "BRL"
}

# Configurações de acessibilidade
ACCESSIBILITY_CONFIG = {
    "high_contrast": False,
    "large_fonts": False,
    "screen_reader_support": True
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    "enable_lazy_loading": True,
    "batch_size": 1000,
    "connection_pool_size": 10,
    "query_timeout_seconds": 30
}

# Configurações de logs
LOGGING_CONFIG = {
    "log_file": "consulta_vd.log",
    "log_level": "INFO",
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "max_log_size_mb": 10,
    "backup_count": 5
}

# Configurações de testes
TEST_CONFIG = {
    "test_database": "test_consulta_vd.db",
    "test_data_file": "test_data.xlsx",
    "coverage_threshold": 80
}

# Configurações de documentação
DOCS_CONFIG = {
    "auto_generate_docs": True,
    "docs_format": "markdown",
    "include_examples": True
}

# Configurações de deploy
DEPLOY_CONFIG = {
    "production_mode": os.getenv("PRODUCTION", "False").lower() == "true",
    "host": os.getenv("HOST", "localhost"),
    "port": int(os.getenv("PORT", "8501")),
    "workers": int(os.getenv("WORKERS", "1"))
}

# Configurações de ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Configurações específicas por ambiente
ENV_CONFIGS = {
    "development": {
        "debug": True,
        "log_level": "DEBUG",
        "cache_enabled": False
    },
    "staging": {
        "debug": False,
        "log_level": "INFO",
        "cache_enabled": True
    },
    "production": {
        "debug": False,
        "log_level": "WARNING",
        "cache_enabled": True,
        "security_checks": True
    }
}

# Obter configurações do ambiente atual
CURRENT_ENV_CONFIG = ENV_CONFIGS.get(ENVIRONMENT, ENV_CONFIGS["development"])

# Função para obter configuração
def get_config(section: str, key: str = None, default=None):
    """
    Obtém configuração do sistema
    
    Args:
        section (str): Seção da configuração
        key (str, optional): Chave específica
        default: Valor padrão se não encontrado
        
    Returns:
        Configuração solicitada
    """
    config_sections = {
        "database": {
            "name": DATABASE_CONFIG["path"].split("/")[-1],
            "path": DATABASE_CONFIG["path"]
        },
        "streamlit": STREAMLIT_CONFIG,
        "audit": AUDIT_CONFIG,
        "export": EXPORT_CONFIG,
        "validation": VALIDATION_CONFIG,
        "ui": UI_CONFIG,
        "search": SEARCH_CONFIG,
        "stamp": STAMP_CONFIG,
        "dev": DEV_CONFIG,
        "security": SECURITY_CONFIG,
        "backup": BACKUP_CONFIG,
        "notification": NOTIFICATION_CONFIG,
        "report": REPORT_CONFIG,
        "cache": CACHE_CONFIG,
        "api": API_CONFIG,
        "integration": INTEGRATION_CONFIG,
        "monitoring": MONITORING_CONFIG,
        "locale": LOCALE_CONFIG,
        "accessibility": ACCESSIBILITY_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "logging": LOGGING_CONFIG,
        "test": TEST_CONFIG,
        "docs": DOCS_CONFIG,
        "deploy": DEPLOY_CONFIG,
        "environment": CURRENT_ENV_CONFIG
    }
    
    if section not in config_sections:
        return default
    
    section_config = config_sections[section]
    
    if key is None:
        return section_config
    
    return section_config.get(key, default)

# Função para validar configurações
def validate_config():
    """
    Valida as configurações do sistema
    
    Returns:
        tuple: (é_válido, lista_de_erros)
    """
    errors = []
    
    # Validar arquivos necessários
    if not Path(DATABASE_CONFIG["path"]).exists() and not ENVIRONMENT == "test":
        errors.append(f"Banco de dados não encontrado: {DATABASE_CONFIG['path']}")
    
    for excel_name, excel_file in EXCEL_FILES.items():
        if not Path(excel_file).exists() and not ENVIRONMENT == "test":
            errors.append(f"Planilha não encontrada: {excel_file}")
    
    # Validar configurações de segurança
    if get_config("security", "password_min_length") < 6:
        errors.append("Senha mínima deve ter pelo menos 6 caracteres")
    
    # Validar configurações de performance
    if get_config("performance", "batch_size") <= 0:
        errors.append("Tamanho do lote deve ser maior que zero")
    
    return len(errors) == 0, errors 