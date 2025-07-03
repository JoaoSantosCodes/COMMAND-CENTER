// Tipos principais do sistema ConsultaVD

export interface Loja {
  id: number;
  nome: string;
  endereco: string;
  cidade: string;
  uf: string;
  status: 'ATIVA' | 'INATIVA' | 'PENDENTE';
  people_code?: string;
  peop_code?: string;
  ggl?: string;
  gr?: string;
  created_at: string;
  updated_at: string;
}

export interface Circuito {
  id: number;
  designacao: string;
  operadora: string;
  tipo: string;
  status: 'ATIVO' | 'INATIVO' | 'MANUTENCAO';
  loja_id: number;
  created_at: string;
  updated_at: string;
}

export interface Inventario {
  id: number;
  loja_id: number;
  equipamento: string;
  modelo: string;
  serial: string;
  status: 'FUNCIONANDO' | 'DEFEITO' | 'MANUTENCAO';
  created_at: string;
  updated_at: string;
}

export interface DashboardStats {
  total_lojas: number;
  total_circuitos: number;
  lojas_por_status: Record<string, number>;
  circuitos_por_operadora: Record<string, number>;
  lojas_por_uf: Record<string, number>;
}

export interface SearchResult {
  lojas: Loja[];
  circuitos: Circuito[];
  inventario: Inventario[];
}

export interface AuditLog {
  id: number;
  table_name: string;
  record_id: number;
  action: 'CREATE' | 'UPDATE' | 'DELETE';
  old_values?: Record<string, any>;
  new_values?: Record<string, any>;
  user_id?: string;
  timestamp: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface SearchFilters {
  status?: string;
  uf?: string;
  operadora?: string;
  search_term?: string;
}

export interface PaginationParams {
  page: number;
  limit: number;
  total: number;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: PaginationParams;
}

// Tipos para formulários
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'select' | 'number' | 'date' | 'textarea';
  required?: boolean;
  options?: { value: string; label: string }[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
  };
}

// Tipos para componentes de UI
export interface CardProps {
  title: string;
  value: string | number;
  icon?: string;
  color?: 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info';
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

import { GridRenderCellParams } from '@mui/x-data-grid';

export interface TableColumn {
  field: string;
  headerName: string;
  width?: number;
  sortable?: boolean;
  filterable?: boolean;
  renderCell?: (params: GridRenderCellParams) => React.ReactNode;
}

// Tipos para cache
export interface CacheStats {
  hits: number;
  misses: number;
  size: number;
  keys: string[];
}

// Tipos para configurações
export interface AppConfig {
  api_url: string;
  environment: 'development' | 'production';
  debug: boolean;
  version: string;
} 