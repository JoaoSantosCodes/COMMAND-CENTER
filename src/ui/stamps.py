"""
Módulo de geração de carimbos para chamados
"""
from datetime import datetime
from typing import Optional

def generate_incident_stamp(sintoma: str, abrangencia: str, impacto: str, 
                           descricao_impacto: str, horario_inicio: str, 
                           horario_termino: str, status: str) -> str:
    """
    Gera carimbo para abertura de chamados
    
    Args:
        sintoma (str): Descrição do sintoma
        abrangencia (str): Abrangência do incidente
        impacto (str): Tipo de impacto
        descricao_impacto (str): Descrição detalhada do impacto
        horario_inicio (str): Horário de início
        horario_termino (str): Horário de término
        status (str): Status atual
        
    Returns:
        str: Carimbo formatado
    """
    # Formatar horários
    try:
        inicio = datetime.strptime(horario_inicio, "%H:%M").strftime("%H:%M")
        termino = datetime.strptime(horario_termino, "%H:%M").strftime("%H:%M")
    except:
        inicio = horario_inicio
        termino = horario_termino
    
    # Data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    # Gerar carimbo
    carimbo = f"""
🔴 **INCIDENTE - {data_atual}**

📋 **SINTOMA:**
{sintoma}

🌍 **ABRANGÊNCIA:**
{abrangencia}

⚡ **IMPACTO:**
{impacto}

📝 **DESCRIÇÃO DO IMPACTO:**
{descricao_impacto}

🕒 **HORÁRIO:**
Início: {inicio}
Término: {termino}

📊 **STATUS:**
{status}

---
*Carimbo gerado automaticamente pelo sistema ConsultaVD*
"""
    
    return carimbo.strip()

def generate_contact_stamp(nome: str, telefone: str, email: str, 
                          cargo: str = "", loja: str = "") -> str:
    """
    Gera carimbo de contato
    
    Args:
        nome (str): Nome do contato
        telefone (str): Telefone
        email (str): E-mail
        cargo (str, optional): Cargo/função
        loja (str, optional): Loja relacionada
        
    Returns:
        str: Carimbo de contato formatado
    """
    carimbo = f"""
👤 **CONTATO**

📛 **Nome:** {nome}
📞 **Telefone:** {telefone}
📧 **E-mail:** {email}
"""
    
    if cargo:
        carimbo += f"💼 **Cargo:** {cargo}\n"
    
    if loja:
        carimbo += f"🏪 **Loja:** {loja}\n"
    
    carimbo += "\n---\n*Carimbo gerado automaticamente pelo sistema ConsultaVD*"
    
    return carimbo.strip()

def generate_maintenance_stamp(loja: str, tipo_manutencao: str, 
                              descricao: str, responsavel: str = "") -> str:
    """
    Gera carimbo de manutenção
    
    Args:
        loja (str): Nome da loja
        tipo_manutencao (str): Tipo de manutenção
        descricao (str): Descrição da manutenção
        responsavel (str, optional): Responsável pela manutenção
        
    Returns:
        str: Carimbo de manutenção formatado
    """
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    carimbo = f"""
🔧 **MANUTENÇÃO - {data_atual}**

🏪 **LOJA:**
{loja}

🔧 **TIPO DE MANUTENÇÃO:**
{tipo_manutencao}

📝 **DESCRIÇÃO:**
{descricao}
"""
    
    if responsavel:
        carimbo += f"\n👤 **RESPONSÁVEL:**\n{responsavel}"
    
    carimbo += "\n\n---\n*Carimbo gerado automaticamente pelo sistema ConsultaVD*"
    
    return carimbo.strip()

def generate_network_stamp(circuito: str, operadora: str, status: str, 
                          loja: str = "", descricao: str = "") -> str:
    """
    Gera carimbo de rede/circuito
    
    Args:
        circuito (str): Designação do circuito
        operadora (str): Operadora
        status (str): Status do circuito
        loja (str, optional): Loja relacionada
        descricao (str, optional): Descrição adicional
        
    Returns:
        str: Carimbo de rede formatado
    """
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    carimbo = f"""
🌐 **CIRCUITO - {data_atual}**

🔗 **CIRCUITO:**
{circuito}

📡 **OPERADORA:**
{operadora}

📊 **STATUS:**
{status}
"""
    
    if loja:
        carimbo += f"\n🏪 **LOJA:**\n{loja}"
    
    if descricao:
        carimbo += f"\n📝 **DESCRIÇÃO:**\n{descricao}"
    
    carimbo += "\n\n---\n*Carimbo gerado automaticamente pelo sistema ConsultaVD*"
    
    return carimbo.strip()

def generate_summary_stamp(lojas_afetadas: list, tipo_incidente: str, 
                          abrangencia: str, impacto: str) -> str:
    """
    Gera carimbo de resumo de incidente
    
    Args:
        lojas_afetadas (list): Lista de lojas afetadas
        tipo_incidente (str): Tipo do incidente
        abrangencia (str): Abrangência
        impacto (str): Impacto
        
    Returns:
        str: Carimbo de resumo formatado
    """
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    carimbo = f"""
📊 **RESUMO DE INCIDENTE - {data_atual}**

🔴 **TIPO DE INCIDENTE:**
{tipo_incidente}

🌍 **ABRANGÊNCIA:**
{abrangencia}

⚡ **IMPACTO:**
{impacto}

🏪 **LOJAS AFETADAS ({len(lojas_afetadas)}):**
"""
    
    for i, loja in enumerate(lojas_afetadas, 1):
        carimbo += f"{i}. {loja}\n"
    
    carimbo += "\n---\n*Carimbo gerado automaticamente pelo sistema ConsultaVD*"
    
    return carimbo.strip()

def format_phone_number(phone: str) -> str:
    """
    Formata número de telefone para exibição
    
    Args:
        phone (str): Número de telefone
        
    Returns:
        str: Número formatado
    """
    if not phone or phone == "N/A":
        return "N/A"
    
    # Remover caracteres não numéricos
    clean_phone = ''.join(filter(str.isdigit, str(phone)))
    
    if len(clean_phone) == 11:
        return f"({clean_phone[:2]}) {clean_phone[2:7]}-{clean_phone[7:]}"
    elif len(clean_phone) == 10:
        return f"({clean_phone[:2]}) {clean_phone[2:6]}-{clean_phone[6:]}"
    else:
        return phone

def format_address(endereco: str, bairro: str, cidade: str, uf: str, cep: str) -> str:
    """
    Formata endereço completo
    
    Args:
        endereco (str): Endereço
        bairro (str): Bairro
        cidade (str): Cidade
        uf (str): UF
        cep (str): CEP
        
    Returns:
        str: Endereço formatado
    """
    parts = []
    
    if endereco and endereco != "N/A":
        parts.append(endereco)
    
    if bairro and bairro != "N/A":
        parts.append(bairro)
    
    if cidade and cidade != "N/A":
        parts.append(cidade)
    
    if uf and uf != "N/A":
        parts.append(uf)
    
    if cep and cep != "N/A":
        parts.append(f"CEP: {cep}")
    
    return ", ".join(parts) if parts else "Endereço não informado" 