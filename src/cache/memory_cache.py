"""
Sistema de cache em memória para ConsultaVD
"""
import time
import threading
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import hashlib
import json

class MemoryCache:
    """Cache em memória com TTL e estatísticas"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        """
        Inicializa o cache
        
        Args:
            max_size (int): Tamanho máximo do cache
            default_ttl (int): TTL padrão em segundos
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._lock = threading.RLock()
        self._stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'evictions': 0,
            'created_at': datetime.now()
        }
        self._enabled = True
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Gera chave única para os parâmetros"""
        # Converter args e kwargs para string JSON
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtém valor do cache
        
        Args:
            key (str): Chave do cache
            
        Returns:
            Any: Valor armazenado ou None se não encontrado/expirado
        """
        if not self._enabled:
            self._stats['misses'] += 1
            return None
        
        with self._lock:
            if key not in self._cache:
                self._stats['misses'] += 1
                return None
            
            item = self._cache[key]
            
            # Verificar se expirou
            if time.time() > item['expires_at']:
                del self._cache[key]
                self._stats['misses'] += 1
                return None
            
            self._stats['hits'] += 1
            return item['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Armazena valor no cache
        
        Args:
            key (str): Chave do cache
            value (Any): Valor a armazenar
            ttl (int, optional): TTL em segundos
            
        Returns:
            bool: True se armazenado com sucesso
        """
        if not self._enabled:
            return False
        
        ttl = ttl or self._default_ttl
        expires_at = time.time() + ttl
        
        with self._lock:
            # Verificar se precisa evictar
            if len(self._cache) >= self._max_size and key not in self._cache:
                self._evict_oldest()
            
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at,
                'created_at': time.time(),
                'ttl': ttl
            }
            
            self._stats['sets'] += 1
            return True
    
    def _evict_oldest(self):
        """Remove o item mais antigo do cache"""
        if not self._cache:
            return
        
        oldest_key = min(self._cache.keys(), 
                        key=lambda k: self._cache[k]['created_at'])
        del self._cache[oldest_key]
        self._stats['evictions'] += 1
    
    def clear(self):
        """Limpa todo o cache"""
        with self._lock:
            self._cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        with self._lock:
            stats = self._stats.copy()
            stats['current_size'] = len(self._cache)
            stats['max_size'] = self._max_size
            stats['hit_rate'] = (
                stats['hits'] / (stats['hits'] + stats['misses'])
                if (stats['hits'] + stats['misses']) > 0 else 0
            )
            stats['enabled'] = self._enabled
            return stats
    
    def enable(self):
        """Habilita o cache"""
        self._enabled = True
    
    def disable(self):
        """Desabilita o cache"""
        self._enabled = False
    
    def is_enabled(self) -> bool:
        """Verifica se o cache está habilitado"""
        return self._enabled

# Instância global do cache
_cache_instance = MemoryCache()

# ============================================================================
# FUNÇÕES PARA API BACKEND
# ============================================================================

def get_cache(key: str) -> Optional[Any]:
    """Alias para get - compatibilidade com API"""
    return _cache_instance.get(key)

def set_cache(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """Alias para set - compatibilidade com API"""
    return _cache_instance.set(key, value, ttl)

def clear_cache():
    """Limpa todo o cache"""
    _cache_instance.clear()

def get_cache_stats() -> Dict[str, Any]:
    """Retorna estatísticas do cache"""
    return _cache_instance.get_stats()

# ============================================================================
# FUNÇÕES ORIGINAIS DO MÓDULO
# ============================================================================

def get_cached_data(*args, **kwargs) -> Optional[Any]:
    """
    Obtém dados do cache baseado nos parâmetros
    
    Args:
        *args: Argumentos posicionais
        **kwargs: Argumentos nomeados
        
    Returns:
        Any: Dados em cache ou None
    """
    key = _cache_instance._generate_key(*args, **kwargs)
    return _cache_instance.get(key)

def set_cached_data(value: Any, ttl: Optional[int] = None, *args, **kwargs) -> bool:
    """
    Armazena dados no cache
    
    Args:
        value (Any): Valor a armazenar
        ttl (int, optional): TTL em segundos
        *args: Argumentos posicionais para gerar chave
        **kwargs: Argumentos nomeados para gerar chave
        
    Returns:
        bool: True se armazenado com sucesso
    """
    key = _cache_instance._generate_key(*args, **kwargs)
    return _cache_instance.set(key, value, ttl)

def is_cache_enabled() -> bool:
    """Verifica se o cache está habilitado"""
    return _cache_instance.is_enabled()

def enable_cache():
    """Habilita o cache"""
    _cache_instance.enable()

def disable_cache():
    """Desabilita o cache"""
    _cache_instance.disable() 