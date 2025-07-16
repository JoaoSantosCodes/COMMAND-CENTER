# RELATÓRIO DE ESTRUTURA DE DADOS - CONSULTAVD
Gerado em: 25/06/2025 18:13:00
================================================================================

## RESUMO EXECUTIVO

**Total de tabelas:** 3
- inventario_planilha1: 5,370 registros
- lojas_lojas: 1,927 registros
- lojas_ggl_gr: 91 registros
**Total de registros:** 7,388

## TABELA: INVENTARIO_PLANILHA1

**Total de registros:** 5,370

### Estrutura das Colunas

| Campo | Tipo | Not Null | Default | Primary Key |
|-------|------|----------|---------|-------------|
| Status_Loja | TEXT | ✗ | NULL | ✗ |
| People | TEXT | ✗ | NULL | ✗ |
| NOME | TEXT | ✗ | NULL | ✗ |
| CENTRO_DE_CUSTO | REAL | ✗ | NULL | ✗ |
| Operadora | TEXT | ✗ | NULL | ✗ |
| Contrato | TEXT | ✗ | NULL | ✗ |
| Circuito_Designação | TEXT | ✗ | NULL | ✗ |
| Novo_Circuito_Designação | TEXT | ✗ | NULL | ✗ |
| Velocidade | TEXT | ✗ | NULL | ✗ |
| Serviço | TEXT | ✗ | NULL | ✗ |
| ID_VIVO | TEXT | ✗ | NULL | ✗ |
| Novo_ID_Vivo | TEXT | ✗ | NULL | ✗ |
| Status_Serviço | TEXT | ✗ | NULL | ✗ |
| Observação | TEXT | ✗ | NULL | ✗ |
| Custo | TEXT | ✗ | NULL | ✗ |
| Multa | TEXT | ✗ | NULL | ✗ |

### Análise de Dados

**Amostra de dados (primeiros 5 registros):**

```
Status_Loja       People  NOME  CENTRO_DE_CUSTO Operadora      Contrato Circuito_Designação Novo_Circuito_Designação Velocidade       Serviço ID_VIVO Novo_ID_Vivo Status_Serviço                         Observação   Custo Multa
      ATIVA DSP915 CD BA CD BA     2009150205.0 VIVO LINK    0449910291     714070182090894          714070182090894     100 MB      DEDICADO 1596614      1596614          ATIVO                               None 3889.42  None
      ATIVA DSP915 CD BA CD BA     2009150205.0       ITS não informado        LFS-CEA-7994             LFS-CEA-7994     100 MB      DEDICADO       -            -          ATIVO                               None    None  None
      ATIVA DSP915 CD BA CD BA     2009150205.0        OI   16450023468             5175921                  5175921        N/P GERENCIAMENTO       -            -      CANCELADO  PC20240718002103/PC20250326001080  220.89  None
      ATIVA DSP915 CD BA CD BA     2009150205.0        OI  161601621839             5079928                  5079928       4 MB      DEDICADO       -            -      CANCELADO                   PC20250326001098       -  None
      ATIVA DSP915 CD BA CD BA     2009150205.0        OI  212700013615             5102261                  5102261      50 MB      DEDICADO       -            -      CANCELADO PC20240718002103/ PC20250326001100  999.62  None
```

**Contagem de valores únicos por coluna:**

- **Status_Loja**: 2 valores únicos (0.0% de 5,370 não-nulos)
- **People**: 1,710 valores únicos (31.8% de 5,370 não-nulos)
- **NOME**: 1,703 valores únicos (31.7% de 5,364 não-nulos)
- **CENTRO_DE_CUSTO**: 1,598 valores únicos (30.0% de 5,326 não-nulos)
- **Operadora**: 46 valores únicos (0.9% de 5,369 não-nulos)
- **Contrato**: 290 valores únicos (5.5% de 5,270 não-nulos)
- **Circuito_Designação**: 5,320 valores únicos (99.4% de 5,351 não-nulos)
- **Novo_Circuito_Designação**: 5,318 valores únicos (99.1% de 5,366 não-nulos)
- **Velocidade**: 35 valores únicos (0.7% de 5,366 não-nulos)
- **Serviço**: 20 valores únicos (0.4% de 5,366 não-nulos)

