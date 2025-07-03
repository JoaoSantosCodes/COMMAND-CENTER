"""
Configurações de produção para ConsultaVD
"""
import os
from pathlib import Path

# Configurações de ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configurações do banco de dados
DATABASE_CONFIG = {
    "path": os.getenv("DATABASE_PATH", "data/consulta_vd.db"),
    "backup_path": os.getenv("BACKUP_PATH", "data/backup/"),
    "max_connections": int(os.getenv("DB_MAX_CONNECTIONS", "20")),
    "timeout": int(os.getenv("DB_TIMEOUT", "30"))
}

# Configurações de segurança
SECURITY_CONFIG = {
    "secret_key": os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
    "algorithm": "HS256",
    "access_token_expire_minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
    "cors_origins": os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:80").split(",")
}

# Configurações de cache
CACHE_CONFIG = {
    "enable_cache": os.getenv("ENABLE_CACHE", "true").lower() == "true",
    "cache_ttl_seconds": int(os.getenv("CACHE_TTL_SECONDS", "300")),
    "max_cache_size_mb": int(os.getenv("MAX_CACHE_SIZE_MB", "100"))
}

# Configurações de logging
LOGGING_CONFIG = {
    "log_file": os.getenv("LOG_FILE", "logs/consulta_vd.log"),
    "log_level": LOG_LEVEL,
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "max_log_size_mb": int(os.getenv("MAX_LOG_SIZE_MB", "10")),
    "backup_count": int(os.getenv("LOG_BACKUP_COUNT", "5"))
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    "enable_lazy_loading": True,
    "batch_size": int(os.getenv("BATCH_SIZE", "1000")),
    "connection_pool_size": int(os.getenv("CONNECTION_POOL_SIZE", "10")),
    "query_timeout_seconds": int(os.getenv("QUERY_TIMEOUT_SECONDS", "30"))
}

# Configurações de monitoramento
MONITORING_CONFIG = {
    "enable_metrics": os.getenv("ENABLE_METRICS", "true").lower() == "true",
    "metrics_interval_seconds": int(os.getenv("METRICS_INTERVAL_SECONDS", "60")),
    "alert_threshold": float(os.getenv("ALERT_THRESHOLD", "0.9"))
}

# Configurações de backup
BACKUP_CONFIG = {
    "auto_backup": os.getenv("AUTO_BACKUP", "true").lower() == "true",
    "backup_interval_hours": int(os.getenv("BACKUP_INTERVAL_HOURS", "24")),
    "max_backup_files": int(os.getenv("MAX_BACKUP_FILES", "10")),
    "backup_directory": os.getenv("BACKUP_DIRECTORY", "backups")
}

# Configurações de API
API_CONFIG = {
    "title": "ConsultaVD API",
    "description": "API REST para o sistema ConsultaVD",
    "version": "2.0.0",
    "docs_url": "/docs" if DEBUG else None,
    "redoc_url": "/redoc" if DEBUG else None
}

# Configurações de servidor
SERVER_CONFIG = {
    "host": os.getenv("HOST", "0.0.0.0"),
    "port": int(os.getenv("PORT", "8000")),
    "workers": int(os.getenv("WORKERS", "4")),
    "reload": DEBUG
}

def get_production_config():
    """Retorna configurações de produção"""
    return {
        "environment": ENVIRONMENT,
        "debug": DEBUG,
        "database": DATABASE_CONFIG,
        "security": SECURITY_CONFIG,
        "cache": CACHE_CONFIG,
        "logging": LOGGING_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "monitoring": MONITORING_CONFIG,
        "backup": BACKUP_CONFIG,
        "api": API_CONFIG,
        "server": SERVER_CONFIG
    }
