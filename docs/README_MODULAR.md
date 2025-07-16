# ConsultaVD - Sistema Modular v2.0

Sistema completo para consulta, visualização e **edição** de dados convertidos de planilhas Excel para SQLite, com interface web intuitiva e arquitetura modular.

## Estrutura Modular

O projeto ConsultaVD está organizado em módulos separados por domínio de responsabilidade:

- **src/database/**: Conexão e queries SQL.
- **src/editor/**: Lógica de edição, campos editáveis e auditoria.
- **src/ui/**: Componentes visuais, validação, responsividade e buscas guiadas.
  - **src/ui/guided_search/**: Fluxos de busca guiada (ex: Loja > Operadora > Circuito).

## Boas práticas

- Imports absolutos entre módulos (ex: `from src.ui import ...`).
- Cada diretório de módulo possui um `__init__.py`.
- Funções de interface separadas das utilitárias.
- Documentação separada por tema.

## 🏗️ Arquitetura Modular

### 📁 Estrutura do Projeto

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
│   └── 📁 ui/                       # Componentes de interface
│       ├── __init__.py
│       ├── components.py           # Componentes reutilizáveis
│       ├── stamps.py               # Geração de carimbos
│       └── validation.py           # Validações e regras
├── 📄 app_modular.py               # Aplicação principal (modular)
├── 📄 app_streamlit_fixed.py       # Aplicação original (legado)
├── 📄 config.py                    # Configuração centralizada
├── 📄 excel_to_sqlite.py           # Conversor Excel → SQLite
├── 📄 requirements.txt             # Dependências
├── 📄 consulta_vd.db              # Banco SQLite
├── 📄 Inventario.xlsx             # Planilha de inventário
├── 📄 Relação de Lojas.xlsx       # Planilha de lojas
└── 📄 README_MODULAR.md           # Esta documentação
```

## 🔧 Componentes Modulares

### 1. **Database Layer** (`src/database/`)
- **`connection.py`**: Conexões, operações básicas e queries genéricas
- **`queries.py`**: Queries específicas do sistema (busca unificada, filtros, etc.)

### 2. **Editor System** (`src/editor/`)
- **`audit.py`**: Sistema de auditoria e logs de alterações
- **`operations.py`**: Operações de edição com validação
- **`fields.py`**: Definição de campos editáveis e configurações

### 3. **UI Components** (`src/ui/`)
- **`components.py`**: Componentes reutilizáveis (cards, filtros, exportação)
- **`stamps.py`**: Geração de carimbos para chamados
- **`validation.py`**: Validações de formulários e informativos

### 4. **Configuration** (`config.py`)
- Configuração centralizada do sistema
- Configurações por ambiente (dev, staging, production)
- Validação de configurações

## 🚀 Funcionalidades

### 🔎 **Busca Unificada**
- Pesquisa por código People/PEOP em ambas as tabelas
- Resultados unificados com campos principais
- Filtro dinâmico por operadora
- Geração automática de carimbos para chamados

### ✏️ **Edição de Dados**
- **Edição inline** de campos diretamente na interface
- **Salvamento automático** no banco de dados
- **Sistema de auditoria** completo
- **Validação de campos** antes do salvamento
- **Feedback visual** de sucesso/erro nas operações

### 📊 **Dashboard Interativo**
- Estatísticas em tempo real
- Gráficos dinâmicos (status, operadoras, UFs)
- Alertas de inconsistências
- Cards informativos

### 📋 **Sistema de Auditoria**
- Log completo de todas as alterações
- Filtros por tabela e período
- Exportação de logs
- Estatísticas de modificações

### 🔧 **Consulta SQL Customizada**
- Execução de queries SQL personalizadas
- Interface amigável para consultas complexas
- Tratamento de erros
- Exemplos de consultas

### 🏷️ **Geração de Carimbos**
- Carimbo visual para abertura de chamados
- Formatação automática de horários
- Botão para copiar carimbo em texto puro
- Integração com dados do inventário

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o script de conversão das planilhas:**
   ```bash
   python excel_to_sqlite.py
   ```

4. **Inicie a aplicação modular:**
   ```bash
   python -m streamlit run app_modular.py
   ```

## 🎯 Como Usar

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

## 🔧 Campos Editáveis

### **Tabela `lojas_lojas`:**
- LOJAS, ENDEREÇO, BAIRRO, CIDADE, UF, CEP
- TELEFONE1, TELEFONE2, CELULAR, E_MAIL
- 2ª_a_6ª, SAB, DOM, FUNC.
- VD_NOVO, NOME_GGL, NOME_GR

### **Tabela `inventario_planilha1`:**
- Status_Loja, Operadora
- ID_VIVO, Novo_ID_Vivo
- Circuito_Designação, Novo_Circuito_Designação

## 🎨 Interface

- **Design responsivo** e moderno
- **Navegação intuitiva** por sidebar
- **Feedback visual** para todas as operações
- **Modo de edição** com toggle
- **Carimbos visuais** com contraste otimizado
- **Dashboard interativo** com gráficos

## 🔒 Segurança

- **Validação de campos** antes do salvamento
- **Tratamento de erros** SQL
- **Rollback automático** em caso de falha
- **Escape de caracteres especiais** em nomes de colunas
- **Sistema de auditoria** completo
- **Logs de alterações** detalhados

## 📊 Exemplos de Uso

### **Busca e Edição Completa:**
1. Buscar um People/PEOP
2. Verificar dados unificados
3. Ir para "Edição de Dados"
4. Selecionar o registro
5. Corrigir campos incorretos
6. Salvar alterações
7. Verificar carimbo atualizado
8. Consultar histórico na auditoria

### **Correção de Dados:**
```sql
-- Exemplo de correção via interface
UPDATE lojas_lojas SET ENDEREÇO = 'Nova Rua, 123' WHERE PEOP = '12345'
```

## 🚨 Observações Importantes

- **Backup recomendado** antes de edições em massa
- **Validação manual** de dados críticos
- **Teste em ambiente de desenvolvimento** primeiro
- **Logs de alterações** implementados e funcionais
- **Sistema modular** facilita manutenção e extensão

## 🔄 Atualizações Recentes

### **v2.0 - Sistema Modular**
- ✅ Arquitetura modular com componentes reutilizáveis
- ✅ Sistema de configuração centralizado
- ✅ Dashboard interativo com gráficos
- ✅ Sistema de auditoria completo
- ✅ Validações avançadas de campos
- ✅ Componentes de UI reutilizáveis
- ✅ Geração de carimbos aprimorada
- ✅ Consulta SQL customizada segura

### **v1.0 - Sistema Original**
- ✅ Conversão Excel → SQLite
- ✅ Busca unificada
- ✅ Geração de carimbos
- ✅ Interface web Streamlit

## 🧪 Testes

Para executar testes do sistema modular:

```bash
# Validar configurações
python -c "import config; print(config.validate_config())"

# Testar componentes individuais
python -c "from src.database import get_tables; print(get_tables())"
```

## 📈 Performance

- **Lazy loading** de dados
- **Cache inteligente** de consultas
- **Paginação** de resultados
- **Filtros otimizados**
- **Queries parametrizadas**

## 🔮 Roadmap

### **v2.1 - Próximas Funcionalidades**
- [ ] API REST para integração externa
- [ ] Sistema de notificações por email
- [ ] Relatórios automáticos
- [ ] Backup automático do banco
- [ ] Interface mobile otimizada
- [ ] Integração com sistemas externos

### **v2.2 - Melhorias Técnicas**
- [ ] Cache Redis para performance
- [ ] Autenticação e autorização
- [ ] Logs estruturados (JSON)
- [ ] Métricas de performance
- [ ] Testes automatizados
- [ ] CI/CD pipeline

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação técnica
2. Consulte os logs de erro
3. Teste com dados de exemplo
4. Verifique a estrutura do banco
5. Consulte o sistema de auditoria

---

**Desenvolvido para otimizar processos de consulta e manutenção de dados VD** 🏪

**Versão:** 2.0 (Modular)  
**Data:** Dezembro 2024  
**Arquitetura:** Modular com componentes reutilizáveis 