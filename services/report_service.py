from typing import List, Dict, Any
from datetime import datetime

from services.transaction_service import TransactionService
from models.transaction import Transaction


class ReportService:
    def __init__(self, transaction_service: TransactionService):
        """
        Inicializa o serviço de relatórios.
        
        Args:
            transaction_service: Serviço de transações
        """
        self.transaction_service = transaction_service
    
    def generate_monthly_report(self, year: int, month: int) -> Dict[str, Any]:
        """
        Gera um relatório mensal.
        
        Args:
            year: Ano do relatório
            month: Mês do relatório (1-12)
            
        Returns:
            Dicionário com os dados do relatório
        """
        # Cria as datas de início e fim do mês
        start_date = f"{year}-{month:02d}-01"
        
        # Determina o último dia do mês
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
            
        end_date = f"{next_year}-{next_month:02d}-01"
        
        # Obtém as transações do período
        transactions = self.transaction_service.get_transactions_by_period(start_date, end_date)
        
        # Separa receitas e despesas
        incomes = [t for t in transactions if t.transaction_type == 'receita']
        expenses = [t for t in transactions if t.transaction_type == 'despesa']
        
        # Calcula totais
        total_income = sum(t.amount for t in incomes)
        total_expense = sum(t.amount for t in expenses)
        balance = total_income - total_expense
        
        # Agrupa por categoria
        income_by_category = self._group_by_category(incomes)
        expense_by_category = self._group_by_category(expenses)
        
        return {
            'period': f"{year}-{month:02d}",
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'income_by_category': income_by_category,
            'expense_by_category': expense_by_category,
            'transactions': transactions
        }
    
    def generate_category_report(self, transaction_type: str) -> Dict[str, float]:
        """
        Gera um relatório de gastos ou receitas por categoria.
        
        Args:
            transaction_type: Tipo de transação ('receita' ou 'despesa')
            
        Returns:
            Dicionário com categorias e seus valores totais
        """
        transactions = self.transaction_service.get_transactions_by_type(transaction_type)
        return self._group_by_category(transactions)
    
    def _group_by_category(self, transactions: List[Transaction]) -> Dict[str, float]:
        """
        Agrupa transações por categoria.
        
        Args:
            transactions: Lista de transações
            
        Returns:
            Dicionário com categorias e seus valores totais
        """
        categories = {}
        
        for transaction in transactions:
            category = transaction.category if transaction.category else "Sem categoria"
            
            if category in categories:
                categories[category] += transaction.amount
            else:
                categories[category] = transaction.amount
                
        return categories