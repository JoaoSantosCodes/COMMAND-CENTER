# 📚 Documentação Unificada - Sistema ConsultaVD v2.0

---

## 🎯 Visão Geral do Sistema

### **O que é o ConsultaVD?**
Sistema completo para consulta, visualização e **edição** de dados convertidos de planilhas Excel para SQLite, com interface web intuitiva e arquitetura modular.

### **Versão Atual**
- **Versão**: 2.0 (Modular)
- **Status**: ✅ Produção
- **Arquitetura**: Modular com componentes reutilizáveis
- **Frontend**: React/TypeScript + Material-UI
- **Backend**: FastAPI + SQLite
- **Interface**: Streamlit (versão modular)

### **Principais Características**
- ✅ **Arquitetura Modular**: Componentes reutilizáveis e independentes
- ✅ **Busca Unificada**: Pesquisa integrada em múltiplas tabelas
- ✅ **Edição de Dados**: Interface de edição com auditoria completa
- ✅ **Dashboard Interativo**: Métricas e gráficos em tempo real
- ✅ **Sistema de Cache**: Performance otimizada
- ✅ **Responsividade**: Interface adaptável a diferentes dispositivos
- ✅ **Auditoria Completa**: Log de todas as alterações
- ✅ **Exportação**: Dados em Excel/CSV

---

## 🏗️ Arquitetura e Estrutura

### **Estrutura Modular do Projeto**

```
ConsultaVD/
├── 📁 src/                          # Código fonte modular
│   ├── 📁 database/                 # Camada de banco de dados
│   │   ├── __init__.py
│   │   ├── connection.py           # Conexões e operações básicas
│   │   └── queries.py              # Queries específicas do sistema
│   ├── 📁 editor/                   # Sistema de edição
│   │   ├── __init__.py
│   │   ├── audit.py                # Auditoria e logs
│   │   ├── operations.py           # Operações de edição
│   │   └── fields.py               # Definição de campos editáveis
│   ├── 📁 ui/                       # Componentes de interface
│   │   ├── __init__.py
│   │   ├── components.py           # Componentes reutilizáveis
│   │   ├── layout.py               # Layout base e sidebar
│   │   ├── sections.py             # Seções principais do app
│   │   ├── stamps.py               # Geração de carimbos
│   │   ├── validation.py           # Validações e regras
│   │   └── guided_search/          # Buscas guiadas
│   │       └── loja_operadora_circuito.py
│   └── 📁 cache/                    # Sistema de cache
│       ├── __init__.py
│       └── memory_cache.py         # Cache em memória
├── 📱 consultavd-frontend/          # Frontend React/TypeScript
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   └── package.json
├── 📄 app_modular.py               # Aplicação principal (modular)
├── 📄 api_backend.py               # API FastAPI
├── 📄 config.py                    # Configuração centralizada
├── 📄 requirements.txt             # Dependências Python
├── 📄 consulta_vd.db              # Banco SQLite
├── 📄 Inventario.xlsx             # Planilha de inventário
├── 📄 Relação de Lojas.xlsx       # Planilha de lojas
└── 📁 docs/                        # Documentação completa
```

### **Componentes Modulares**

#### **1. Database Layer** (`src/database/`)
- **`connection.py`**: Conexões, operações básicas e queries genéricas
- **`queries.py`**: Queries específicas do sistema (busca unificada, filtros, etc.)

#### **2. Editor System** (`src/editor/`)
- **`audit.py`**: Sistema de auditoria e logs de alterações
- **`operations.py`**: Operações de edição com validação
- **`fields.py`**: Definição de campos editáveis e configurações

#### **3. UI Components** (`src/ui/`)
- **`components.py`**: Componentes reutilizáveis (cards, filtros, exportação)
- **`layout.py`**: Layout base, sidebar, menu, footer
- **`sections.py`**: Seções principais do app
- **`stamps.py`**: Geração de carimbos para chamados
- **`validation.py`**: Validações de formulários e informativos
- **`guided_search/`**: Fluxos de busca guiada

#### **4. Cache System** (`src/cache/`)
- **`memory_cache.py`**: Cache em memória para otimização de performance

