# 📝 Tipos - ConsultaVD Frontend

Esta pasta contém todas as definições TypeScript do sistema ConsultaVD, centralizando os tipos, interfaces e enums utilizados em toda a aplicação.

## 📁 Estrutura dos Tipos

### **index.ts** (2.9KB, 140 linhas)
Arquivo principal contendo todas as definições de tipos do sistema.

## 🏗️ Categorias de Tipos

### **🏪 Tipos de Lojas**
```tsx
// Interface principal de loja
interface Loja {
  id: string;
  codigo: string;
  nome: string;
  endereco: string;
  bairro: string;
  cidade: string;
  uf: string;
  cep: string;
  telefone1?: string;
  telefone2?: string;
  celular?: string;
  email?: string;
  horario_funcionamento?: string;
  sabado?: string;
  domingo?: string;
  funcionario?: string;
  vd_novo?: string;
  gestor?: string;
  gerente?: string;
  status: LojaStatus;
  created_at?: string;
  updated_at?: string;
}

// Status de loja
type LojaStatus = 'ATIVA' | 'INATIVA' | 'PENDENTE' | 'EM_MANUTENCAO';

// Filtros para busca de lojas
interface LojaFilters {
  status?: LojaStatus;
  uf?: string;
  cidade?: string;
  gestor?: string;
}
```

### **👥 Tipos de Pessoas**
```tsx
// Interface de pessoa
interface Person {
  id: string;
  codigo: string;
  nome: string;
  funcao?: string;
  telefone?: string;
  email?: string;
  loja_id?: string;
  status: PersonStatus;
}

// Status de pessoa
type PersonStatus = 'ATIVO' | 'INATIVO' | 'AFASTADO';

// Contatos de pessoa
interface PersonContact {
  id: string;
  person_id: string;
  tipo: ContactType;
  valor: string;
  principal: boolean;
}

// Tipos de contato
type ContactType = 'TELEFONE' | 'EMAIL' | 'WHATSAPP' | 'CELULAR';
```

### **🔌 Tipos de Circuitos**
```tsx
// Interface de circuito
interface Circuito {
  id: string;
  designacao: string;
  operadora: string;
  tipo: string;
  velocidade?: string;
  status: CircuitoStatus;
  loja_id: string;
  created_at?: string;
  updated_at?: string;
}

// Status de circuito
type CircuitoStatus = 'ATIVO' | 'INATIVO' | 'EM_MANUTENCAO' | 'SUSPENSO';

// Operadora
interface Operadora {
  nome: string;
  circuitos: Circuito[];
  total_circuitos: number;
  circuitos_ativos: number;
}
```

### **📊 Tipos de Dashboard**
```tsx
// Estatísticas do dashboard
interface DashboardStats {
  total_lojas: number;
  lojas_ativas: number;
  lojas_inativas: number;
  total_circuitos: number;
  circuitos_ativos: number;
  circuitos_inativos: number;
  total_operadoras: number;
  operadoras_ativas: number;
}

// Card de métrica
interface MetricCard {
  title: string;
  value: number | string;
  icon: string;
  color: 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info';
  trend?: {
    value: number;
    isPositive: boolean;
  };
}
```

### **🔍 Tipos de Busca**
```tsx
// Resultado de busca unificada
interface SearchResult {
  tipo: 'loja' | 'pessoa' | 'circuito' | 'operadora';
  dados: Loja | Person | Circuito | Operadora;
  score: number;
  highlights?: string[];
}

// Parâmetros de busca
interface SearchParams {
  query: string;
  tipo?: SearchType;
  status?: string;
  uf?: string;
  cidade?: string;
  page?: number;
  limit?: number;
}

// Tipos de busca
type SearchType = 'lojas' | 'pessoas' | 'circuitos' | 'operadoras' | 'todos';

// Filtros de busca
interface SearchFilters {
  status?: string[];
  uf?: string[];
  cidade?: string[];
  operadora?: string[];
  tipo_circuito?: string[];
}
```

### **📋 Tipos de Tabelas**
```tsx
// Coluna de tabela
interface TableColumn {
  id: string;
  label: string;
  minWidth?: number;
  align?: 'left' | 'right' | 'center';
  format?: (value: any) => string;
  sortable?: boolean;
  filterable?: boolean;
}

// Configuração de paginação
interface PaginationConfig {
  page: number;
  rowsPerPage: number;
  totalRows: number;
  totalPages: number;
}

// Configuração de ordenação
interface SortConfig {
  field: string;
  direction: 'asc' | 'desc';
}
```

### **🏷️ Tipos de Carimbos**
```tsx
// Dados para geração de carimbo
interface CarimboData {
  sintoma: string;
  abrangencia: string;
  impacto: string;
  descricao_impacto: string;
  horario_inicio: string;
  horario_termino: string;
  status: CarimboStatus;
}

// Status de carimbo
type CarimboStatus = 'INCIDENTE' | 'MANUTENCAO' | 'MELHORIA' | 'INFORMATIVO';

// Carimbo gerado
interface Carimbo {
  id: string;
  texto: string;
  data_criacao: string;
  criado_por: string;
  tipo: CarimboStatus;
}
```

