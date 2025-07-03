# 📢 Documentação - Sistema de Informativos

## 🎯 Visão Geral

O Sistema de Informativos do ConsultaVD oferece validação inteligente de informativos de incidentes através de um sistema híbrido que combina:

- **🔍 Validação Baseada em Regras** (sempre disponível)
- **🤖 Validação com IA Avançada** (quando configurada)
- **📋 Templates Inteligentes**
- **📊 Histórico de Validações**

## 🚀 Funcionalidades

### 1. 🤖 Validação com IA

#### Validação Baseada em Regras
**Sempre disponível**, sem dependências externas.

**Critérios avaliados:**
- ✅ **Campos obrigatórios**: Loja, Circuito, Operadora, Descrição
- ✅ **Tamanho do texto**: Mínimo 50, máximo 1000 caracteres
- ✅ **Pontuação adequada**: Verifica uso de pontuação
- ✅ **Termos técnicos**: Sugere uso de vocabulário técnico

**Pontuação:**
- **10/10**: Informativo excelente
- **7-9/10**: ✅ Bom
- **4-6/10**: ⚠️ Precisa melhorar
- **0-3/10**: ❌ Precisa revisão

#### Validação com IA Avançada
**Opcional**, requer configuração da API OpenAI.

**Análises realizadas:**
- 🎯 **Clareza**: Avaliação da clareza do texto
- 📋 **Completude**: Verificação de informações completas
- 🚨 **Problemas identificados**: Detecção de inconsistências
- 💡 **Sugestões de melhoria**: Recomendações específicas
- 📊 **Qualidade geral**: Classificação excelente/bom/regular/ruim

### 2. 📋 Templates Inteligentes

**Tipos de incidentes suportados:**
- 🔴 **Falha no Circuito**: Template para falhas completas
- 🟡 **Instabilidade de Conexão**: Template para instabilidades
- 🟠 **Lentidão na Conexão**: Template para problemas de velocidade

**Características:**
- ✅ Estrutura padronizada
- ✅ Campos obrigatórios destacados
- ✅ Formatação profissional
- ✅ Fácil personalização

### 3. 📊 Histórico de Validações

**Funcionalidade em desenvolvimento:**
- 📈 Estatísticas de validações
- 📊 Média de pontuações
- 📅 Histórico temporal
- 👤 Validações por usuário

## ⚙️ Configuração

### Configuração da IA Avançada

1. **Obter API Key da OpenAI:**
   - Acesse: https://platform.openai.com/api-keys
   - Crie uma nova API key
   - Copie a chave

2. **Configurar no Streamlit:**
   
   **Opção A - Arquivo .streamlit/secrets.toml:**
   ```toml
   openai_api_key = "sua-api-key-aqui"
   ```
   
   **Opção B - Variável de ambiente:**
   ```bash
   export OPENAI_API_KEY="sua-api-key-aqui"
   ```

3. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Configuração Local (Sem IA)

O sistema funciona perfeitamente sem a IA avançada:
- ✅ Validação baseada em regras sempre disponível
- ✅ Templates funcionais
- ✅ Interface completa
- ⚠️ Apenas a validação com IA fica indisponível

## 📖 Como Usar

### 1. Acessar o Sistema
1. Abra o ConsultaVD
2. Na sidebar, clique em **"📢 Informativos"**
3. Selecione a aba **"🤖 Validação com IA"**

### 2. Validar um Informativo

#### Com Regras (Recomendado para início):
1. Digite o informativo no campo de texto
2. Clique em **"🔍 Validar com Regras"**
3. Analise os resultados:
   - Pontuação geral
   - Problemas identificados
   - Sugestões de melhoria

#### Com IA Avançada (Se configurada):
1. Digite o informativo no campo de texto
2. Clique em **"🤖 Validar com IA Avançada"**
3. Analise os resultados detalhados:
   - Pontuação de clareza e completude
   - Análise qualitativa
   - Sugestões específicas da IA

### 3. Usar Templates

1. Vá para a aba **"📋 Templates"**
2. Selecione o tipo de incidente
3. Clique em **"📄 Gerar Template"**
4. Personalize o template gerado
5. Use como base para seu informativo

## 🎯 Exemplos de Uso

