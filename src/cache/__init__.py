# Módulo de cache
from .memory_cache import (
    get_cached_data, set_cached_data, clear_cache,
    get_cache_stats, is_cache_enabled, enable_cache, disable_cache
)

__all__ = [
    'get_cached_data',
    'set_cached_data', 
    'clear_cache',
    'get_cache_stats',
    'is_cache_enabled',
    'enable_cache',
    'disable_cache'
] 