### **🔧 Tipos de Configuração**
```tsx
// Configurações da aplicação
interface AppConfig {
  apiUrl: string;
  environment: 'development' | 'staging' | 'production';
  version: string;
  features: {
    darkMode: boolean;
    notifications: boolean;
    export: boolean;
    advancedSearch: boolean;
  };
}

// Configurações de tema
interface ThemeConfig {
  mode: 'light' | 'dark';
  primaryColor: string;
  secondaryColor: string;
  fontSize: 'small' | 'medium' | 'large';
}
```

## 🎯 Padrões de Nomenclatura

### **Convenções**
- **PascalCase** para interfaces e tipos
- **camelCase** para propriedades
- **UPPER_CASE** para constantes e enums
- **Sufixos descritivos**: `Status`, `Config`, `Data`, `Result`

### **Exemplos**
```tsx
// ✅ Boas práticas
interface LojaData { ... }
type LojaStatus = 'ATIVA' | 'INATIVA';
interface SearchResult { ... }
type ContactType = 'EMAIL' | 'PHONE';

// ❌ Evitar
interface loja { ... }
type status = string;
interface result { ... }
```

## 🔄 Reutilização de Tipos

### **Tipos Utilitários**
```tsx
// Tipo para tornar propriedades opcionais
type PartialLoja = Partial<Loja>;

// Tipo para tornar propriedades obrigatórias
type RequiredLoja = Required<Loja>;

// Tipo para selecionar propriedades específicas
type LojaBasic = Pick<Loja, 'id' | 'nome' | 'cidade' | 'status'>;

// Tipo para omitir propriedades
type LojaWithoutId = Omit<Loja, 'id' | 'created_at' | 'updated_at'>;

// Tipo para união de tipos
type Entity = Loja | Person | Circuito;

// Tipo para chaves de objeto
type LojaKeys = keyof Loja;
```

### **Tipos Condicionais**
```tsx
// Tipo condicional baseado em propriedade
type LojaWithContacts = Loja & {
  contatos: PersonContact[];
};

// Tipo baseado em status
type ActiveLoja = Loja & {
  status: 'ATIVA';
};

// Tipo para formulários
type LojaFormData = Omit<Loja, 'id' | 'created_at' | 'updated_at'>;
```

## 🧪 Validação de Tipos

### **Type Guards**
```tsx
// Verificar se é loja
export const isLoja = (entity: Entity): entity is Loja => {
  return 'codigo' in entity && 'nome' in entity && 'cidade' in entity;
};

// Verificar se é pessoa
export const isPerson = (entity: Entity): entity is Person => {
  return 'codigo' in entity && 'nome' in entity && 'funcao' in entity;
};

// Verificar se é circuito
export const isCircuito = (entity: Entity): entity is Circuito => {
  return 'designacao' in entity && 'operadora' in entity;
};

// Uso
const processEntity = (entity: Entity) => {
  if (isLoja(entity)) {
    // TypeScript sabe que é Loja
    console.log(entity.cidade);
  } else if (isPerson(entity)) {
    // TypeScript sabe que é Person
    console.log(entity.funcao);
  }
};
```

### **Validação de Dados**
```tsx
// Validar loja
export const validateLoja = (data: any): Loja => {
  if (!data.id || !data.nome || !data.cidade) {
    throw new Error('Dados de loja inválidos');
  }
  
  return {
    id: data.id,
    nome: data.nome,
    cidade: data.cidade,
    // ... outras propriedades
  } as Loja;
};

// Validar busca
export const validateSearchParams = (params: any): SearchParams => {
  if (!params.query || params.query.trim().length < 2) {
    throw new Error('Query deve ter pelo menos 2 caracteres');
  }
  
  return {
    query: params.query.trim(),
    tipo: params.tipo || 'todos',
    page: params.page || 1,
    limit: params.limit || 10,
  };
};
```

## 📚 Documentação de Tipos

### **JSDoc para Tipos Complexos**
```tsx
/**
 * Interface principal para representar uma loja no sistema
 * @interface Loja
 * @property {string} id - Identificador único da loja
 * @property {string} codigo - Código da loja (ex: L1234)
 * @property {string} nome - Nome da loja
 * @property {string} endereco - Endereço completo
 * @property {string} cidade - Cidade da loja
 * @property {string} uf - Estado (UF) da loja
 * @property {LojaStatus} status - Status atual da loja
 * @property {string} [telefone1] - Telefone principal (opcional)
 * @property {string} [email] - Email de contato (opcional)
 */
interface Loja {
  id: string;
  codigo: string;
  nome: string;
  endereco: string;
  cidade: string;
  uf: string;
  status: LojaStatus;
  telefone1?: string;
  email?: string;
}
```

## 🔧 Configuração TypeScript

### **tsconfig.json**
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true
  }
}
```

## 🧪 Testes de Tipos

### **Testes com TypeScript**
```tsx
// Teste de tipo
const testLoja: Loja = {
  id: '1',
  codigo: 'L1234',
  nome: 'Loja Teste',
  endereco: 'Rua Teste, 123',
  cidade: 'São Paulo',
  uf: 'SP',
  status: 'ATIVA'
};

// Verificar se o tipo está correto
type TestLojaType = typeof testLoja;
type IsLoja = TestLojaType extends Loja ? true : false;
```

---
*Tipos desenvolvidos com TypeScript strict mode*  
*Última atualização: Janeiro 2025* 