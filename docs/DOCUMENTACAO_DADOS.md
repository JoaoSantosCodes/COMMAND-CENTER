# Documentação Técnica - Sistema de Consulta e Edição VD

## 📋 Visão Geral

Sistema completo para conversão, consulta, visualização e **edição** de dados de planilhas Excel para SQLite, com interface web Streamlit.

## 🏗️ Arquitetura

### **Componentes Principais:**
1. **Conversor Excel → SQLite** (`excel_to_sqlite.py`)
2. **Interface Web** (`app_streamlit.py`)
3. **Banco de Dados** (`consulta_vd.db`)
4. **Sistema de Edição** (integrado na interface)

### **Fluxo de Dados:**
```
Planilhas Excel → Conversor → SQLite → Interface Web → Edição → SQLite
```

## 🗄️ Estrutura do Banco

### **Tabela: `inventario_planilha1`**
- **Registros:** 5.370
- **Origem:** `Inventario.xlsx` (Planilha1)

**Campos Principais:**
- `People` (TEXT) - Código identificador
- `Status_Loja` (TEXT) - Status da loja
- `Operadora` (TEXT) - Nome da operadora
- `ID_VIVO` (TEXT) - ID Vantive
- `Novo_ID_Vivo` (TEXT) - Novo ID Vivo
- `Circuito_Designação` (TEXT) - Designação do circuito
- `Novo_Circuito_Designação` (TEXT) - Nova designação

**Campos Editáveis:**
- Status_Loja, Operadora
- ID_VIVO, Novo_ID_Vivo
- Circuito_Designação, Novo_Circuito_Designação

### **Tabela: `lojas_lojas`**
- **Registros:** 1.927
- **Origem:** `Relação de Lojas.xlsx` (Lojas)

**Campos Principais:**
- `PEOP` (TEXT) - Código identificador
- `LOJAS` (TEXT) - Nome da loja
- `ENDEREÇO` (TEXT) - Endereço completo
- `CIDADE` (TEXT) - Cidade
- `UF` (TEXT) - Estado
- `TELEFONE1` (TEXT) - Telefone principal
- `E_MAIL` (TEXT) - E-mail
- `2ª_a_6ª` (TEXT) - Horário de funcionamento

**Campos Editáveis:**
- LOJAS, ENDEREÇO, BAIRRO, CIDADE, UF, CEP
- TELEFONE1, TELEFONE2, CELULAR, E_MAIL
- 2ª_a_6ª, SAB, DOM, FUNC.
- VD_NOVO, NOME_GGL, NOME_GR

## 🔧 Funcionalidades de Edição

### **Sistema de Edição Inline**
- **Interface dedicada** para edição de registros
- **Seleção por tabela e ID** (People/PEOP)
- **Campos editáveis** pré-definidos por tabela
- **Validação automática** antes do salvamento
- **Feedback visual** de sucesso/erro

### **Funções de Atualização**

#### `update_lojas_record(peop_code, field, new_value)`
```python
def update_lojas_record(peop_code, field, new_value):
    """Atualiza um campo na tabela lojas_lojas"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Escape de caracteres especiais
        if field in ['ENDEREÇO', 'E_MAIL', '2ª_a_6ª', 'FUNC.']:
            field_escaped = f'"{field}"'
        else:
            field_escaped = field
        
        query = f"UPDATE lojas_lojas SET {field_escaped} = ? WHERE PEOP = ?"
        cursor.execute(query, (new_value, peop_code))
        conn.commit()
        return True, "Campo atualizado com sucesso!"
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao atualizar: {str(e)}"
```

#### `update_inventario_record(people_code, field, new_value)`
```python
def update_inventario_record(people_code, field, new_value):
    """Atualiza um campo na tabela inventario_planilha1"""
    # Similar ao anterior, mas para inventario_planilha1
```

### **Segurança e Validação**
- **Escape de caracteres especiais** em nomes de colunas
- **Rollback automático** em caso de erro
- **Validação de tipos** de dados
- **Tratamento de exceções** SQL

## 🔍 Busca Unificada

