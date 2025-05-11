from datetime import datetime
from typing import Optional, Any, Callable


def get_valid_input(prompt: str, validation_func: Callable[[str], bool], 
                     error_message: str) -> str:
    """
    Obtém uma entrada do usuário com validação.
    
    Args:
        prompt: Mensagem a ser exibida para o usuário
        validation_func: Função de validação
        error_message: Mensagem de erro para entradas inválidas
        
    Returns:
        Entrada validada do usuário
    """
    while True:
        user_input = input(prompt)
        
        if validation_func(user_input):
            return user_input
        
        print(error_message)


def get_float_input(prompt: str, min_value: float = 0.0) -> float:
    """
    Obtém um valor float do usuário.
    
    Args:
        prompt: Mensagem a ser exibida para o usuário
        min_value: Valor mínimo aceitável
        
    Returns:
        Valor float validado
    """
    def validate(value: str) -> bool:
        try:
            float_val = float(value)
            return float_val > min_value
        except ValueError:
            return False
    
    error_message = f"Por favor, insira um número válido maior que {min_value}."
    value_str = get_valid_input(prompt, validate, error_message)
    
    return float(value_str)


def get_date_input(prompt: str) -> str:
    """
    Obtém uma data no formato YYYY-MM-DD do usuário.
    
    Args:
        prompt: Mensagem a ser exibida para o usuário
        
    Returns:
        Data no formato YYYY-MM-DD
    """
    def validate(value: str) -> bool:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    error_message = "Por favor, insira uma data válida no formato YYYY-MM-DD."
    return get_valid_input(prompt, validate, error_message)


def get_transaction_type() -> str:
    """
    Obtém o tipo de transação do usuário.
    
    Returns:
        Tipo de transação ('receita' ou 'despesa')
    """
    def validate(value: str) -> bool:
        return value.lower() in ['1', '2']
    
    error_message = "Por favor, digite 1 para receita ou 2 para despesa."
    option = get_valid_input("Tipo (1 - Receita, 2 - Despesa): ", validate, error_message)
    
    return 'receita' if option == '1' else 'despesa'


def get_menu_option(max_option: int) -> int:
    """
    Obtém uma opção de menu do usuário.
    
    Args:
        max_option: Número máximo de opções no menu
        
    Returns:
        Número da opção escolhida
    """
    def validate(value: str) -> bool:
        try:
            option = int(value)
            return 0 <= option <= max_option
        except ValueError:
            return False
    
    error_message = f"Por favor, digite um número entre 0 e {max_option}."
    option_str = get_valid_input("Escolha uma opção: ", validate, error_message)
    
    return int(option_str)