### **Componentes Visuais Reutilizáveis**
- **DashboardCard**: Card customizável para métricas e destaques
- **AlertMessage**: Alerta colorido para info, sucesso, erro, aviso
- **SectionTitle**: Título de seção com ou sem ícone
- **Divider**: Linha divisória estilizada
- **TableViewer**: Visualização de DataFrame com legenda
- **CustomForm**: Formulário dinâmico e reutilizável
- **FilterBar**: Barra de filtros customizada
- **CustomList**: Lista customizada com renderização flexível

---

## 🚀 Funcionalidades Principais

### **1. Busca Unificada**
- **People/PEOP**: Busca por código de loja
- **Designação**: Busca por tipo de circuito (VIVO, CLARO, OI)
- **ID Vivo**: Busca específica para operadora VIVO
- **Endereço**: Busca por endereço, bairro ou cidade
- **GGL e GR**: Validação de gerentes regionais
- **Resultados unificados** com campos principais
- **Filtro dinâmico** por operadora
- **Geração automática** de carimbos para chamados

### **2. Busca Guiada**
- **Loja > Operadora > Circuito**: Navegação estruturada
- **Filtros dinâmicos** baseados no conteúdo real
- **Interface intuitiva** com seleção em cascata
- **Detalhes completos** do circuito selecionado

### **3. Edição de Dados**
- **Edição inline** de campos diretamente na interface
- **Salvamento automático** no banco de dados
- **Sistema de auditoria** completo
- **Validação de campos** antes do salvamento
- **Feedback visual** de sucesso/erro nas operações

#### **Campos Editáveis**

**Tabela `lojas_lojas`:**
- LOJAS, ENDEREÇO, BAIRRO, CIDADE, UF, CEP
- TELEFONE1, TELEFONE2, CELULAR, E_MAIL
- 2ª_a_6ª, SAB, DOM, FUNC.
- VD_NOVO, NOME_GGL, NOME_GR

**Tabela `inventario_planilha1`:**
- Status_Loja, Operadora
- ID_VIVO, Novo_ID_Vivo
- Circuito_Designação, Novo_Circuito_Designação

### **4. Dashboard Interativo**
- **Estatísticas em tempo real**
- **Gráficos dinâmicos** (status, operadoras, UFs)
- **Alertas de inconsistências**
- **Cards informativos**
- **Métricas principais**:
  - Total de lojas ativas, inativas, a inaugurar
  - Distribuição por status, GGL, GR, UF, operadora

### **5. Sistema de Auditoria**
- **Log completo** de todas as alterações
- **Filtros por tabela** e período
- **Exportação de logs**
- **Estatísticas de modificações**
- **Nova aba "Auditoria"** no menu principal

### **6. Geração de Carimbos**
- **Carimbo visual** para abertura de chamados
- **Formatação automática** de horários
- **Botão para copiar** carimbo em texto puro
- **Integração com dados** do inventário

### **7. Exportação de Dados**
- **Exportação automática** de qualquer resultado
- **Formatos**: Excel (.xlsx) e CSV
- **Nomes de arquivo** específicos por tipo de busca
- **Botões de exportação** em todas as abas

### **8. Validação e Alertas**
- **Validação automática** de dados
- **Alertas automáticos**:
  - Lojas sem GGL ou GR cadastrado
  - Duplicidade de código PEOP
  - Campos obrigatórios vazios
  - Lojas ativas sem telefone

### **9. Consulta SQL Customizada**
- **Execução de queries** SQL personalizadas
- **Interface amigável** para consultas complexas
- **Tratamento de erros**
- **Exemplos de consultas**
- **Apenas SELECT** permitido (segurança)

### **10. Gerenciamento de Cache**
- **Cache inteligente** de consultas
- **Lazy loading** de dados
- **Paginação** de resultados
- **Filtros otimizados**
- **Queries parametrizadas**

---

## 🛠️ Instalação e Configuração

### **Pré-requisitos**
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Node.js 14+ (para frontend React)

### **Instalação Completa**

#### **Opção 1: Script Automático**
```bash
# Executar script completo
start_system.bat
```

#### **Opção 2: Instalação Manual**

**1. Clone ou baixe o projeto**

**2. Instale as dependências Python:**
```bash
pip install -r requirements.txt
```

