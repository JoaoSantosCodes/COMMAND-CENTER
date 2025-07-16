"""
Módulo de validação de informativos e regras
"""
import re
from typing import Dict, List, Tuple

def validar_informativo_regras(texto: str) -> Dict[str, any]:
    """
    Valida informativo baseado em regras predefinidas
    
    Args:
        texto (str): Texto do informativo
        
    Returns:
        Dict[str, any]: Resultado da validação
    """
    resultado = {
        'valido': True,
        'erros': [],
        'avisos': [],
        'pontuacao': 0,
        'max_pontuacao': 100
    }
    
    # Verificar se o texto não está vazio
    if not texto or len(texto.strip()) < 10:
        resultado['valido'] = False
        resultado['erros'].append("Texto muito curto (mínimo 10 caracteres)")
        resultado['pontuacao'] -= 20
    
    # Verificar se contém informações essenciais
    palavras_chave = ['loja', 'circuito', 'operadora', 'status', 'impacto']
    palavras_encontradas = []
    
    for palavra in palavras_chave:
        if palavra.lower() in texto.lower():
            palavras_encontradas.append(palavra)
            resultado['pontuacao'] += 10
    
    if len(palavras_encontradas) < 2:
        resultado['valido'] = False
        resultado['erros'].append("Faltam informações essenciais (loja, circuito, operadora, status, impacto)")
        resultado['pontuacao'] -= 30
    
    # Verificar formatação
    if not re.search(r'\*\*.*\*\*', texto):
        resultado['avisos'].append("Considere usar **negrito** para destacar informações importantes")
        resultado['pontuacao'] -= 5
    
    # Verificar se tem estrutura clara
    if not re.search(r'[A-Z][^.!?]*[.!?]', texto):
        resultado['avisos'].append("Verifique a estrutura das frases")
        resultado['pontuacao'] -= 5
    
    # Verificar se tem informações de contato
    if re.search(r'\b\d{2,3}[-\s]?\d{4,5}[-\s]?\d{4}\b', texto):
        resultado['pontuacao'] += 15
    else:
        resultado['avisos'].append("Considere incluir informações de contato")
    
    # Verificar se tem horários
    if re.search(r'\b\d{1,2}:\d{2}\b', texto):
        resultado['pontuacao'] += 10
    else:
        resultado['avisos'].append("Considere incluir horários de funcionamento")
    
    # Verificar se tem endereço
    if re.search(r'\b(rua|avenida|av\.|r\.|alameda|praça)\b', texto, re.IGNORECASE):
        resultado['pontuacao'] += 10
    else:
        resultado['avisos'].append("Considere incluir endereço completo")
    
    # Ajustar pontuação final
    resultado['pontuacao'] = max(0, min(100, resultado['pontuacao']))
    
    return resultado

def validar_informativo_ia(texto: str) -> Dict[str, any]:
    """
    Valida informativo usando IA (simulação)
    
    Args:
        texto (str): Texto do informativo
        
    Returns:
        Dict[str, any]: Resultado da validação
    """
    # Simulação de validação por IA
    resultado = {
        'valido': True,
        'erros': [],
        'avisos': [],
        'pontuacao': 0,
        'max_pontuacao': 100,
        'sugestoes_ia': []
    }
    
    # Análise de sentimento básica
    palavras_positivas = ['funcionando', 'ativo', 'normal', 'resolvido', 'ok']
    palavras_negativas = ['problema', 'erro', 'falha', 'inativo', 'quebrado']
    
    texto_lower = texto.lower()
    score_positivo = sum(1 for palavra in palavras_positivas if palavra in texto_lower)
    score_negativo = sum(1 for palavra in palavras_negativas if palavra in texto_lower)
    
    if score_negativo > score_positivo:
        resultado['sugestoes_ia'].append("O texto parece indicar problemas. Considere ser mais específico sobre o status.")
    
    # Análise de clareza
    frases = re.split(r'[.!?]+', texto)
    frases_longas = [f for f in frases if len(f.split()) > 20]
    
    if len(frases_longas) > 2:
        resultado['sugestoes_ia'].append("Considere quebrar frases muito longas para melhor compreensão.")
    
    # Análise de completude
    elementos_essenciais = {
        'localização': ['loja', 'endereço', 'cidade', 'bairro'],
        'técnico': ['circuito', 'operadora', 'equipamento'],
        'temporal': ['horário', 'data', 'duração'],
        'contato': ['telefone', 'email', 'responsável']
    }
    
    for categoria, palavras in elementos_essenciais.items():
        encontrados = sum(1 for palavra in palavras if palavra in texto_lower)
        if encontrados == 0:
            resultado['sugestoes_ia'].append(f"Considere incluir informações de {categoria}.")
        elif encontrados >= 2:
            resultado['pontuacao'] += 10
    
    # Pontuação baseada na análise
    resultado['pontuacao'] = min(100, resultado['pontuacao'] + 50)
    
    return resultado

