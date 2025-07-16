"""
Testes unitários para o sistema de cache
"""
import pytest
import sys
import time
from pathlib import Path

# Adicionar src ao path
current_dir = Path(__file__).parent.parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from src.cache import (
    get_cached_data, set_cached_data, clear_cache,
    get_cache_stats, is_cache_enabled, enable_cache, disable_cache
)

class TestCacheBasic:
    """Testes básicos do cache"""
    
    def test_cache_enabled_by_default(self):
        """Testa se o cache está habilitado por padrão"""
        assert is_cache_enabled() is True
    
    def test_set_and_get_data(self):
        """Testa armazenar e recuperar dados do cache"""
        test_data = {"test": "value", "number": 123}
        
        # Armazenar dados
        result = set_cached_data(test_data, 60, "test_function", "param1", param2="value2")
        assert result is True
        
        # Recuperar dados
        cached_data = get_cached_data("test_function", "param1", param2="value2")
        assert cached_data == test_data
    
    def test_cache_miss(self):
        """Testa quando dados não estão em cache"""
        # Tentar recuperar dados inexistentes
        cached_data = get_cached_data("nonexistent_function", "param1")
        assert cached_data is None
    
    def test_clear_cache(self):
        """Testa limpeza do cache"""
        # Armazenar dados
        set_cached_data("test_value", 60, "test_clear")
        
        # Verificar se está no cache
        assert get_cached_data("test_clear") == "test_value"
        
        # Limpar cache
        clear_cache()
        
        # Verificar se foi removido
        assert get_cached_data("test_clear") is None

class TestCacheTTL:
    """Testes de TTL (Time To Live)"""
    
    def test_cache_expiration(self):
        """Testa expiração do cache"""
        # Armazenar dados com TTL muito baixo
        set_cached_data("expire_test", 1, "expire_function")
        
        # Verificar se está no cache
        assert get_cached_data("expire_function") == "expire_test"
        
        # Aguardar expiração
        time.sleep(2)
        
        # Verificar se expirou
        assert get_cached_data("expire_function") is None
    
    def test_different_ttl_values(self):
        """Testa diferentes valores de TTL"""
        # TTL padrão
        set_cached_data("default_ttl", None, "default_test")
        assert get_cached_data("default_test") == "default_ttl"
        
        # TTL customizado
        set_cached_data("custom_ttl", 10, "custom_test")
        assert get_cached_data("custom_test") == "custom_ttl"

class TestCacheStats:
    """Testes de estatísticas do cache"""
    
    def test_cache_stats_structure(self):
        """Testa estrutura das estatísticas do cache"""
        stats = get_cache_stats()
        
        # Verificar campos obrigatórios
        assert 'hits' in stats
        assert 'misses' in stats
        assert 'sets' in stats
        assert 'evictions' in stats
        assert 'current_size' in stats
        assert 'max_size' in stats
        assert 'hit_rate' in stats
        assert 'enabled' in stats
        assert 'created_at' in stats
    
    def test_cache_stats_accuracy(self):
        """Testa precisão das estatísticas"""
        # Limpar cache para começar limpo
        clear_cache()
        
        # Obter estatísticas iniciais
        initial_stats = get_cache_stats()
        initial_sets = initial_stats['sets']
        initial_hits = initial_stats['hits']
        initial_misses = initial_stats['misses']
        
        # Fazer algumas operações
        set_cached_data("test1", 60, "function1")
        set_cached_data("test2", 60, "function2")
        
        # Recuperar dados (hits)
        get_cached_data("function1")
        get_cached_data("function2")
        
        # Tentar recuperar dados inexistentes (misses)
        get_cached_data("nonexistent")
        get_cached_data("another_nonexistent")
        
        # Obter estatísticas finais
        final_stats = get_cache_stats()
        
        # Verificar se as estatísticas foram atualizadas
        assert final_stats['sets'] >= initial_sets + 2
        assert final_stats['hits'] >= initial_hits + 2
        assert final_stats['misses'] >= initial_misses + 2

class TestCacheEnableDisable:
    """Testes de habilitação/desabilitação do cache"""
    
    def test_disable_cache(self):
        """Testa desabilitação do cache"""
        # Armazenar dados
        set_cached_data("test_disable", 60, "disable_test")
        
        # Desabilitar cache
        disable_cache()
        assert is_cache_enabled() is False
        
        # Tentar recuperar dados (deve falhar)
        cached_data = get_cached_data("disable_test")
        assert cached_data is None
        
        # Tentar armazenar dados (deve falhar)
        result = set_cached_data("new_data", 60, "disable_test2")
        assert result is False
    
    def test_enable_cache(self):
        """Testa habilitação do cache"""
        # Desabilitar cache
        disable_cache()
        assert is_cache_enabled() is False
        
        # Habilitar cache
        enable_cache()
        assert is_cache_enabled() is True
        
        # Testar operações normais
        set_cached_data("test_enable", 60, "enable_test")
        cached_data = get_cached_data("enable_test")
        assert cached_data == "test_enable"

class TestCachePerformance:
    """Testes de performance do cache"""
    
    def test_cache_hit_rate_calculation(self):
        """Testa cálculo da taxa de acerto"""
        clear_cache()
        
        # Fazer algumas operações
        for i in range(5):
            set_cached_data(f"value{i}", 60, f"function{i}")
        
        # Recuperar dados (hits)
        for i in range(5):
            get_cached_data(f"function{i}")
        
        # Tentar recuperar dados inexistentes (misses)
        for i in range(3):
            get_cached_data(f"nonexistent{i}")
        
        stats = get_cache_stats()
        
        # Verificar taxa de acerto
        expected_hit_rate = 5 / (5 + 3)  # 5 hits, 3 misses
        assert abs(stats['hit_rate'] - expected_hit_rate) < 0.01
    
    def test_cache_size_limits(self):
        """Testa limites de tamanho do cache"""
        clear_cache()
        
        # Armazenar muitos dados para testar eviction
        for i in range(1100):  # Mais que o limite padrão de 1000
            set_cached_data(f"value{i}", 60, f"function{i}")
        
        stats = get_cache_stats()
        
        # Verificar se o tamanho não excedeu o limite
        assert stats['current_size'] <= stats['max_size']
        
        # Verificar se houve evictions
        assert stats['evictions'] > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 