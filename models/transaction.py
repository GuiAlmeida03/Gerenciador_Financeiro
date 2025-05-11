from datetime import datetime
from typing import Dict, Any


class Transaction:
    def __init__(self, transaction_type: str, amount: float, date: str = None, 
                 category: str = "", description: str = ""):
        """
        Inicializa uma nova transação.
        
        Args:
            transaction_type: Tipo da transação ('receita' ou 'despesa')
            amount: Valor da transação (positivo)
            date: Data da transação (formato: YYYY-MM-DD)
            category: Categoria da transação
            description: Descrição da transação
        """
        if transaction_type not in ['receita', 'despesa']:
            raise ValueError("Tipo de transação deve ser 'receita' ou 'despesa'")
        
        if amount <= 0:
            raise ValueError("Valor da transação deve ser positivo")
            
        self.transaction_type = transaction_type
        self.amount = amount
        
        # Se a data não for fornecida, usa a data atual
        if date is None:
            self.date = datetime.now().strftime("%Y-%m-%d")
        else:
            # Valida o formato da data
            try:
                datetime.strptime(date, "%Y-%m-%d")
                self.date = date
            except ValueError:
                raise ValueError("Formato de data inválido. Use YYYY-MM-DD")
        
        self.category = category
        self.description = description
        
    def to_dict(self) -> Dict[str, Any]:
        """Converte a transação para um dicionário."""
        return {
            'type': self.transaction_type,
            'amount': self.amount,
            'date': self.date,
            'category': self.category,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Cria uma instância de Transaction a partir de um dicionário."""
        return cls(
            transaction_type=data['type'],
            amount=data['amount'],
            date=data['date'],
            category=data['category'],
            description=data['description']
        )