# 🔌 Serviços - ConsultaVD Frontend

Esta pasta contém os serviços de integração com APIs e comunicação com o backend do sistema ConsultaVD.

## 📁 Estrutura dos Serviços

### **api.ts** (7.9KB, 230 linhas)
Serviço principal de comunicação com o backend, centralizando todas as chamadas de API.

## 🏗️ Arquitetura do Serviço

### **Configuração Base**
```tsx
import axios from 'axios';

// Configuração do cliente HTTP
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptors para tratamento global
apiClient.interceptors.request.use(
  (config) => {
    // Adicionar headers de autenticação se necessário
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Tratamento global de erros
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);
```

## 📡 Endpoints Implementados

### **Dashboard**
```tsx
// Estatísticas do dashboard
export const getDashboardStats = async (): Promise<DashboardStats> => {
  const response = await apiClient.get('/api/dashboard/stats');
  return response.data;
};
```

### **Busca Unificada**
```tsx
// Busca de lojas
export const searchLojas = async (query: string): Promise<Loja[]> => {
  const response = await apiClient.get(`/api/search/lojas?q=${encodeURIComponent(query)}`);
  return response.data;
};

// Busca de pessoas
export const searchPeople = async (code: string): Promise<Person[]> => {
  const response = await apiClient.get(`/api/search/people?code=${encodeURIComponent(code)}`);
  return response.data;
};

// Busca por ID Vivo
export const searchByIdVivo = async (idVivo: string): Promise<any[]> => {
  const response = await apiClient.get(`/api/search/id-vivo?id_vivo=${encodeURIComponent(idVivo)}`);
  return response.data;
};

// Busca por GGL/GR
export const searchByGglGr = async (gglGr: string): Promise<any[]> => {
  const response = await apiClient.get(`/api/search/ggl-gr?ggl_gr=${encodeURIComponent(gglGr)}`);
  return response.data;
};
```

### **Gestão de Lojas**
```tsx
// Obter operadoras de uma loja
export const getLojaOperadoras = async (lojaId: string): Promise<Operadora[]> => {
  const response = await apiClient.get(`/api/lojas/${lojaId}/operadoras`);
  return response.data;
};

// Obter circuitos de uma operadora
export const getOperadoraCircuitos = async (
  lojaId: string, 
  operadora: string
): Promise<Circuito[]> => {
  const response = await apiClient.get(`/api/lojas/${lojaId}/operadoras/${operadora}/circuitos`);
  return response.data;
};
```

### **Busca Guiada**
```tsx
// Busca específica loja > operadora > circuito
export const searchLojaOperadoraCircuito = async (
  lojaId: string,
  operadora: string,
  circuito: string
): Promise<any> => {
  const response = await apiClient.get(
    `/api/search/loja-operadora-circuito?loja_id=${lojaId}&operadora=${operadora}&circuito=${circuito}`
  );
  return response.data;
};
```

### **Health Check**
```tsx
// Verificar status da API
export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const response = await apiClient.get('/api/health');
    return response.status === 200;
  } catch (error) {
    return false;
  }
};
```

## 🔧 Funcionalidades do Serviço

### **Tratamento de Erros**
```tsx
// Wrapper para tratamento de erros
const handleApiError = (error: any): never => {
  if (error.response) {
    // Erro de resposta do servidor
    const { status, data } = error.response;
    throw new Error(`Erro ${status}: ${data.message || 'Erro desconhecido'}`);
  } else if (error.request) {
    // Erro de rede
    throw new Error('Erro de conexão com o servidor');
  } else {
    // Erro de configuração
    throw new Error('Erro de configuração da requisição');
  }
};

// Uso em funções
export const getData = async () => {
  try {
    const response = await apiClient.get('/api/data');
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};
```