--------------------------------------------------------------------------------

## TABELA: LOJAS_LOJAS

**Total de registros:** 1,927

### Estrutura das Colunas

| Campo | Tipo | Not Null | Default | Primary Key |
|-------|------|----------|---------|-------------|
| STATUS | TEXT | ✗ | NULL | ✗ |
| POLÍTICA_COML. | INTEGER | ✗ | NULL | ✗ |
| CODIGO | INTEGER | ✗ | NULL | ✗ |
| PEOP | TEXT | ✗ | NULL | ✗ |
| LOJAS | TEXT | ✗ | NULL | ✗ |
| REGIAO_GGL | TEXT | ✗ | NULL | ✗ |
| REGIAO_GR | TEXT | ✗ | NULL | ✗ |
| REGIAO_DIV | TEXT | ✗ | NULL | ✗ |
| NOME_GGL | TEXT | ✗ | NULL | ✗ |
| NOME_GR | TEXT | ✗ | NULL | ✗ |
| NOME_DIV | TEXT | ✗ | NULL | ✗ |
| REGIAO_IM | TEXT | ✗ | NULL | ✗ |
| ENDEREÇO | TEXT | ✗ | NULL | ✗ |
| BAIRRO | TEXT | ✗ | NULL | ✗ |
| CIDADE | TEXT | ✗ | NULL | ✗ |
| UF | TEXT | ✗ | NULL | ✗ |
| CEP | TEXT | ✗ | NULL | ✗ |
| Latitude | TEXT | ✗ | NULL | ✗ |
| Longitude | TEXT | ✗ | NULL | ✗ |
| ESCOAMENTO | TEXT | ✗ | NULL | ✗ |
| NOME_DA_FACHADA | TEXT | ✗ | NULL | ✗ |
| INAUG. | TEXT | ✗ | NULL | ✗ |
| SAFRA | TEXT | ✗ | NULL | ✗ |
| CLUSTER | TEXT | ✗ | NULL | ✗ |
| CLUSTER_
ABREV. | TEXT | ✗ | NULL | ✗ |
| PARCELAMENTO | TEXT | ✗ | NULL | ✗ |
| CLUSTER_DE_
PARCELAMENTO | TEXT | ✗ | NULL | ✗ |
| TELEFONE1 | TEXT | ✗ | NULL | ✗ |
| TELEFONE2 | TEXT | ✗ | NULL | ✗ |
| CELULAR | TEXT | ✗ | NULL | ✗ |
| E_MAIL | TEXT | ✗ | NULL | ✗ |
| 2ª_a_6ª | TEXT | ✗ | NULL | ✗ |
| SAB | TEXT | ✗ | NULL | ✗ |
| DOM | TEXT | ✗ | NULL | ✗ |
| FUNC. | TEXT | ✗ | NULL | ✗ |
| TIPO_LOJA | TEXT | ✗ | NULL | ✗ |
| FACHADA | TEXT | ✗ | NULL | ✗ |
| PSICOTRÓPICOS | TEXT | ✗ | NULL | ✗ |
| FARMÁCIA_POP. | TEXT | ✗ | NULL | ✗ |
| SERVIÇOS
_FARMACEUTICOS | TEXT | ✗ | NULL | ✗ |
| VACINAS | TEXT | ✗ | NULL | ✗ |
| IFOOD | TEXT | ✗ | NULL | ✗ |
| RAPPI | TEXT | ✗ | NULL | ✗ |
| CORNER_SHOP | TEXT | ✗ | NULL | ✗ |
| SUPER_EXPRESSA | TEXT | ✗ | NULL | ✗ |
| VAGAS_ESTACIONAMENTO | TEXT | ✗ | NULL | ✗ |
| BICICLETARIO | TEXT | ✗ | NULL | ✗ |
| PDVs_ATIVOS | TEXT | ✗ | NULL | ✗ |
| IMOBILIÁRIO | TEXT | ✗ | NULL | ✗ |
| CD_SUPRIDOR | TEXT | ✗ | NULL | ✗ |
| INSCR._ESTADUAL | TEXT | ✗ | NULL | ✗ |
| CNPJ | TEXT | ✗ | NULL | ✗ |
| CENTRO_DE_CUSTOS | TEXT | ✗ | NULL | ✗ |
| VD_NOVO | TEXT | ✗ | NULL | ✗ |
| DATA_DA_UNIFICAÇAO | TEXT | ✗ | NULL | ✗ |
| CNPJ_NOVO | TEXT | ✗ | NULL | ✗ |
| DATA_INATIVAÇAO | TEXT | ✗ | NULL | ✗ |
| REALOCAÇÃO | TEXT | ✗ | NULL | ✗ |
| DATA_DA_VIRADA | TEXT | ✗ | NULL | ✗ |
| EAC | TEXT | ✗ | NULL | ✗ |
| DENGUE_COVID | TEXT | ✗ | NULL | ✗ |
| INJETAVEIS | TEXT | ✗ | NULL | ✗ |
| REFORMA | TEXT | ✗ | NULL | ✗ |