def gerar_template_informativo(tipo_incidente: str) -> str:
    """
    Gera template de informativo baseado no tipo de incidente
    
    Args:
        tipo_incidente (str): Tipo do incidente
        
    Returns:
        str: Template do informativo
    """
    templates = {
        'rede': """
**INCIDENTE DE REDE - {data}**

**LOJA:** {loja}
**CIRCUITO:** {circuito}
**OPERADORA:** {operadora}

**SINTOMA:**
{descricao_sintoma}

**IMPACTO:**
{impacto}

**STATUS ATUAL:**
{status}

**HORÁRIO DE FUNCIONAMENTO:**
Segunda a Sexta: {horario_semana}
Sábado: {horario_sabado}
Domingo: {horario_domingo}

**CONTATOS:**
Telefone: {telefone}
E-mail: {email}

**RESPONSÁVEL:**
{responsavel}
""",
        
        'equipamento': """
**MANUTENÇÃO DE EQUIPAMENTO - {data}**

**LOJA:** {loja}
**EQUIPAMENTO:** {equipamento}
**TIPO DE MANUTENÇÃO:** {tipo_manutencao}

**DESCRIÇÃO:**
{descricao}

**IMPACTO:**
{impacto}

**STATUS:**
{status}

**HORÁRIO DE FUNCIONAMENTO:**
Segunda a Sexta: {horario_semana}
Sábado: {horario_sabado}
Domingo: {horario_domingo}

**CONTATOS:**
Telefone: {telefone}
E-mail: {email}

**RESPONSÁVEL:**
{responsavel}
""",
        
        'geral': """
**INFORMATIVO GERAL - {data}**

**LOJA:** {loja}
**TIPO:** {tipo}

**DESCRIÇÃO:**
{descricao}

**IMPACTO:**
{impacto}

**STATUS:**
{status}

**HORÁRIO DE FUNCIONAMENTO:**
Segunda a Sexta: {horario_semana}
Sábado: {horario_sabado}
Domingo: {horario_domingo}

**CONTATOS:**
Telefone: {telefone}
E-mail: {email}

**RESPONSÁVEL:**
{responsavel}
"""
    }
    
    return templates.get(tipo_incidente.lower(), templates['geral'])

def validar_telefone(telefone: str) -> Tuple[bool, str]:
    """
    Valida formato de telefone
    
    Args:
        telefone (str): Número de telefone
        
    Returns:
        Tuple[bool, str]: (é_válido, mensagem)
    """
    if not telefone:
        return True, ""
    
    # Remover caracteres não numéricos
    numeros = re.sub(r'\D', '', telefone)
    
    if len(numeros) == 10 or len(numeros) == 11:
        return True, ""
    else:
        return False, "Telefone deve ter 10 ou 11 dígitos"

def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida formato de email
    
    Args:
        email (str): Endereço de email
        
    Returns:
        Tuple[bool, str]: (é_válido, mensagem)
    """
    if not email:
        return True, ""
    
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(padrao, email):
        return True, ""
    else:
        return False, "Email deve ter formato válido"

def validar_cep(cep: str) -> Tuple[bool, str]:
    """
    Valida formato de CEP
    
    Args:
        cep (str): CEP
        
    Returns:
        Tuple[bool, str]: (é_válido, mensagem)
    """
    if not cep:
        return True, ""
    
    # Remover caracteres não numéricos
    numeros = re.sub(r'\D', '', cep)
    
    if len(numeros) == 8:
        return True, ""
    else:
        return False, "CEP deve ter 8 dígitos"

def validar_uf(uf: str) -> Tuple[bool, str]:
    """
    Valida formato de UF
    
    Args:
        uf (str): UF
        
    Returns:
        Tuple[bool, str]: (é_válido, mensagem)
    """
    if not uf:
        return True, ""
    
    ufs_validas = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    
    if uf.upper() in ufs_validas:
        return True, ""
    else:
        return False, "UF deve ser uma sigla válida de estado brasileiro" 