**3. Execute o script de conversão das planilhas:**
```bash
python excel_to_sqlite.py
```

**4. Para Frontend React/TypeScript:**
```bash
cd consultavd-frontend
npm install
```

**5. Inicie a aplicação:**

**Backend (FastAPI):**
```bash
python -m uvicorn api_backend:app --reload
```

**Frontend (React):**
```bash
cd consultavd-frontend
npm start
```

**Aplicação Modular (Streamlit):**
```bash
python -m streamlit run app_modular.py
```

### **URLs de Acesso**
- **Frontend React**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health
- **Aplicação Streamlit**: http://localhost:8501

### **Teste do Sistema**
```bash
# Executar testes modulares
python test_modular.py

# Executar testes de importação
python test_imports.py

# Teste completo do sistema
test_system.bat
```

---

## 🎯 Guia de Uso

### **Dashboard**
1. Acesse o Dashboard no menu principal
2. Visualize estatísticas em tempo real
3. Analise gráficos de distribuição
4. Identifique alertas de inconsistências

### **Busca Unificada**
1. Acesse "Busca Unificada"
2. Escolha o tipo de busca (People/PEOP, Designação, etc.)
3. Digite os critérios de busca
4. Visualize os resultados unificados
5. Use o filtro de operadora se necessário
6. Copie o carimbo gerado

### **Busca Guiada**
1. Acesse "Busca Guiada"
2. Digite parte do nome ou código da loja
3. Selecione a loja desejada na lista filtrada
4. Selecione a operadora disponível
5. Selecione o circuito/designação
6. Veja todos os detalhes do circuito selecionado

### **Edição de Dados**
1. Acesse "Edição de Dados"
2. Selecione a tabela desejada
3. Escolha o registro pelo ID (People/PEOP)
4. Edite os campos desejados
5. Clique em "Salvar Alterações"
6. Confirme o sucesso da operação
7. Verifique o histórico na auditoria

### **Auditoria**
1. Acesse "Auditoria"
2. Visualize histórico de alterações
3. Use filtros por tabela e período
4. Analise estatísticas de modificações
5. Exporte logs se necessário

### **Visualização**
1. Acesse "Visualizar Tabelas"
2. Selecione a tabela
3. Ajuste o limite de registros
4. Use filtros dinâmicos
5. Explore os dados

### **SQL Customizado**
1. Acesse "Consulta SQL Customizada"
2. Digite sua query SQL (apenas SELECT)
3. Execute e visualize os resultados
4. Use os exemplos fornecidos

### **Ajuda e Documentação**
1. Acesse "Ajuda" no menu principal
2. Explore as 4 seções:
   - 🚀 **Guia Rápido**: Visão geral das funcionalidades
   - ❓ **FAQ**: Perguntas frequentes com respostas
   - 📖 **Tutoriais**: Passo a passo detalhado
   - 🔧 **Solução de Problemas**: Troubleshooting

---

## 🔧 Desenvolvimento e Manutenção

### **Boas Práticas**
- **Imports absolutos** entre módulos (ex: `from src.ui import ...`)
- **Cada diretório** de módulo possui um `__init__.py`
- **Funções de interface** separadas das utilitárias
- **Documentação separada** por tema

### **Estrutura de Desenvolvimento**
- **Arquitetura modular** com componentes reutilizáveis
- **Sistema de configuração** centralizado
- **Testes automatizados** para cada módulo
- **Validação de imports** antes do deploy

### **Como Usar os Componentes**

#### **Exemplo de Card no Dashboard**
```python
from src.ui import DashboardCard
DashboardCard("Total de Lojas", "123", icon="🏪", color="blue").render()
```

#### **Exemplo de Formulário Customizado**
```python
from src.ui import CustomForm
fields = [
    {"label": "Nome", "key": "nome", "type": "text"},
    {"label": "Status", "key": "status", "type": "select", "options": ["Ativo", "Inativo"]}
]
CustomForm(fields, on_submit, title="Cadastro")
```

#### **Exemplo de Filtro**
```python
from src.ui import FilterBar
filters = [
    {"label": "Status", "key": "status", "type": "select", "options": ["Todos", "Ativo", "Inativo"]},
    {"label": "Nome", "key": "nome", "type": "text"}
]
FilterBar(filters, on_filter)
```