### Exemplo 1: Informativo Simples
```
Loja DSP Villa Lobos apresentando falha no circuito VIVO desde 14:30. 
Conexão completamente indisponível. Impacto alto nas operações de vendas.
```

**Validação esperada:**
- ✅ Pontuação: 8/10
- ✅ Campos obrigatórios presentes
- ✅ Tamanho adequado
- ✅ Termos técnicos utilizados

### Exemplo 2: Informativo Completo
```
INCIDENTE: Falha no Circuito
Loja: DSP Villa Lobos (Matriz)
Circuito: VIVO-2023-001
Operadora: VIVO
Descrição: Circuito apresentando falha completa desde 14:30
Impacto: Alto - Lojas sem conectividade para vendas
Ações tomadas: Contato com operadora iniciado
Status: Em investigação
```

**Validação esperada:**
- ✅ Pontuação: 10/10
- ✅ Estrutura profissional
- ✅ Informações completas
- ✅ Formatação adequada

## 🔧 Personalização

### Adicionar Novos Campos Obrigatórios

No arquivo `app_streamlit_fixed.py`, função `validar_informativo_regras`:

```python
campos_obrigatorios = {
    "loja": ["loja", "store", "filial"],
    "circuito": ["circuito", "circuit", "designação"],
    "operadora": ["operadora", "operator", "vivo", "oi", "claro", "tim"],
    "descrição": ["descrição", "descricao", "description", "problema", "incidente"],
    "novo_campo": ["palavra_chave1", "palavra_chave2"]  # Adicionar aqui
}
```

### Adicionar Novos Templates

Na função `gerar_template_informativo`:

```python
templates = {
    "falha_circuito": "...",
    "instabilidade": "...",
    "lentidao": "...",
    "novo_tipo": """
    **INCIDENTE: [Nome do Tipo]**
    - **Campo1:** [Descrição]
    - **Campo2:** [Descrição]
    """
}
```

## 🚨 Solução de Problemas

### IA Não Disponível
**Sintoma:** Mensagem "IA não disponível"
**Solução:**
1. Verificar se a API key está configurada
2. Verificar conectividade com internet
3. Usar validação baseada em regras (sempre funciona)

### Erro de Validação
**Sintoma:** Erro ao validar informativo
**Solução:**
1. Verificar se o texto não está vazio
2. Verificar se não excede 1000 caracteres
3. Verificar se contém informações básicas

### Templates Não Aparecem
**Sintoma:** Templates não são gerados
**Solução:**
1. Verificar se selecionou o tipo de incidente
2. Verificar se clicou em "Gerar Template"
3. Verificar se o tipo está na lista de templates

## 📈 Melhorias Futuras

### Planejadas:
- 📊 Dashboard de estatísticas
- 🔄 Histórico persistente no banco
- 🤖 Mais modelos de IA (Claude, Gemini)
- 📱 Interface mobile otimizada
- 🔗 Integração com sistemas externos

### Sugestões:
- 📝 Editor rico de texto
- 🎨 Temas visuais
- 🔔 Notificações de qualidade
- 📋 Exportação de relatórios

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar esta documentação
2. Testar com exemplos simples
3. Usar validação baseada em regras como fallback
4. Verificar logs do sistema

---

**Sistema desenvolvido para ConsultaVD - Versão 2025**

## 📝 Histórico de Alterações Recentes

### 2025-06-26

- **Sistema híbrido de validação de informativos:**
  - Validação baseada em regras (sempre disponível)
  - Validação com IA avançada (OpenAI, opcional)
  - Templates inteligentes e histórico preparado
- **Integração OpenAI atualizada:**
  - Compatível com openai>=1.0.0 (uso de openai.OpenAI e client.chat.completions.create)
  - Ajuste do requirements.txt para dependências modernas
- **Configuração segura da API key:**
  - Criação do arquivo `.streamlit/secrets.toml` para armazenar a chave da OpenAI
- **Melhorias de interface:**
  - Sidebar com navegação única e separação visual por categorias
  - Abas para Validação, Templates e Histórico
  - Feedback visual com métricas, cores e emojis
- **Documentação expandida:**
  - Guia de uso, exemplos, personalização e solução de problemas
  - Histórico de alterações para rastreabilidade

--- 