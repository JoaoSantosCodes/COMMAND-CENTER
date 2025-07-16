import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  Loja, 
  Circuito, 
  Inventario, 
  DashboardStats, 
  SearchResult, 
  AuditLog,
  ApiResponse,
  PaginatedResponse,
  SearchFilters
} from '../types';

// Configuração base da API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para tratamento de erros
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error);
        return Promise.reject(error);
      }
    );
  }

  // Dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    const response: AxiosResponse<ApiResponse<DashboardStats>> = await this.api.get('/api/dashboard/stats');
    return response.data.data!;
  }

  // Lojas
  async getLojas(filters?: SearchFilters, page = 1, limit = 50): Promise<PaginatedResponse<Loja>> {
    const params = { page, limit, ...filters };
    const response: AxiosResponse<PaginatedResponse<Loja>> = await this.api.get('/api/lojas', { params });
    return response.data;
  }

  async getLoja(id: number): Promise<Loja> {
    const response: AxiosResponse<ApiResponse<Loja>> = await this.api.get(`/api/lojas/${id}`);
    return response.data.data!;
  }

  async createLoja(loja: Partial<Loja>): Promise<Loja> {
    const response: AxiosResponse<ApiResponse<Loja>> = await this.api.post('/api/lojas', loja);
    return response.data.data!;
  }

  async updateLoja(id: number, loja: Partial<Loja>): Promise<Loja> {
    const response: AxiosResponse<ApiResponse<Loja>> = await this.api.put(`/api/lojas/${id}`, loja);
    return response.data.data!;
  }

  async deleteLoja(id: number): Promise<void> {
    await this.api.delete(`/api/lojas/${id}`);
  }

  // Circuitos
  async getCircuitos(filters?: SearchFilters, page = 1, limit = 50): Promise<PaginatedResponse<Circuito>> {
    const params = { page, limit, ...filters };
    const response: AxiosResponse<PaginatedResponse<Circuito>> = await this.api.get('/api/circuitos', { params });
    return response.data;
  }

  async getCircuito(id: number): Promise<Circuito> {
    const response: AxiosResponse<ApiResponse<Circuito>> = await this.api.get(`/api/circuitos/${id}`);
    return response.data.data!;
  }

  async createCircuito(circuito: Partial<Circuito>): Promise<Circuito> {
    const response: AxiosResponse<ApiResponse<Circuito>> = await this.api.post('/api/circuitos', circuito);
    return response.data.data!;
  }

  async updateCircuito(id: number, circuito: Partial<Circuito>): Promise<Circuito> {
    const response: AxiosResponse<ApiResponse<Circuito>> = await this.api.put(`/api/circuitos/${id}`, circuito);
    return response.data.data!;
  }

  async deleteCircuito(id: number): Promise<void> {
    await this.api.delete(`/api/circuitos/${id}`);
  }

  // Inventário
  async getInventario(filters?: SearchFilters, page = 1, limit = 50): Promise<PaginatedResponse<Inventario>> {
    const params = { page, limit, ...filters };
    const response: AxiosResponse<PaginatedResponse<Inventario>> = await this.api.get('/api/inventario', { params });
    return response.data;
  }

  async getInventarioItem(id: number): Promise<Inventario> {
    const response: AxiosResponse<ApiResponse<Inventario>> = await this.api.get(`/api/inventario/${id}`);
    return response.data.data!;
  }

  async createInventarioItem(item: Partial<Inventario>): Promise<Inventario> {
    const response: AxiosResponse<ApiResponse<Inventario>> = await this.api.post('/api/inventario', item);
    return response.data.data!;
  }

  async updateInventarioItem(id: number, item: Partial<Inventario>): Promise<Inventario> {
    const response: AxiosResponse<ApiResponse<Inventario>> = await this.api.put(`/api/inventario/${id}`, item);
    return response.data.data!;
  }

  async deleteInventarioItem(id: number): Promise<void> {
    await this.api.delete(`/api/inventario/${id}`);
  }

  // Busca Unificada
  async unifiedSearch(searchTerm: string): Promise<SearchResult> {
    const response: AxiosResponse<ApiResponse<SearchResult>> = await this.api.get('/api/search/unified', {
      params: { q: searchTerm }
    });
    return response.data.data!;
  }

  async searchByPeople(peopleCode: string): Promise<SearchResult> {
    const response: AxiosResponse<ApiResponse<SearchResult>> = await this.api.get('/api/search/people', {
      params: { code: peopleCode }
    });
    return response.data.data!;
  }

  async searchByDesignation(designation: string): Promise<SearchResult> {
    const response: AxiosResponse<ApiResponse<SearchResult>> = await this.api.get('/api/search/designation', {
      params: { designation }
    });
    return response.data.data!;
  }

  async searchByAddress(address: string): Promise<SearchResult> {
    const response: AxiosResponse<ApiResponse<SearchResult>> = await this.api.get('/api/search/address', {
      params: { address }
    });
    return response.data.data!;
  }

  async searchByIdVivo(idVivo: string): Promise<SearchResult> {
    const response: AxiosResponse<ApiResponse<SearchResult>> = await this.api.get('/api/search/id-vivo', {
      params: { id_vivo: idVivo }
    });
    return response.data.data!;
  }

  async searchByGglGr(gglGr: string): Promise<SearchResult> {
    const response: AxiosResponse<ApiResponse<SearchResult>> = await this.api.get('/api/search/ggl-gr', {
      params: { ggl_gr: gglGr }
    });
    return response.data.data!;
  }

  async searchLojas(searchTerm: string): Promise<ApiResponse<any[]>> {
    const response: AxiosResponse<ApiResponse<any[]>> = await this.api.get('/api/search/lojas', {
      params: { q: searchTerm }
    });
    return response.data;
  }

  async getOperadorasByLoja(lojaId: string): Promise<ApiResponse<string[]>> {
    const response: AxiosResponse<ApiResponse<string[]>> = await this.api.get(`/api/lojas/${lojaId}/operadoras`);
    return response.data;
  }

  async getCircuitosByLojaOperadora(lojaId: string, operadora: string): Promise<ApiResponse<string[]>> {
    const response: AxiosResponse<ApiResponse<string[]>> = await this.api.get(`/api/lojas/${lojaId}/operadoras/${operadora}/circuitos`);
    return response.data;
  }

  async searchByLojaOperadoraCircuito(lojaId: string, operadora: string, circuito: string): Promise<SearchResult> {
    const response: AxiosResponse<ApiResponse<SearchResult>> = await this.api.get('/api/search/loja-operadora-circuito', {
      params: { loja_id: lojaId, operadora, circuito }
    });
    return response.data.data!;
  }

  // Auditoria
  async getAuditLogs(page = 1, limit = 50): Promise<PaginatedResponse<AuditLog>> {
    const response: AxiosResponse<PaginatedResponse<AuditLog>> = await this.api.get('/api/audit/logs', {
      params: { page, limit }
    });
    return response.data;
  }

  // Cache
  async getCacheStats(): Promise<any> {
    const response: AxiosResponse<ApiResponse<any>> = await this.api.get('/api/cache/stats');
    return response.data.data!;
  }

  async clearCache(): Promise<void> {
    await this.api.post('/api/cache/clear');
  }

  // Export
  async exportData(table: string, format: 'csv' | 'excel' = 'csv'): Promise<Blob> {
    const response = await this.api.get(`/api/export/${table}`, {
      params: { format },
      responseType: 'blob'
    });
    return response.data;
  }

  async exportSearchResults(results: any[], searchType: string, filters: any = {}): Promise<Blob> {
    const response = await this.api.post('/api/export/search-results', {
      results,
      searchType,
      filters
    }, {
      responseType: 'blob'
    });
    return response.data;
  }

  // Health Check
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.api.get('/api/health');
      return response.status === 200;
    } catch {
      return false;
    }
  }

  // SQL Customizado
  async executeSQL(query: string): Promise<{ columns: string[], data: any[] }> {
    const response = await this.api.post('/api/sql/execute', { query });
    return response.data;
  }

  // Templates
  async getTemplates(tipo?: string): Promise<any[]> {
    const response = await this.api.get('/api/templates', { params: tipo ? { tipo } : {} });
    return response.data;
  }

  async createTemplate(data: { tipo: string; nome: string; conteudo: any }): Promise<any> {
    const response = await this.api.post('/api/templates', data);
    return response.data;
  }

  async deleteTemplate(id: number): Promise<void> {
    await this.api.delete(`/api/templates/${id}`);
  }
}

// Instância singleton
export const apiService = new ApiService();
export default apiService; 