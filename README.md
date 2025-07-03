# 🚀 ConsultaVD - Sistema de Consulta e Gestão de Dados

Sistema moderno e modular para consulta, edição e auditoria de dados de lojas, circuitos e operadoras. Desenvolvido com **FastAPI** (backend) e **React/TypeScript** (frontend), oferecendo interface responsiva, tema claro/escuro e experiência de usuário moderna.

## 🎯 Visão Geral

O ConsultaVD evoluiu de uma aplicação Streamlit monolítica para uma arquitetura moderna e escalável:

- **Backend**: FastAPI com endpoints RESTful
- **Frontend**: React 18 + TypeScript + Material-UI
- **Banco de Dados**: SQLite com sistema de auditoria
- **Interface**: Responsiva com suporte a tema claro/escuro
- **Arquitetura**: Modular e bem documentada

## 🏗️ Arquitetura do Sistema

### Backend (FastAPI)
```
api_backend.py              # API principal com endpoints REST
config.py                   # Configurações centralizadas
requirements.txt            # Dependências Python
```

### Frontend (React/TypeScript)
```
consultavd-frontend/
├── src/
│   ├── components/         # Componentes reutilizáveis
│   ├── pages/             # Páginas da aplicação
│   ├── services/          # Integração com API
│   ├── types/             # Definições TypeScript
│   └── hooks/             # Custom hooks
├── public/                # Arquivos estáticos
└── package.json           # Dependências Node.js
```

### Estrutura Modular (Legacy)
```
src/
├── database/              # Camada de acesso a dados
├── editor/                # Sistema de edição e auditoria
├── ui/                    # Componentes de interface
└── cache/                 # Sistema de cache
```

## 🚀 Como Executar (Scripts)

Todos os scripts de automação agora estão na pasta `scripts/`.

### Desenvolvimento (Backend + Frontend)
```bat
scripts\start_system.bat
```

### Produção Simples (sem Docker)
```bat
scripts\start_production.bat
```

### Deploy Produção Manual (Windows, sem Docker)
```bat
scripts\deploy_production.bat
```

### Deploy Produção com Docker
```bat
scripts\deploy.bat
```

### Iniciar apenas o Backend
```bat
scripts\start_backend.bat
```

### Iniciar apenas o Frontend
```bat
scripts\start_frontend.bat
```

### Testar o Sistema
```bat
scripts\test_system.bat
```

### Checar Tipos TypeScript (Frontend)
```bat
scripts\check_typescript.bat
```

### Gerar Documentação em PDF
```bat
scripts\gerar_documentacao_pdf.bat
# ou (Linux)
scripts/gerar_documentacao_pdf.sh
```

## 🚀 Como Executar

### Opção 1: Sistema Completo (Recomendado)
```bash
# Executar script de inicialização
scripts/start_system.bat
```

### Opção 2: Execução Manual

#### Backend (FastAPI)
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar backend
python -m uvicorn api_backend:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend (React)
```bash
# Navegar para o frontend
cd consultavd-frontend

# Instalar dependências
npm install

# Executar em desenvolvimento
npm start
```

### Acessos
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎨 Interface e UX

### Tema Claro/Escuro
- **Material-UI ThemeProvider** customizado
- **Alternância em tempo real** entre temas
- **Estado persistido** no navegador
- **Componentes responsivos** que respeitam o tema

### Componentes Principais
- **DashboardCard**: Cards de métricas com animações
- **DataTable**: Tabelas com paginação e filtros
- **LojaDetalheCard**: Exibição detalhada de lojas
- **PeopleCard**: Informações de pessoas
- **CarimboGenerator**: Geração de carimbos

### Responsividade
- **Desktop** (1200px+) - Layout completo
- **Tablet** (768px - 1199px) - Layout adaptado
- **Mobile** (< 768px) - Layout mobile-first

## 🔍 Funcionalidades Principais

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

## 📁 Estrutura do Projeto

```
ConsultaVD/
├── 🚀 api_backend.py              # API FastAPI principal
├── ⚙️ config.py                   # Configurações globais
├── 📦 requirements.txt            # Dependências Python
├── 📖 README.md                   # Este arquivo
│
├── 🎨 consultavd-frontend/        # Frontend React/TypeScript
│   ├── src/
│   │   ├── components/            # Componentes reutilizáveis
│   │   ├── pages/                 # Páginas da aplicação
│   │   ├── services/              # Integração com API
│   │   ├── types/                 # Definições TypeScript
│   │   └── hooks/                 # Custom hooks
│   ├── public/                    # Arquivos estáticos
│   └── package.json               # Dependências Node.js
│
├── 🏗️ src/                        # Código modular (legacy)
│   ├── database/                  # Camada de acesso a dados
│   ├── editor/                    # Sistema de edição
│   ├── ui/                        # Componentes de interface
│   └── cache/                     # Sistema de cache
│
├── 📚 docs/                       # Documentação completa (21 arquivos)
├── 🧪 tests/                      # Testes automatizados
├── 🔧 scripts/                    # Scripts de automação
├── 📊 data/                       # Banco de dados e planilhas
├── 📋 logs/                       # Logs de auditoria
├── 📈 reports/                    # Relatórios de build/teste
├── 🏛️ legacy/                     # Versões históricas Streamlit
├── 🖼️ assets/                     # Recursos visuais
└── 📦 dist/                       # Pacote de distribuição
```