### Análise de Dados

**Amostra de dados (primeiros 5 registros):**

```
     STATUS  POLÍTICA_COML.  CODIGO  PEOP                         LOJAS         REGIAO_GGL      REGIAO_GR REGIAO_DIV         NOME_GGL         NOME_GR     NOME_DIV REGIAO_IM                   ENDEREÇO              BAIRRO  CIDADE UF      CEP Latitude Longitude ESCOAMENTO    NOME_DA_FACHADA              INAUG. SAFRA CLUSTER CLUSTER_\nABREV.                  PARCELAMENTO CLUSTER_DE_\nPARCELAMENTO TELEFONE1 TELEFONE2 CELULAR                  E_MAIL  2ª_a_6ª      SAB      DOM    FUNC. TIPO_LOJA FACHADA PSICOTRÓPICOS FARMÁCIA_POP. SERVIÇOS\n_FARMACEUTICOS VACINAS IFOOD RAPPI CORNER_SHOP SUPER_EXPRESSA VAGAS_ESTACIONAMENTO BICICLETARIO PDVs_ATIVOS IMOBILIÁRIO CD_SUPRIDOR INSCR._ESTADUAL               CNPJ CENTRO_DE_CUSTOS VD_NOVO DATA_DA_UNIFICAÇAO CNPJ_NOVO DATA_INATIVAÇAO REALOCAÇÃO DATA_DA_VIRADA     EAC DENGUE_COVID INJETAVEIS REFORMA
A INAUGURAR            9999    1854 L1854         DP CABO FRIO PORTINHO                  -              -          -                -               -            -         -                          -                   -       -  -        -        -         -          -                  -                   -     -       -                -                             -                    PADRÃO         -         -       -                      --        -        -        -        -         -       -             -             -                  INATIVO INATIVO     -     -           -              -                    -            -           -           -           -               -                  -                -       -                  -         -               -          -              - INATIVO      INATIVO    INATIVO       -
A INAUGURAR            9999    2600 L2600    DSP ENGORDADOURO - JUNDIAI                  -              -          -                -               -            -         -                          -                   -       -  -       --        -         -          -                  -                   -     -    AR_G               AR Parcela minima de 60 e até 3X                    PADRÃO         -         -       -                      --        -        -        -        -         -       -             -             -                  INATIVO INATIVO     -     -           -              -                    -            -           -           -           -               -                  -                -       -                  -         -               -          -              - INATIVO      INATIVO    INATIVO       -
      ATIVA            9999    2601 L2601 DSP GUARUJA ADHEMAR DE BARROS   SP LITORAL NORTE SP LITORAL+ABC        SUL ROGERIO CARVALHO     ALLAN YOUNG BRUNA COSTA          - AV ADHEMAR DE BARROS, 2105 JARDIM HELENA MARIA GUARUJA SP 11430003        -         -          - DROGARIA SAO PAULO 2025-04-30 00:00:00  2025   CBR_G              CBR Parcela minima de 40 e até 3X                    PADRÃO         -         -       - filial.2601@dpsp.com.br 24 HORAS 24 HORAS 24 HORAS 24 HORAS         -       -             -             -                  INATIVO INATIVO     -     -           -              -                    -            -           -           -         910    335708545116 61.412.110/0323-59       2026010000       -                  -         -            None        NÃO              - INATIVO      INATIVO    INATIVO       -
A INAUGURAR            9999    2599 L2599         DSP TARTARUGA GUARUJA                  -              -          -                -               -            -         -                          -                   -       -  -       --        -         -          -                  -                   -     -   CBR_G              CBR Parcela minima de 40 e até 3X                    PADRÃO         -         -       -                      --        -        -        -        -         -       -             -             -                  INATIVO INATIVO     -     -           -              -                    -            -           -           -           -               -                  -                -       -                  -         -               -          -              - INATIVO      INATIVO    INATIVO       -
A INAUGURAR            9999    2598 L2598            DSP VILA APARECIDA SP VALE DO PARAIBA    SP INTERIOR          - FERNANDA ROBERTA ANDERSON SANTOS            -         -                          -                   -       -  -       --        -         -          -                  -                   -     -    AR_G               AR Parcela minima de 60 e até 3X                    PADRÃO         -         -       -                      --        -        -        -        -         -       -             -             -                  INATIVO INATIVO     -     -           -              -                    -            -           -           -         910               -                  -                -       -                  -         -               -          -              - INATIVO      INATIVO    INATIVO       -
```