### **Cache e Performance**
```tsx
// Cache simples em memória
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutos

const getCachedData = (key: string) => {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  return null;
};

const setCachedData = (key: string, data: any) => {
  cache.set(key, { data, timestamp: Date.now() });
};

// Função com cache
export const getCachedLojas = async (): Promise<Loja[]> => {
  const cacheKey = 'lojas';
  const cached = getCachedData(cacheKey);
  
  if (cached) {
    return cached;
  }
  
  const data = await getLojas();
  setCachedData(cacheKey, data);
  return data;
};
```

### **Retry Logic**
```tsx
// Função com retry automático
const retryRequest = async (
  requestFn: () => Promise<any>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<any> => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await requestFn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
    }
  }
};

// Uso
export const getDataWithRetry = async () => {
  return retryRequest(() => apiClient.get('/api/data'));
};
```

## 📊 Tipos TypeScript

### **Interfaces de Resposta**
```tsx
interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

interface DashboardStats {
  totalLojas: number;
  lojasAtivas: number;
  lojasInativas: number;
  totalCircuitos: number;
  circuitosAtivos: number;
  circuitosInativos: number;
}

interface Loja {
  id: string;
  nome: string;
  endereco: string;
  cidade: string;
  uf: string;
  status: 'ATIVA' | 'INATIVA' | 'PENDENTE';
  telefone1?: string;
  telefone2?: string;
  email?: string;
}

interface Operadora {
  nome: string;
  circuitos: Circuito[];
}

interface Circuito {
  designacao: string;
  status: string;
  tipo: string;
}
```

## 🎯 Padrões de Uso

### **Hook Customizado**
```tsx
import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const useApiData = <T>(
  apiFunction: () => Promise<T>,
  dependencies: any[] = []
) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await apiFunction();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, dependencies);

  return { data, loading, error, refetch: () => fetchData() };
};

// Uso
const { data: lojas, loading, error } = useApiData(apiService.getLojas);
```

### **Componente com Dados**
```tsx
import React from 'react';
import { useApiData } from '../hooks/useApiData';
import { apiService } from '../services/api';

export const LojasList: React.FC = () => {
  const { data: lojas, loading, error } = useApiData(apiService.getLojas);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!lojas) return <Typography>Nenhuma loja encontrada</Typography>;

  return (
    <div>
      {lojas.map(loja => (
        <LojaCard key={loja.id} loja={loja} />
      ))}
    </div>
  );
};
```

## 🔒 Segurança

### **Headers de Segurança**
```tsx
// Headers adicionais para segurança
apiClient.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
apiClient.defaults.headers.common['X-API-Version'] = '2.0';
```

### **Validação de Dados**
```tsx
// Validação de entrada
const validateSearchQuery = (query: string): boolean => {
  if (!query || query.trim().length < 2) {
    throw new Error('Query deve ter pelo menos 2 caracteres');
  }
  return true;
};

// Uso
export const searchLojas = async (query: string): Promise<Loja[]> => {
  validateSearchQuery(query);
  const response = await apiClient.get(`/api/search/lojas?q=${encodeURIComponent(query)}`);
  return response.data;
};
```

## 🧪 Testes

### **Testes de Serviço**
```tsx
import { renderHook } from '@testing-library/react-hooks';
import { apiService } from '../services/api';

describe('API Service', () => {
  it('should fetch dashboard stats', async () => {
    const { result } = renderHook(() => useApiData(apiService.getDashboardStats));
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });
    
    expect(result.current.data).toBeDefined();
    expect(result.current.error).toBeNull();
  });
});
```

## 📈 Monitoramento

### **Logs de Performance**
```tsx
// Middleware para logging
apiClient.interceptors.request.use(
  (config) => {
    config.metadata = { startTime: new Date() };
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => {
    const duration = new Date().getTime() - response.config.metadata.startTime;
    console.log(`API Call: ${response.config.url} - ${duration}ms`);
    return response;
  },
  (error) => Promise.reject(error)
);
```

---
*Serviços desenvolvidos com Axios e TypeScript*  
*Última atualização: Janeiro 2025* 