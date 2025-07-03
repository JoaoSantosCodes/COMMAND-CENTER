# 📁 Estrutura do Projeto ConsultaVD v2.0 (Atualizada)

## 🏗️ Visão Geral da Arquitetura

O ConsultaVD v2.0 está totalmente modularizado, com componentes visuais reutilizáveis e seções independentes para cada parte do sistema.

### Principais Componentes Visuais
- **DashboardCard**: Card customizável para métricas e destaques
- **AlertMessage**: Alerta colorido para info, sucesso, erro, aviso
- **SectionTitle**: Título de seção com ou sem ícone
- **Divider**: Linha divisória estilizada
- **TableViewer**: Visualização de DataFrame com legenda
- **CustomForm**: Formulário dinâmico e reutilizável
- **FilterBar**: Barra de filtros customizada
- **CustomList**: Lista customizada com renderização flexível

### Seções Modularizadas
- **show_dashboard_section**
- **show_unified_search_section**
- **show_guided_search_section**
- **show_data_editor_section**
- **show_audit_section**
- **show_table_viewer_section**
- **show_sql_query_section**
- **show_help_section**
- **show_about_section**
- **show_cache_management_section**

Essas seções podem ser facilmente manipuladas, testadas e expandidas de forma independente.

## 📦 Estrutura de Pastas (Resumo)

```
ConsultaVD/
├── app_modular.py
├── config.py
├── requirements.txt
├── build.py
├── README.md
├── src/
│   ├── ui/
│   │   ├── components.py   # Componentes visuais reutilizáveis
│   │   ├── layout.py       # Layout base, sidebar, menu, footer
│   │   ├── sections.py     # Seções principais do app
│   │   └── ...
│   └── ...
├── docs/
│   ├── ESTRUTURA_PROJETO_ATUALIZADA.md
│   └── ...
├── data/
├── logs/
├── scripts/
├── tests/
└── ...
```

## 🚀 Como Usar os Componentes

### Exemplo de Card no Dashboard
```python
from src.ui import DashboardCard
DashboardCard("Total de Lojas", "123", icon="🏪", color="blue").render()
```

### Exemplo de Formulário Customizado
```python
from src.ui import CustomForm
fields = [
    {"label": "Nome", "key": "nome", "type": "text"},
    {"label": "Status", "key": "status", "type": "select", "options": ["Ativo", "Inativo"]}
]
CustomForm(fields, on_submit, title="Cadastro")
```

### Exemplo de Filtro
```python
from src.ui import FilterBar
filters = [
    {"label": "Status", "key": "status", "type": "select", "options": ["Todos", "Ativo", "Inativo"]},
    {"label": "Nome", "key": "nome", "type": "text"}
]
FilterBar(filters, on_filter)
```

### Exemplo de Lista
```python
from src.ui import CustomList
CustomList([{"nome": "João"}], lambda item, i: st.write(item["nome"]))
```

## 🔄 Benefícios
- **Reutilização**: Use os mesmos componentes em diferentes seções
- **Padronização**: Visual consistente em todo o app
- **Facilidade de manutenção**: Alterações em um componente refletem em todo o sistema
- **Testabilidade**: Cada seção e componente pode ser testado isoladamente

---
*Documentação atualizada em: 29/06/2025*