### **Query Principal:**
```sql
SELECT
    i.People as "People/PEOP",
    i.Status_Loja,
    l.LOJAS,
    l.CODIGO,
    l."ENDEREÇO",
    l.BAIRRO,
    l.CIDADE,
    l.UF,
    l.CEP,
    l.TELEFONE1,
    l.TELEFONE2,
    l.CELULAR,
    l."E_MAIL",
    l."2ª_a_6ª",
    l.SAB,
    l.DOM,
    l."FUNC.",
    l.VD_NOVO,
    l.NOME_GGL,
    l.NOME_GR
FROM inventario_planilha1 i
LEFT JOIN lojas_lojas l ON i.People = l.PEOP
WHERE i.People = ?
UNION
SELECT
    l.PEOP as "People/PEOP",
    NULL as Status_Loja,
    l.LOJAS,
    l.CODIGO,
    l."ENDEREÇO",
    l.BAIRRO,
    l.CIDADE,
    l.UF,
    l.CEP,
    l.TELEFONE1,
    l.TELEFONE2,
    l.CELULAR,
    l."E_MAIL",
    l."2ª_a_6ª",
    l.SAB,
    l.DOM,
    l."FUNC.",
    l.VD_NOVO,
    l.NOME_GGL,
    l.NOME_GR
FROM lojas_lojas l
WHERE l.PEOP = ? AND l.PEOP NOT IN (SELECT People FROM inventario_planilha1)
```

### **Características:**
- **UNION** entre inventário e lojas
- **LEFT JOIN** para dados completos
- **Fallback** para lojas sem inventário
- **Campos unificados** com aliases

## 🏷️ Sistema de Carimbos

### **Geração Automática:**
- **Dados unificados** das duas tabelas
- **Formatação de horários** automática
- **Integração com inventário** por operadora
- **Versão visual e texto puro**

### **Campos do Carimbo:**
- VD (People/PEOP)
- Operadora (do inventário)
- Designação (do inventário)
- ID Vantive (do inventário)
- Endereço e Cidade (das lojas)
- Horário de Funcionamento (das lojas)
- Contatos Command Center

## 🎨 Interface Web

### **Navegação:**
- **Sidebar** com opções principais
- **Modo de edição** com toggle
- **Feedback visual** para todas as operações
- **Design responsivo**

### **Páginas Principais:**
1. **Busca Unificada People/PEOP**
2. **Edição de Dados** (NOVO)
3. **Visualizar Tabelas**
4. **Consulta SQL Customizada**
5. **Sobre**

### **Estado da Sessão:**
```python
st.session_state = {
    'people_code': '',
    'operadora_sel': '',
    'edit_mode': False
}
```

## 🔒 Considerações de Segurança

### **Validação de Dados:**
- **Verificação de tipos** antes do salvamento
- **Escape de SQL injection** em queries dinâmicas
- **Validação de campos obrigatórios**

### **Backup e Recuperação:**
- **Rollback automático** em transações
- **Logs de erro** detalhados
- **Recomendação de backup** antes de edições

## 📊 Performance

### **Otimizações:**
- **Limite de registros** na visualização
- **Índices automáticos** no SQLite
- **Queries otimizadas** com JOINs
- **Cache de sessão** para dados frequentes

### **Limitações:**
- **SQLite** para desenvolvimento/pequeno volume
- **Sem paginação** avançada
- **Sem cache distribuído**

## 🚀 Deploy e Manutenção

### **Requisitos:**
- Python 3.8+
- Streamlit 1.45+
- pandas, openpyxl, sqlite3

### **Comandos de Deploy:**
```bash
# Instalação
pip install -r requirements.txt

# Conversão de dados
python excel_to_sqlite.py

# Execução
python -m streamlit run app_streamlit.py
```

### **Monitoramento:**
- **Logs do Streamlit** para erros
- **Verificação de integridade** do banco
- **Backup regular** dos dados

## 🔄 Versionamento

### **v2.0 - Sistema de Edição**
- ✅ Edição inline de campos
- ✅ Salvamento automático
- ✅ Interface de edição dedicada
- ✅ Validação e tratamento de erros

### **v1.0 - Sistema de Consulta**
- ✅ Conversão Excel → SQLite
- ✅ Busca unificada
- ✅ Geração de carimbos
- ✅ Interface web

## 📞 Suporte Técnico

### **Logs Importantes:**
- **Erros SQL** na edição
- **Problemas de conexão** com banco
- **Erros de validação** de dados

### **Troubleshooting:**
1. Verificar estrutura do banco
2. Validar nomes de colunas
3. Testar queries isoladamente
4. Verificar permissões de arquivo

---

**Documentação técnica do Sistema de Consulta e Edição VD** 🏪 