# 📄 Páginas - ConsultaVD Frontend

Esta pasta contém as páginas principais da aplicação ConsultaVD, cada uma responsável por uma funcionalidade específica do sistema.

## 📁 Estrutura das Páginas

### 📊 **Dashboard.tsx** (7.7KB, 246 linhas)
Página principal do sistema com métricas, gráficos e visão geral dos dados.

**Funcionalidades:**
- ✅ Cards de métricas principais (lojas, circuitos, operadoras)
- ✅ Gráficos interativos de tendências
- ✅ Resumo de atividades recentes
- ✅ Links rápidos para funcionalidades
- ✅ Atualização em tempo real
- ✅ Responsividade completa

**Componentes Utilizados:**
- `DashboardCard` - Cards de métricas
- `Recharts` - Gráficos interativos
- `Material-UI Grid` - Layout responsivo

**API Endpoints:**
- `GET /api/dashboard/stats` - Estatísticas do dashboard

**Uso:**
```tsx
// Acesso via rota
<Route path="/" element={<Dashboard />} />

// Navegação programática
navigate('/');
```

### 🔍 **BuscaUnificada.tsx** (13KB, 398 linhas)
Página de busca avançada que permite consultar dados em múltiplas tabelas simultaneamente.

**Funcionalidades:**
- ✅ Busca unificada em lojas, pessoas, circuitos
- ✅ Filtros avançados por tipo, status, região
- ✅ Resultados paginados e ordenáveis
- ✅ Exportação de resultados (CSV/Excel)
- ✅ Busca por Enter key
- ✅ Histórico de buscas
- ✅ Resultados em tempo real

**Tipos de Busca:**
- **Lojas**: Por código, nome, endereço, cidade
- **Pessoas**: Por código, nome, função
- **Circuitos**: Por designação, operadora, status
- **ID Vivo**: Busca específica por ID Vivo

**Componentes Utilizados:**
- `DataTable` - Tabela de resultados
- `TextField` - Campo de busca
- `Autocomplete` - Filtros avançados
- `Button` - Ações de exportação

**API Endpoints:**
- `GET /api/search/lojas` - Busca de lojas
- `GET /api/search/people` - Busca de pessoas
- `GET /api/search/id-vivo` - Busca por ID Vivo
- `GET /api/search/ggl-gr` - Busca por GGL/GR

**Uso:**
```tsx
// Acesso via rota
<Route path="/busca" element={<BuscaUnificada />} />

// Navegação com parâmetros
navigate('/busca?q=loja123');
```

### 🏪 **Lojas.tsx** (1.6KB, 42 linhas)
Página de gestão e visualização de lojas com funcionalidades de CRUD.

**Funcionalidades:**
- ✅ Listagem de todas as lojas
- ✅ Filtros por status e região
- ✅ Visualização de detalhes
- ✅ Navegação para busca guiada
- ✅ Integração com dashboard

**Componentes Utilizados:**
- `DataTable` - Lista de lojas
- `LojaDetalheCard` - Detalhes de loja
- `Sidebar` - Navegação

**API Endpoints:**
- `GET /api/lojas` - Lista de lojas
- `GET /api/lojas/{id}` - Detalhes de loja

**Uso:**
```tsx
// Acesso via rota
<Route path="/lojas" element={<Lojas />} />

// Navegação
navigate('/lojas');
```

### ⚙️ **Avancados.tsx** (1.7KB, 41 linhas)
Página para funcionalidades avançadas e configurações do sistema.

**Funcionalidades:**
- ✅ Geração de carimbos
- ✅ Relatórios customizados
- ✅ Configurações avançadas
- ✅ Ferramentas de administração
- ✅ Logs e auditoria

**Componentes Utilizados:**
- `CarimboGenerator` - Gerador de carimbos
- `DataTable` - Visualização de logs
- `Form` - Configurações

**API Endpoints:**
- `POST /api/stamps/generate` - Geração de carimbos
- `GET /api/logs` - Logs de auditoria
- `GET /api/config` - Configurações

**Uso:**
```tsx
// Acesso via rota
<Route path="/avancados" element={<Avancados />} />

// Navegação
navigate('/avancados');
```

## 🎯 Padrões de Implementação

### **Estrutura Padrão de Página**
```tsx
import React, { useState, useEffect } from 'react';
import { Container, Typography, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';

interface PageProps {
  // Props específicas da página
}

export const Page: React.FC<PageProps> = (props) => {
  // Estados
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Hooks
  const navigate = useNavigate();

  // Efeitos
  useEffect(() => {
    loadData();
  }, []);

  // Funções
  const loadData = async () => {
    setLoading(true);
    try {
      const result = await apiService.getData();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Render
  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        Título da Página
      </Typography>
      
      {loading && <CircularProgress />}
      {error && <Alert severity="error">{error}</Alert>}
      
      <Box>
        {/* Conteúdo da página */}
      </Box>
    </Container>
  );
};
```

### **Gerenciamento de Estado**
- **useState** para estado local
- **useEffect** para efeitos colaterais
- **useNavigate** para navegação
- **Context API** para estado global (quando necessário)

### **Tratamento de Erros**
- Try/catch em operações assíncronas
- Estados de loading e error
- Feedback visual para o usuário
- Logs de erro para debugging

### **Responsividade**
- Container com maxWidth
- Grid system do Material-UI
- Breakpoints consistentes
- Mobile-first approach

## 🔄 Navegação entre Páginas

### **Rotas Definidas**
```tsx
// App.tsx
<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/busca" element={<BuscaUnificada />} />
  <Route path="/lojas" element={<Lojas />} />
  <Route path="/avancados" element={<Avancados />} />
</Routes>
```

### **Navegação Programática**
```tsx
const navigate = useNavigate();

// Navegação simples
navigate('/busca');

// Navegação com parâmetros
navigate('/busca?q=termo&tipo=loja');

// Navegação com estado
navigate('/lojas', { state: { selectedLoja: lojaId } });
```

## 📱 Responsividade

### **Breakpoints Utilizados**
- **xs** (0px): Mobile
- **sm** (600px): Tablet pequeno
- **md** (900px): Tablet
- **lg** (1200px): Desktop
- **xl** (1536px): Desktop grande

### **Adaptações por Página**
- **Dashboard**: Cards empilhados em mobile
- **BuscaUnificada**: Filtros colapsados em mobile
- **Lojas**: Tabela com scroll horizontal
- **Avancados**: Formulários em coluna única

## 🧪 Testes de Páginas

### **Testes de Renderização**
```tsx
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Dashboard } from './Dashboard';

describe('Dashboard', () => {
  it('should render dashboard title', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
  });
});
```

### **Testes de Integração**
- Carregamento de dados
- Interações do usuário
- Navegação entre páginas
- Tratamento de erros

## 📚 Documentação Adicional

### **Componentes Relacionados**
- Ver `src/components/README.md` para detalhes dos componentes
- Ver `src/services/README.md` para integração com APIs
- Ver `src/types/README.md` para definições TypeScript

### **Padrões de Design**
- Material-UI Design System
- Responsive Design
- Accessibility (a11y)
- Performance Optimization

---
*Páginas desenvolvidas com React, TypeScript e Material-UI*  
*Última atualização: Janeiro 2025* 