## 🔌 API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Estatísticas do dashboard

### Busca
- `GET /api/search/lojas?q={query}` - Busca de lojas
- `GET /api/search/people?code={code}` - Busca de pessoas
- `GET /api/search/id-vivo?id_vivo={id}` - Busca por ID Vivo
- `GET /api/search/ggl-gr?ggl_gr={name}` - Busca por gestor

### Lojas e Operadoras
- `GET /api/lojas/{id}/operadoras` - Operadoras de uma loja
- `GET /api/lojas/{id}/operadoras/{operadora}/circuitos` - Circuitos

### Busca Guiada
- `GET /api/search/loja-operadora-circuito` - Busca guiada completa

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno
- **SQLite** - Banco de dados
- **Pandas** - Manipulação de dados
- **Pydantic** - Validação de dados

### Frontend
- **React 18** - Biblioteca de interface
- **TypeScript** - Tipagem estática
- **Material-UI (MUI)** - Componentes visuais
- **Axios** - Cliente HTTP
- **Recharts** - Gráficos interativos

## 📚 Documentação

### Documentação Principal
- **[📖 Guia de Desenvolvimento](docs/README_MODULAR.md)** - Desenvolvimento modular
- **[🎯 Guia de Uso](docs/GUIA_USO_EDICAO.md)** - Manual do usuário
- **[🗺️ Roadmap 2025](docs/ROADMAP_2025.md)** - Planejamento futuro

### Documentação Técnica
- **[📊 Estrutura de Dados](docs/RELATORIO_ESTRUTURA_DADOS.md)** - Schema do banco
- **[🔍 Busca Guiada](docs/DOCUMENTACAO_BUSCA_GUIADA.md)** - Funcionalidades de busca
- **[🔄 Fluxograma](docs/FLUXOGRAMA_SISTEMA.md)** - Fluxo completo do sistema

### Documentação de Pastas
- **[📁 Frontend](consultavd-frontend/README.md)** - Documentação do React
- **[📁 Scripts](scripts/README.md)** - Scripts de automação
- **[📁 Dados](data/README.md)** - Banco de dados e planilhas
- **[📁 Logs](logs/README.md)** - Sistema de auditoria

## 🧪 Testes

### Executar Testes
```bash
# Testes automatizados
python -m pytest tests/

# Testes específicos
python tests/test_database.py
python tests/test_editor.py
python tests/test_ui.py
```

### Validação do Sistema
```bash
# Verificar se tudo está funcionando
scripts/test_system.bat
```

## 🔧 Scripts de Automação

### Inicialização
- **`start_system.bat`** - Inicia backend e frontend
- **`start_backend.bat`** - Inicia apenas o backend
- **`start_frontend.bat`** - Inicia apenas o frontend

### Desenvolvimento
- **`check_typescript.bat`** - Verifica erros TypeScript
- **`test_system.bat`** - Testa integração

### Utilitários
- **`excel_to_sqlite.py`** - Importa dados de planilhas
- **`query_database.py`** - Consultas no banco
- **`gerar_relatorio_estrutura.py`** - Gera relatórios

## 📊 Status do Projeto

### ✅ Implementado
- [x] Migração para FastAPI + React/TypeScript
- [x] Interface responsiva com Material-UI
- [x] Sistema de tema claro/escuro
- [x] API RESTful completa
- [x] Sistema de auditoria
- [x] Busca unificada e guiada
- [x] Dashboard interativo
- [x] Testes automatizados
- [x] Documentação completa

### 🚧 Em Desenvolvimento
- [ ] Deploy em produção
- [ ] Otimizações de performance
- [ ] Novas funcionalidades

## 🤝 Contribuição

### Padrões de Código
- **TypeScript strict mode** no frontend
- **PEP 8** no backend Python
- **Componentes funcionais** com hooks
- **Documentação** para novas funcionalidades

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

## 📞 Suporte

### Problemas Comuns
1. **Erro de CORS**: Verifique se o backend está rodando
2. **Erro de build**: Limpe cache com `npm run build -- --reset-cache`
3. **Dependências**: Delete `node_modules` e execute `npm install`

### Logs e Debug
- **Console do navegador** para erros de frontend
- **Network tab** para requisições de API
- **Logs de auditoria** em `logs/logs.txt`

---

**ConsultaVD v2.0** - Sistema moderno e modular para gestão de dados  
*Desenvolvido com FastAPI, React, TypeScript e Material-UI*  
*Última atualização: Janeiro 2025*
