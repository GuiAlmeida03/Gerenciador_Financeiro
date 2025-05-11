from typing import List, Dict, Any
from .transaction import Transaction


class Account:
    def __init__(self, initial_balance: float = 0.0):
        """
        Inicializa uma conta com saldo inicial.
        
        Args:
            initial_balance: Saldo inicial da conta
        """
        if initial_balance < 0:
            raise ValueError("Saldo inicial não pode ser negativo")
            
        self.balance = initial_balance
        self.transactions: List[Transaction] = []
    
    def add_transaction(self, transaction: Transaction) -> None:
        """
        Adiciona uma transação e atualiza o saldo.
        
        Args:
            transaction: Transação a ser adicionada
        """
        self.transactions.append(transaction)
        
        # Atualiza o saldo com base no tipo da transação
        if transaction.transaction_type == 'receita':
            self.balance += transaction.amount
        else:  # despesa
            self.balance -= transaction.amount
    
    def get_balance(self) -> float:
        """Retorna o saldo atual da conta."""
        return self.balance
    
    def get_transactions(self) -> List[Transaction]:
        """Retorna todas as transações da conta."""
        return self.transactions
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a conta para um dicionário."""
        return {
            'balance': self.balance,
            'transactions': [t.to_dict() for t in self.transactions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Account':
        """Cria uma instância de Account a partir de um dicionário."""
        account = cls(initial_balance=data['balance'])
        
        for transaction_data in data['transactions']:
            transaction = Transaction.from_dict(transaction_data)
            # Adiciona a transação sem modificar o saldo, pois já está contabilizado
            account.transactions.append(transaction)
            
        return account