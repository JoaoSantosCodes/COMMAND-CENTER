"""
Módulo de definição de campos editáveis
"""
from typing import List, Dict, Any

def get_editable_fields_lojas() -> List[str]:
    """
    Retorna lista de campos editáveis da tabela lojas_lojas
    
    Returns:
        List[str]: Lista de campos editáveis
    """
    return [
        'LOJAS', 'ENDEREÇO', 'BAIRRO', 'CIDADE', 'UF', 'CEP',
        'TELEFONE1', 'TELEFONE2', 'CELULAR', 'E_MAIL', '2ª_a_6ª',
        'SAB', 'DOM', 'FUNC.', 'VD_NOVO', 'NOME_GGL', 'NOME_GR'
    ]

def get_editable_fields_inventario() -> List[str]:
    """
    Retorna lista de campos editáveis da tabela inventario_planilha1
    
    Returns:
        List[str]: Lista de campos editáveis
    """
    return [
        'Status_Loja', 'Operadora', 'ID_VIVO', 'Novo_ID_Vivo',
        'Circuito_Designação', 'Novo_Circuito_Designação'
    ]

def get_field_config() -> Dict[str, Dict[str, Any]]:
    """
    Retorna configuração dos campos (validações, tipos, etc.)
    
    Returns:
        Dict[str, Dict[str, Any]]: Configuração dos campos
    """
    return {
        'LOJAS': {
            'type': 'text',
            'required': True,
            'max_length': 100,
            'description': 'Nome da loja'
        },
        'ENDEREÇO': {
            'type': 'text',
            'required': False,
            'max_length': 200,
            'description': 'Endereço completo'
        },
        'BAIRRO': {
            'type': 'text',
            'required': False,
            'max_length': 100,
            'description': 'Bairro'
        },
        'CIDADE': {
            'type': 'text',
            'required': False,
            'max_length': 100,
            'description': 'Cidade'
        },
        'UF': {
            'type': 'text',
            'required': False,
            'max_length': 2,
            'description': 'Unidade Federativa (2 letras)'
        },
        'CEP': {
            'type': 'text',
            'required': False,
            'max_length': 9,
            'description': 'CEP (formato: 00000-000)'
        },
        'TELEFONE1': {
            'type': 'text',
            'required': False,
            'max_length': 20,
            'description': 'Telefone principal'
        },
        'TELEFONE2': {
            'type': 'text',
            'required': False,
            'max_length': 20,
            'description': 'Telefone secundário'
        },
        'CELULAR': {
            'type': 'text',
            'required': False,
            'max_length': 20,
            'description': 'Celular'
        },
        'E_MAIL': {
            'type': 'email',
            'required': False,
            'max_length': 100,
            'description': 'E-mail'
        },
        '2ª_a_6ª': {
            'type': 'text',
            'required': False,
            'max_length': 50,
            'description': 'Horário de funcionamento (segunda a sexta)'
        },
        'SAB': {
            'type': 'text',
            'required': False,
            'max_length': 50,
            'description': 'Horário de funcionamento (sábado)'
        },
        'DOM': {
            'type': 'text',
            'required': False,
            'max_length': 50,
            'description': 'Horário de funcionamento (domingo)'
        },
        'FUNC.': {
            'type': 'text',
            'required': False,
            'max_length': 100,
            'description': 'Funcionário responsável'
        },
        'VD_NOVO': {
            'type': 'text',
            'required': False,
            'max_length': 50,
            'description': 'VD Novo'
        },
        'NOME_GGL': {
            'type': 'text',
            'required': False,
            'max_length': 100,
            'description': 'Nome do GGL'
        },
        'NOME_GR': {
            'type': 'text',
            'required': False,
            'max_length': 100,
            'description': 'Nome do GR'
        },
        'Status_Loja': {
            'type': 'select',
            'required': False,
            'options': ['ATIVA', 'INATIVA', 'A INAUGURAR', 'EM MANUTENÇÃO'],
            'description': 'Status da loja'
        },
        'Operadora': {
            'type': 'select',
            'required': False,
            'options': ['VIVO', 'CLARO', 'OI', 'TIM', 'OUTROS'],
            'description': 'Operadora do circuito'
        },
        'ID_VIVO': {
            'type': 'text',
            'required': False,
            'max_length': 50,
            'description': 'ID Vivo'
        },
        'Novo_ID_Vivo': {
            'type': 'text',
            'required': False,
            'max_length': 50,
            'description': 'Novo ID Vivo'
        },
        'Circuito_Designação': {
            'type': 'text',
            'required': False,
            'max_length': 100,
            'description': 'Designação do circuito'
        },
        'Novo_Circuito_Designação': {
            'type': 'text',
            'required': False,
            'max_length': 100,
            'description': 'Nova designação do circuito'
        }
    }

def get_field_display_name(field_name: str) -> str:
    """
    Retorna nome de exibição para um campo
    
    Args:
        field_name (str): Nome do campo
        
    Returns:
        str: Nome de exibição
    """
    display_names = {
        'LOJAS': 'Nome da Loja',
        'ENDEREÇO': 'Endereço',
        'BAIRRO': 'Bairro',
        'CIDADE': 'Cidade',
        'UF': 'UF',
        'CEP': 'CEP',
        'TELEFONE1': 'Telefone 1',
        'TELEFONE2': 'Telefone 2',
        'CELULAR': 'Celular',
        'E_MAIL': 'E-mail',
        '2ª_a_6ª': 'Segunda a Sexta',
        'SAB': 'Sábado',
        'DOM': 'Domingo',
        'FUNC.': 'Funcionário',
        'VD_NOVO': 'VD Novo',
        'NOME_GGL': 'GGL',
        'NOME_GR': 'GR',
        'Status_Loja': 'Status da Loja',
        'Operadora': 'Operadora',
        'ID_VIVO': 'ID Vivo',
        'Novo_ID_Vivo': 'Novo ID Vivo',
        'Circuito_Designação': 'Designação do Circuito',
        'Novo_Circuito_Designação': 'Nova Designação'
    }
    
    return display_names.get(field_name, field_name)

def get_field_validation_rules(field_name: str) -> Dict[str, Any]:
    """
    Retorna regras de validação para um campo específico
    
    Args:
        field_name (str): Nome do campo
        
    Returns:
        Dict[str, Any]: Regras de validação
    """
    validation_rules = {
        'CEP': {
            'pattern': r'^\d{5}-?\d{3}$',
            'message': 'CEP deve ter formato 00000-000'
        },
        'TELEFONE1': {
            'pattern': r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
            'message': 'Telefone deve ter formato válido'
        },
        'TELEFONE2': {
            'pattern': r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
            'message': 'Telefone deve ter formato válido'
        },
        'CELULAR': {
            'pattern': r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
            'message': 'Celular deve ter formato válido'
        },
        'E_MAIL': {
            'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'message': 'E-mail deve ter formato válido'
        },
        'UF': {
            'pattern': r'^[A-Z]{2}$',
            'message': 'UF deve ter 2 letras maiúsculas'
        }
    }
    
    return validation_rules.get(field_name, {}) 