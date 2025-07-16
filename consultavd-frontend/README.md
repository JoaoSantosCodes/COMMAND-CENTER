# 🚀 ConsultaVD Frontend - React/TypeScript

Frontend moderno para o sistema ConsultaVD, desenvolvido com React, TypeScript e Material-UI. Interface responsiva e intuitiva para consulta, edição e auditoria de dados de lojas, circuitos e operadoras.

## 🛠️ Tecnologias Utilizadas

- **React 18** - Biblioteca de interface moderna
- **TypeScript** - Tipagem estática para segurança
- **Material-UI (MUI)** - Componentes visuais profissionais
- **Axios** - Cliente HTTP para APIs
- **Recharts** - Gráficos e visualizações interativas
- **React Router** - Navegação entre páginas
- **React Query** - Gerenciamento de estado e cache

## 📦 Estrutura Detalhada do Projeto

```
consultavd-frontend/
├── 📁 src/                          # Código fonte principal
│   ├── 📁 components/               # Componentes reutilizáveis
│   │   ├── 📁 LojaDetalheCard/      # Componentes de detalhes de loja
│   │   │   ├── index.tsx           # Componente principal
│   │   │   ├── Titulo.tsx          # Título e informações básicas
│   │   │   ├── Endereco.tsx        # Dados de endereço
│   │   │   ├── Contatos.tsx        # Informações de contato
│   │   │   ├── Funcionamento.tsx   # Horários de funcionamento
│   │   │   ├── Gestores.tsx        # Dados dos gestores
│   │   │   └── StatusExtra.tsx     # Status e informações extras
│   │   ├── DashboardCard.tsx       # Cards de métricas do dashboard
│   │   ├── DataTable.tsx           # Tabela de dados com paginação
│   │   ├── PeopleCard.tsx          # Card de informações de pessoas
│   │   ├── PeopleContactCard.tsx   # Card de contatos de pessoas
│   │   ├── CarimboGenerator.tsx    # Gerador de carimbos
│   │   └── Sidebar.tsx             # Barra lateral de navegação
│   ├── 📁 pages/                   # Páginas da aplicação
│   │   ├── Dashboard.tsx           # Página principal com métricas
│   │   ├── BuscaUnificada.tsx      # Busca em múltiplas tabelas
│   │   ├── Lojas.tsx               # Gestão de lojas
│   │   └── Avancados.tsx           # Funcionalidades avançadas
│   ├── 📁 services/                # Serviços de integração
│   │   └── api.ts                  # Cliente da API backend
│   ├── 📁 types/                   # Definições TypeScript
│   │   └── index.ts                # Tipos centralizados
│   ├── 📁 hooks/                   # Custom hooks
│   ├── 📁 utils/                   # Funções utilitárias
│   ├── App.tsx                     # Componente raiz da aplicação
│   ├── index.tsx                   # Ponto de entrada
│   └── ThemeProvider.tsx           # Provedor de tema Material-UI
├── 📁 public/                      # Arquivos estáticos
│   ├── index.html                  # HTML base
│   └── manifest.json               # Manifesto PWA
├── 📁 build/                       # Build de produção (gerado)
├── 📁 node_modules/                # Dependências (gerado)
├── package.json                    # Configurações e dependências
├── package-lock.json               # Lock de versões
├── tsconfig.json                   # Configuração TypeScript
├── start_system.bat                # Script de inicialização
└── README.md                       # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos
- **Node.js 16+** 
- **npm ou yarn**
- **Backend Python** rodando em `http://localhost:8000`

### Instalação e Execução

1. **Instalar dependências:**
```bash
npm install
```

2. **Executar em modo desenvolvimento:**
```bash
npm start
```

3. **Acessar a aplicação:**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs

### Script de Inicialização Rápida
```bash
# Windows
start_system.bat

# Linux/Mac
./start_system.sh
```

## 📋 Scripts Disponíveis

```bash
npm start          # Executa em modo desenvolvimento
npm run build      # Gera build de produção
npm test           # Executa testes
npm run eject      # Ejecta configurações (irreversível)
npm run lint       # Executa linting
npm run format     # Formata código
```

## 🎨 Componentes Principais

### DashboardCard
Card moderno para métricas e destaques:
```tsx
<DashboardCard
  title="Total de Lojas"
  value="123"
  icon="🏪"
  color="primary"
  trend={{ value: 5, isPositive: true }}
/>
```

### DataTable
Tabela de dados com paginação e filtros:
```tsx
<DataTable
  rows={lojas}
  columns={columns}
  loading={loading}
  onEdit={handleEdit}
  onDelete={handleDelete}
  pagination={pagination}
/>
```

### LojaDetalheCard
Componente modular para exibição detalhada de lojas:
```tsx
<LojaDetalheCard
  loja={lojaData}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

### PeopleCard
Card para informações de pessoas:
```tsx
<PeopleCard
  person={personData}
  showContact={true}
  onContact={handleContact}
