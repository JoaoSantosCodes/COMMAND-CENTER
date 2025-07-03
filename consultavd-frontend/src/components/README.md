# 🧩 Componentes - ConsultaVD Frontend

Esta pasta contém todos os componentes reutilizáveis do sistema ConsultaVD, organizados por funcionalidade e responsabilidade.

## 📁 Estrutura dos Componentes

### 🏪 **LojaDetalheCard/** - Componentes de Detalhes de Loja
Pasta modular contendo componentes específicos para exibição detalhada de informações de lojas:

- **`index.tsx`** (3.0KB) - Componente principal que orquestra todos os sub-componentes
- **`Titulo.tsx`** (1.4KB) - Título da loja e informações básicas (código, status)
- **`Endereco.tsx`** (979B) - Dados completos de endereço (rua, bairro, cidade, UF, CEP)
- **`Contatos.tsx`** (1.1KB) - Informações de contato (telefones, email)
- **`Funcionamento.tsx`** (976B) - Horários de funcionamento (dias da semana)
- **`Gestores.tsx`** (744B) - Dados dos gestores responsáveis pela loja
- **`StatusExtra.tsx`** (687B) - Status adicional e informações extras

**Uso:**
```tsx
<LojaDetalheCard
  loja={lojaData}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

### 📊 **DashboardCard.tsx** (2.3KB)
Card moderno para exibição de métricas e estatísticas no dashboard.

**Props:**
- `title`: Título do card
- `value`: Valor principal
- `icon`: Ícone (emoji ou Material-UI icon)
- `color`: Cor do tema (primary, secondary, error, etc.)
- `trend`: Dados de tendência (opcional)

**Uso:**
```tsx
<DashboardCard
  title="Total de Lojas"
  value="123"
  icon="🏪"
  color="primary"
  trend={{ value: 5, isPositive: true }}
/>
```

### 📋 **DataTable.tsx** (5.5KB)
Tabela de dados avançada com paginação, filtros, ordenação e ações.

**Funcionalidades:**
- Paginação automática
- Filtros por coluna
- Ordenação por múltiplas colunas
- Ações inline (editar, excluir)
- Loading states
- Seleção de linhas
- Exportação de dados

**Uso:**
```tsx
<DataTable
  rows={lojas}
  columns={columns}
  loading={loading}
  onEdit={handleEdit}
  onDelete={handleDelete}
  pagination={pagination}
  onSelectionChange={handleSelection}
/>
```

### 👥 **PeopleCard.tsx** (4.1KB)
Card para exibição de informações de pessoas (gestores, contatos).

**Funcionalidades:**
- Informações básicas da pessoa
- Status e indicadores
- Ações rápidas
- Integração com contatos

**Uso:**
```tsx
<PeopleCard
  person={personData}
  showActions={true}
  onContact={handleContact}
  onEdit={handleEdit}
/>
```

### 📞 **PeopleContactCard.tsx** (6.7KB)
Card especializado para informações de contato de pessoas.

**Funcionalidades:**
- Múltiplos tipos de contato
- Validação de dados
- Ações de contato direto
- Histórico de interações

**Uso:**
```tsx
<PeopleContactCard
  contacts={contactData}
  onCall={handleCall}
  onEmail={handleEmail}
  onWhatsApp={handleWhatsApp}
/>
```

### 🏷️ **CarimboGenerator.tsx** (2.4KB)
Gerador de carimbos e informativos para incidentes e comunicações.

**Funcionalidades:**
- Templates de carimbos
- Validação de dados
- Preview em tempo real
- Exportação de carimbos

**Uso:**
```tsx
<CarimboGenerator
  incidentData={incident}
  onGenerate={handleGenerate}
  onPreview={handlePreview}
/>
```

### 🧭 **Sidebar.tsx** (3.1KB)
Barra lateral de navegação principal do sistema.

**Funcionalidades:**
- Menu de navegação
- Indicadores de status
- Acesso rápido
- Responsividade

**Uso:**
```tsx
<Sidebar
  currentPage={currentPage}
  onNavigate={handleNavigate}
  user={userData}
/>
```

## 🎨 Padrões de Design

### **Material-UI Integration**
Todos os componentes utilizam Material-UI para:
- Consistência visual
- Responsividade
- Acessibilidade
- Temas personalizados

### **TypeScript**
- Props tipadas
- Interfaces bem definidas
- Type safety
- IntelliSense completo

### **Responsividade**
- Mobile-first design
- Breakpoints consistentes
- Adaptação automática
- Touch-friendly

## 🔧 Desenvolvimento de Novos Componentes

### **Estrutura Padrão**
```tsx
import React from 'react';
import { Box, Typography } from '@mui/material';

interface ComponentProps {
  // Props tipadas
  title: string;
  data: any;
  onAction?: (data: any) => void;
}

export const Component: React.FC<ComponentProps> = ({
  title,
  data,
  onAction
}) => {
  // Hooks e lógica
  const handleAction = () => {
    onAction?.(data);
  };

  // Render
  return (
    <Box>
      <Typography variant="h6">{title}</Typography>
      {/* Conteúdo do componente */}
    </Box>
  );
};
```

### **Convenções de Nomenclatura**
- **PascalCase** para nomes de componentes
- **camelCase** para props e variáveis
- **kebab-case** para classes CSS
- **UPPER_CASE** para constantes

### **Documentação**
- JSDoc para props complexas
- Exemplos de uso
- Descrição de funcionalidades
- Notas de implementação

## 🧪 Testes de Componentes

### **Testes Unitários**
```tsx
import { render, screen } from '@testing-library/react';
import { DashboardCard } from './DashboardCard';

describe('DashboardCard', () => {
  it('should render title and value', () => {
    render(<DashboardCard title="Test" value="123" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
    expect(screen.getByText('123')).toBeInTheDocument();
  });
});
```

### **Testes de Integração**
- Interação com APIs
- Estados de loading
- Tratamento de erros
- Responsividade

## 📚 Recursos Adicionais

### **Storybook** (Futuro)
- Documentação interativa
- Exemplos de uso
- Testes visuais
- Desenvolvimento isolado

### **Component Library**
- Biblioteca de componentes
- Guia de estilo
- Padrões de design
- Boas práticas

---
*Componentes desenvolvidos com React, TypeScript e Material-UI*  
*Última atualização: Janeiro 2025* 