### **Testes**
```bash
# Validar configurações
python -c "import config; print(config.validate_config())"

# Testar componentes individuais
python -c "from src.database import get_tables; print(get_tables())"

# Executar build completo
python build.py
```

### **Performance**
- **Lazy loading** de dados
- **Cache inteligente** de consultas
- **Paginação** de resultados
- **Filtros otimizados**
- **Queries parametrizadas**

---

## 🗺️ Roadmap e Melhorias

### **Status Atual: v2.0 - Modular** ✅

#### **✅ Implementado e Funcionando**
- **Arquitetura Base**: Modularização completa, configuração centralizada
- **Funcionalidades de Busca**: Busca unificada, busca guiada, filtros avançados
- **Edição de Dados**: Interface de edição, validação, auditoria
- **Dashboard e Visualização**: Estatísticas, gráficos, consulta SQL
- **Qualidade e Testes**: Testes automatizados, validação de imports

### **🚀 Roadmap Q3-Q4 2025**

#### **🎯 Prioridade Alta**
- **Segurança e Autenticação**: Sistema de login, controle de acesso
- **Interface e UX**: Tema escuro/claro, notificações, interface mobile
- **Integração e APIs**: API REST, webhooks, integração externa

#### **🎯 Prioridade Média**
- **Analytics e Relatórios**: Relatórios personalizados, gráficos avançados
- **Automação e IA**: Sugestões inteligentes, detecção de inconsistências
- **Performance e Escalabilidade**: Cache Redis, otimização de queries

#### **🎯 Prioridade Baixa**
- **Funcionalidades Avançadas**: Backup automático, versionamento, workflow
- **Documentação e Treinamento**: Vídeos tutoriais, guia interativo

### **📅 Cronograma Detalhado**

- **Julho 2025**: Sistema de autenticação, tema escuro/claro, API REST básica
- **Agosto 2025**: Relatórios personalizados, gráficos interativos, notificações
- **Setembro 2025**: Sugestões inteligentes, detecção de inconsistências, cache Redis
- **Outubro 2025**: Containerização, deploy automatizado, monitoramento
- **Novembro 2025**: Migração PostgreSQL, PWA, offline mode
- **Dezembro 2025**: Sistema de backup, workflow de aprovação, documentação

### **🎯 Métricas de Sucesso**
- **Performance**: Tempo de resposta < 2s, uptime > 99.9%
- **Usabilidade**: Taxa de adoção > 90%, satisfação > 4.5/5
- **Qualidade**: Cobertura de testes > 90%, bugs críticos = 0

---

## 📊 Status e Conversões

### **✅ Conversão React/TypeScript Concluída**

#### **Problemas Resolvidos**
1. **Erro de Importação no Cache**: Adicionadas funções `get_cache`, `set_cache`
2. **Arquivos Faltantes no Frontend**: Criados arquivos essenciais (index.html, manifest.json, etc.)

#### **Sistema Pronto para Uso**
- **Backend (FastAPI)**: API REST completa, endpoints CRUD, cache funcionando
- **Frontend (React/TypeScript)**: Estrutura básica, Material-UI, roteamento, tema personalizado

### **🔄 Atualizações Recentes**

#### **v2.0 - Sistema Modular**
- ✅ Arquitetura modular com componentes reutilizáveis
- ✅ Sistema de configuração centralizado
- ✅ Dashboard interativo com gráficos
- ✅ Sistema de auditoria completo
- ✅ Validações avançadas de campos
- ✅ Componentes de UI reutilizáveis
- ✅ Geração de carimbos aprimorada
- ✅ Consulta SQL customizada segura

#### **v1.0 - Sistema Original**
- ✅ Conversão Excel → SQLite
- ✅ Busca unificada
- ✅ Geração de carimbos
- ✅ Interface web Streamlit

---

## 🔧 Troubleshooting

### **Problemas Comuns**

#### **1. Erro de Importação**
```bash
# Verificar imports
python test_imports.py

# Validar configurações
python -c "import config; print(config.validate_config())"
```

#### **2. Problemas de Cache**
```bash
# Limpar cache
python -c "from src.cache.memory_cache import clear_cache; clear_cache()"
```