/>
```

## 🔌 Integração com API

O frontend se comunica com o backend através do serviço `api.ts`:

```tsx
import { apiService } from '../services/api';

// Buscar lojas
const lojas = await apiService.getLojas();

// Busca unificada
const resultados = await apiService.searchUnified(query);

// Dashboard stats
const stats = await apiService.getDashboardStats();

// Operadoras de uma loja
const operadoras = await apiService.getLojaOperadoras(lojaId);
```

### Endpoints Principais
- `GET /api/dashboard/stats` - Estatísticas do dashboard
- `GET /api/search/lojas` - Busca de lojas
- `GET /api/search/people` - Busca de pessoas
- `GET /api/lojas/{id}/operadoras` - Operadoras de uma loja
- `GET /api/search/loja-operadora-circuito` - Busca guiada

## 📊 Tipos TypeScript

Todos os tipos estão definidos em `src/types/index.ts`:

```tsx
interface Loja {
  id: number;
  nome: string;
  endereco: string;
  cidade: string;
  uf: string;
  status: 'ATIVA' | 'INATIVA' | 'PENDENTE';
  telefone1?: string;
  telefone2?: string;
  email?: string;
  horario_funcionamento?: string;
  gestor?: string;
}

interface DashboardStats {
  totalLojas: number;
  lojasAtivas: number;
  lojasInativas: number;
  totalCircuitos: number;
  circuitosAtivos: number;
  circuitosInativos: number;
}

interface SearchResult {
  tipo: 'loja' | 'pessoa' | 'circuito';
  dados: any;
  score: number;
}
```

## 🎯 Funcionalidades por Página

### 📊 Dashboard
- ✅ Métricas em tempo real
- ✅ Gráficos interativos
- ✅ Cards de destaque
- ✅ Resumo de atividades

### 🔍 Busca Unificada
- ✅ Busca em múltiplas tabelas
- ✅ Filtros avançados
- ✅ Resultados paginados
- ✅ Exportação de dados
- ✅ Busca por Enter key

### 🏪 Gestão de Lojas
- ✅ Listagem de lojas
- ✅ Detalhes completos
- ✅ Edição inline
- ✅ Filtros por status/região

### ⚙️ Funcionalidades Avançadas
- ✅ Geração de carimbos
- ✅ Relatórios customizados
- ✅ Configurações avançadas

## 🔧 Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
REACT_APP_VERSION=2.0.0
```

### Proxy
O projeto está configurado para fazer proxy das requisições para `http://localhost:8000` (backend).

### Tema Material-UI
O tema é configurado em `ThemeProvider.tsx` com suporte a:
- Modo claro/escuro
- Cores personalizadas
- Tipografia customizada
- Componentes responsivos

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:
- **Desktop** (1200px+) - Layout completo
- **Tablet** (768px - 1199px) - Layout adaptado
- **Mobile** (< 768px) - Layout mobile-first

### Breakpoints
```tsx
xs: 0px      // Mobile
sm: 600px    // Tablet pequeno
md: 900px    // Tablet
lg: 1200px   // Desktop
xl: 1536px   // Desktop grande
```

## 🧪 Testes

```bash
# Executar testes
npm test

# Executar testes com coverage
npm test -- --coverage

# Executar testes em modo watch
npm test -- --watch
```

## 🏗️ Build de Produção

```bash
# Gerar build otimizado
npm run build

# Os arquivos serão gerados em build/
# Inclui:
# - JavaScript minificado
# - CSS otimizado
# - Assets comprimidos
# - Service worker (PWA)
```

## 🔄 Desenvolvimento

### Estrutura de Commits
```
feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação
refactor: refatoração
test: testes
chore: tarefas de build
```

### Padrões de Código
- **TypeScript strict mode**
- **ESLint + Prettier**
- **Componentes funcionais** com hooks
- **Props tipadas**
- **Tratamento de erros**
- **Nomenclatura consistente**

### Estrutura de Componentes
```tsx
// Componente padrão
interface ComponentProps {
  // Props tipadas
}

export const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Hooks
  // Lógica
  // Render
  return <div>...</div>;
};
```

## 🚀 Deploy

### Build para Produção
```bash
npm run build
```

### Servir Build Localmente
```bash
npx serve -s build
```

### Deploy em Servidor
1. Execute `npm run build`
2. Copie a pasta `build/` para o servidor
3. Configure o servidor web (nginx, Apache, etc.)
4. Configure proxy para API backend

## 📞 Suporte e Troubleshooting

### Problemas Comuns
1. **Erro de CORS**: Verifique se o backend está rodando
2. **Erro de build**: Limpe cache com `npm run build -- --reset-cache`
3. **Dependências**: Delete `node_modules` e execute `npm install`

### Logs de Desenvolvimento
- Console do navegador para erros de frontend
- Network tab para requisições de API
- React DevTools para debugging de componentes

---
*Frontend desenvolvido com React 18, TypeScript e Material-UI*  
*Versão: 2.0.0 - Janeiro 2025* 