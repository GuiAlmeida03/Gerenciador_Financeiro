from datetime import datetime
from typing import List, Dict, Any, Optional

from models.transaction import Transaction
from models.account import Account
from services.file_handler import FileHandler


class TransactionService:
    def __init__(self, file_handler: FileHandler):
        """
        Inicializa o serviço de transações.
        
        Args:
            file_handler: Manipulador de arquivo para persistência
        """
        self.file_handler = file_handler
        self.account = self._load_account()
    
    def _load_account(self) -> Account:
        """
        Carrega a conta do arquivo ou cria uma nova se não existir.
        
        Returns:
            Instância de Account carregada ou nova
        """
        data = self.file_handler.load_data()
        
        if data:
            return Account.from_dict(data)
        else:
            return Account()
    
    def _save_account(self) -> None:
        """Salva a conta atual no arquivo."""
        self.file_handler.save_data(self.account.to_dict())
    
    def add_transaction(self, transaction: Transaction) -> None:
        """
        Adiciona uma nova transação.
        
        Args:
            transaction: Transação a ser adicionada
        """
        self.account.add_transaction(transaction)
        self._save_account()
    
    def get_balance(self) -> float:
        """
        Obtém o saldo atual.
        
        Returns:
            Saldo atual da conta
        """
        return self.account.get_balance()
    
    def get_all_transactions(self) -> List[Transaction]:
        """
        Obtém todas as transações.
        
        Returns:
            Lista de todas as transações
        """
        return self.account.get_transactions()
    
    def get_transactions_by_period(self, start_date: str, end_date: str) -> List[Transaction]:
        """
        Obtém transações em um período específico.
        
        Args:
            start_date: Data inicial (formato: YYYY-MM-DD)
            end_date: Data final (formato: YYYY-MM-DD)
            
        Returns:
            Lista de transações no período especificado
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        return [
            transaction for transaction in self.account.get_transactions()
            if start <= datetime.strptime(transaction.date, "%Y-%m-%d") <= end
        ]
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        """
        Obtém transações de um tipo específico.
        
        Args:
            transaction_type: Tipo de transação ('receita' ou 'despesa')
            
        Returns:
            Lista de transações do tipo especificado
        """
        return [
            transaction for transaction in self.account.get_transactions()
            if transaction.transaction_type == transaction_type
        ]
    
    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        """
        Obtém transações de uma categoria específica.
        
        Args:
            category: Categoria das transações
            
        Returns:
            Lista de transações da categoria especificada
        """
        return [
            transaction for transaction in self.account.get_transactions()
            if transaction.category == category
        ]