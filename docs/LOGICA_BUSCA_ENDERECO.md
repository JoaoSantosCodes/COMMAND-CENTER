# Lógica e Processo de Busca por Endereço (Unificada)

## Visão Geral
A busca por endereço no sistema ConsultaVD permite localizar lojas a partir de qualquer parte do endereço, bairro ou cidade, exibindo os dados completos e padronizados da loja.

---

## 1. Relacionamento entre Tabelas
- **lojas_lojas**: A busca é feita diretamente na tabela de lojas, sem necessidade de JOIN com inventário.
- Os campos pesquisados são: `ENDEREÇO`, `BAIRRO`, `CIDADE`.

---

## 2. Lógica da Busca
- O backend executa uma query SQL buscando por qualquer correspondência parcial nos campos de endereço, bairro ou cidade.
- Todos os campos relevantes da loja são retornados já padronizados:
  - `LOJAS`, `CODIGO`, `Status_Loja`, `ENDEREÇO`, `BAIRRO`, `CIDADE`, `UF`, `CEP`, `TELEFONE1`, `TELEFONE2`, `CELULAR`, `E_MAIL`, `VD NOVO`, `People/PEOP`, `STATUS`, `NOME_GGL`, `NOME_GR`
- O frontend exibe os dados completos da loja, sem necessidade de fallback ou tratamento especial.

---

## 3. Fluxo da Busca por Endereço
1. O usuário informa parte do endereço, bairro ou cidade no frontend.
2. O frontend chama o endpoint `/api/search/address?address=...`.
3. O backend executa a query diretamente na tabela de lojas.
4. O frontend exibe os dados completos da(s) loja(s) encontrada(s).

---

## 4. Resultados
- Busca por endereço exibe corretamente os dados completos das lojas encontradas.
- Integração frontend-backend padronizada e robusta.
- Não há necessidade de fallback, pois a busca é feita diretamente na tabela de lojas.
- Documentação e lógica registradas para futuras manutenções.

---

**Processo registrado em junho/2024.** 