**Contagem de valores únicos por coluna:**

- **STATUS**: 3 valores únicos (0.2% de 1,927 não-nulos)
- **POLÍTICA_COML.**: 193 valores únicos (10.0% de 1,927 não-nulos)
- **CODIGO**: 1,927 valores únicos (100.0% de 1,927 não-nulos)
- **PEOP**: 1,927 valores únicos (100.0% de 1,927 não-nulos)
- **LOJAS**: 1,927 valores únicos (100.0% de 1,927 não-nulos)
- **REGIAO_GGL**: 95 valores únicos (4.9% de 1,927 não-nulos)
- **REGIAO_GR**: 13 valores únicos (0.7% de 1,927 não-nulos)
- **REGIAO_DIV**: 4 valores únicos (0.2% de 1,927 não-nulos)
- **NOME_GGL**: 92 valores únicos (4.8% de 1,927 não-nulos)
- **NOME_GR**: 13 valores únicos (0.7% de 1,927 não-nulos)

--------------------------------------------------------------------------------

## TABELA: LOJAS_GGL_GR

**Total de registros:** 91

### Estrutura das Colunas

| Campo | Tipo | Not Null | Default | Primary Key |
|-------|------|----------|---------|-------------|
| REGIÃO_GGL | TEXT | ✗ | NULL | ✗ |
| NOME_GGL | TEXT | ✗ | NULL | ✗ |
| CELULAR | TEXT | ✗ | NULL | ✗ |
| E_MAIL | TEXT | ✗ | NULL | ✗ |
| GR | TEXT | ✗ | NULL | ✗ |
| USUÁRIO_PEOPLE | TEXT | ✗ | NULL | ✗ |
| LISTA_DE_PERMISSÃO | TEXT | ✗ | NULL | ✗ |
| Unnamed:_7 | REAL | ✗ | NULL | ✗ |
| REGIÃO_GR | TEXT | ✗ | NULL | ✗ |
| NOME_GR | TEXT | ✗ | NULL | ✗ |
| CELULAR.1 | TEXT | ✗ | NULL | ✗ |
| EMAIL | TEXT | ✗ | NULL | ✗ |

### Análise de Dados

**Amostra de dados (primeiros 5 registros):**