#### **3. Erro no Banco de Dados**
```bash
# Verificar estrutura do banco
python scripts/utils/check_tables.py

# Reconstruir banco
python excel_to_sqlite.py
```

#### **4. Problemas de Frontend**
```bash
# Reinstalar dependências
cd consultavd-frontend
rm -rf node_modules package-lock.json
npm install
```

### **Logs e Debug**
- **Logs de aplicação**: Pasta `logs/`
- **Logs de auditoria**: Acessível via interface
- **Logs de erro**: Console do navegador (frontend)
- **Logs de API**: Terminal do backend

### **Validação do Sistema**
```bash
# Teste completo
test_system.bat

# Teste individual
python test_modular.py
```

---

## 📚 Referências Técnicas

### **Lógica de Busca**

#### **Busca por People/PEOP**
- Busca exata por código PEOP
- Resultados unificados de ambas as tabelas
- Validação de existência do código

#### **Busca por Designação**
- Busca por tipo de circuito (VIVO, CLARO, OI)
- Filtro por operadora específica
- Resultados com detalhes completos

#### **Busca por ID Vivo**
- Busca específica para operadora VIVO
- Validação de formato do ID
- Resultados com informações de circuito

#### **Busca por Endereço**
- Busca por endereço, bairro ou cidade
- Busca parcial (LIKE)
- Resultados ordenados por relevância

### **Estrutura de Dados**

#### **Tabela `lojas_lojas`**
- **Campos principais**: PEOP, LOJAS, ENDEREÇO, BAIRRO, CIDADE, UF
- **Contatos**: TELEFONE1, TELEFONE2, CELULAR, E_MAIL
- **Horários**: 2ª_a_6ª, SAB, DOM, FUNC.
- **Gerentes**: VD_NOVO, NOME_GGL, NOME_GR

#### **Tabela `inventario_planilha1`**
- **Identificação**: ID_VIVO, Novo_ID_Vivo
- **Circuito**: Circuito_Designação, Novo_Circuito_Designação
- **Status**: Status_Loja, Operadora
- **Relacionamento**: PEOP (chave estrangeira)

### **Sistema de Auditoria**
- **Log de alterações**: Tabela, campo, valor anterior, valor novo
- **Metadados**: Usuário, data/hora, IP
- **Filtros**: Por tabela, período, tipo de alteração
- **Exportação**: Logs em Excel/CSV

### **Sistema de Cache**
- **Cache em memória**: Para consultas frequentes
- **TTL configurável**: Tempo de vida dos dados em cache
- **Invalidação automática**: Após alterações no banco
- **Métricas**: Hit rate, miss rate, tamanho do cache

---

## 📞 Suporte e Contato

### **Para Dúvidas**
- **Documentação**: Pasta `docs/`
- **Ajuda integrada**: Aba "Ajuda" no sistema
- **FAQ**: Perguntas frequentes na documentação

### **Para Problemas Técnicos**
- **Logs**: Verificar pasta `logs/` e interface de auditoria
- **Testes**: Executar `test_system.bat`
- **Validação**: Verificar imports e configurações

### **Para Desenvolvimento**
- **Código fonte**: Pasta `src/`
- **Testes**: Pasta `tests/`
- **Scripts**: Pasta `scripts/`

### **Informações do Sistema**
- **Versão**: ConsultaVD v2.0 - Modular
- **Arquitetura**: React/TypeScript + FastAPI + SQLite
- **Última atualização**: Janeiro 2025
- **Status**: ✅ Produção

---

## 📝 Histórico de Versões

### **v2.0 - Sistema Modular (Atual)**
- **Data**: Janeiro 2025
- **Principais mudanças**: Arquitetura modular, React/TypeScript, FastAPI
- **Status**: ✅ Produção

### **v1.0 - Sistema Original**
- **Data**: Dezembro 2024
- **Principais mudanças**: Conversão Excel → SQLite, busca unificada
- **Status**: ✅ Legado

---

*Documentação unificada gerada em: Janeiro 2025*  
*Versão: ConsultaVD v2.0 - Modular*  
*Total de arquivos consolidados: 21*  
*Tamanho total da documentação original: ~300KB* 