```
            REGIÃO_GGL         NOME_GGL         CELULAR                       E_MAIL          GR   USUÁRIO_PEOPLE LISTA_DE_PERMISSÃO Unnamed:_7           REGIÃO_GR        NOME_GR      CELULAR.1                      EMAIL
SP SAO JOSE DOS CAMPOS GLEDSON FLORIANO  (12)99787-5391 gledson.floriano@dpsp.com.br SP INTERIOR  GLEDSONFLORIANO           PPVDSP38       None        CENTRO OESTE    DAISY TOSTA (61)99666-6761  daisy.martins@dpsp.com.br
            SP ATIBAIA  JAQUELINE AMATI (16) 99741-0782  jaqueline.amati@dpsp.com.br SP INTERIOR                -           PPVDSP05       None               MINAS VERONICA GOMES (31)99926-2814 veronica.gomes@dpsp.com.br
    SP VALE DO PARAIBA FERNANDA ROBERTA  (12)99716-8465 fernanda.roberta@dpsp.com.br SP INTERIOR FERNANDACLAUDINO           PPVDSP70       None            NORDESTE THIRZA FREITAS (19)99130-9363 thirza.freitas@dpsp.com.br
  SP IGUATEMI CAMPINAS MARILEY TOMAZINI  (11)95630-8823  mariley.conrado@dpsp.com.br SP INTERIOR MARILEY.TOMAZINI           PPVDSP80       None          RJ BAIXADA  RODRIGO ROCHA (21)97156-4232 rodrigo.rsouza@dpsp.com.br
                SP ITU    RAFAEL MIGUEL   11)99194-5836    rafael.miguel@dpsp.com.br SP INTERIOR     RAFAELMIGUEL           PPVDSP54       None RJ ZONA SUL+NITEROI LUDMILA ARAUJO (31)97164-4168 ludmila.araujo@dpsp.com.br
```

**Contagem de valores únicos por coluna:**

- **REGIÃO_GGL**: 91 valores únicos (100.0% de 91 não-nulos)
- **NOME_GGL**: 90 valores únicos (98.9% de 91 não-nulos)
- **CELULAR**: 84 valores únicos (92.3% de 91 não-nulos)
- **E_MAIL**: 88 valores únicos (97.8% de 90 não-nulos)
- **GR**: 11 valores únicos (12.1% de 91 não-nulos)
- **USUÁRIO_PEOPLE**: 85 valores únicos (95.5% de 89 não-nulos)
- **LISTA_DE_PERMISSÃO**: 89 valores únicos (98.9% de 90 não-nulos)
- **REGIÃO_GR**: 14 valores únicos (100.0% de 14 não-nulos)
- **NOME_GR**: 14 valores únicos (100.0% de 14 não-nulos)

--------------------------------------------------------------------------------

## RELACIONAMENTOS IDENTIFICADOS

**Relacionamento People/PEOP:**
- Registros com match: 4,922
- Total inventário: 5,370
- Taxa de match: 91.7%

**Lojas por Região GGL:**
- -: 269 lojas
- RJ LAGOS: 23 lojas
- RJ CAMPO GRANDE: 23 lojas
- MG OESTE BH: 23 lojas
- ES VITORIA: 23 lojas
- SP SAO JOSE DOS CAMPOS: 22 lojas
- RJ SAO GONCALO NITEROI: 22 lojas
- RJ NOVA IGUACU: 22 lojas
- RJ NITEROI OCEANICA: 22 lojas
- SP SOROCABA: 21 lojas

**Status das Lojas:**
- ATIVA: 1,632 lojas
- INATIVA: 264 lojas
- A INAUGURAR: 31 lojas

## RECOMENDAÇÕES

1. **Validação de Dados:**
   - Verificar consistência entre People e PEOP
   - Validar coordenadas geográficas
   - Confirmar CNPJs únicos

2. **Otimizações:**
   - Criar índices para campos de busca frequente
   - Implementar constraints para integridade
   - Normalizar dados duplicados

3. **Monitoramento:**
   - Acompanhar crescimento dos dados
   - Verificar qualidade dos dados regularmente
   - Manter backup atualizado
