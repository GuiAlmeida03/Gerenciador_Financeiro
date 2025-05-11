import unittest
import os
import tempfile
from datetime import datetime

from models.transaction import Transaction
from services.file_handler import FileHandler
from services.transaction_service import TransactionService
from services.report_service import ReportService


class TestFileHandler(unittest.TestCase):
    def setUp(self):
        """Configuração para cada teste."""
        # Cria um arquivo temporário para os testes
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, 'test_data.json')
        self.file_handler = FileHandler(self.temp_file)
    
    def tearDown(self):
        """Limpeza após cada teste."""
        self.temp_dir.cleanup()
    
    def test_save_and_load_data(self):
        """Testa a salvamento e carregamento de dados."""
        test_data = {'test': 'data', 'number': 123}
        
        # Salva os dados
        self.file_handler.save_data(test_data)
        
        # Carrega os dados
        loaded_data = self.file_handler.load_data()
        
        # Verifica se os dados carregados são iguais aos salvos
        self.assertEqual(loaded_data, test_data)
    
    def test_load_nonexistent_file(self):
        """Testa o carregamento de um arquivo inexistente."""
        # Remove o arquivo temporário
        os.remove(self.temp_file)
        
        # Carrega dados de um arquivo inexistente
        loaded_data = self.file_handler.load_data()
        
        # Verifica se retorna um dicionário vazio
        self.assertEqual(loaded_data, {})


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        """Configuração para cada teste."""
        # Cria um arquivo temporário para os testes
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, 'test_data.json')
        self.file_handler = FileHandler(self.temp_file)
        self.transaction_service = TransactionService(self.file_handler)
    
    def tearDown(self):
        """Limpeza após cada teste."""
        self.temp_dir.cleanup()
    
    def test_add_transaction(self):
        """Testa a adição de uma transação."""
        transaction = Transaction(
            transaction_type='receita',
            amount=100.0,
            date='2025-01-01',
            category='Salário',
            description='Pagamento mensal'
        )
        
        # Adiciona a transação
        self.transaction_service.add_transaction(transaction)
        
        # Verifica se a transação foi adicionada
        transactions = self.transaction_service.get_all_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].transaction_type, 'receita')
        self.assertEqual(transactions[0].amount, 100.0)
        
        # Verifica se o saldo foi atualizado
        self.assertEqual(self.transaction_service.get_balance(), 100.0)
    
    def test_get_transactions_by_period(self):
        """Testa a obtenção de transações por período."""
        # Adiciona transações em diferentes datas
        transaction1 = Transaction(
            transaction_type='receita',
            amount=100.0,
            date='2025-01-01'
        )
        
        transaction2 = Transaction(
            transaction_type='despesa',
            amount=50.0,
            date='2025-02-01'
        )
        
        transaction3 = Transaction(
            transaction_type='receita',
            amount=200.0,
            date='2025-03-01'
        )
        
        self.transaction_service.add_transaction(transaction1)
        self.transaction_service.add_transaction(transaction2)
        self.transaction_service.add_transaction(transaction3)
        
        # Obtém transações de janeiro a fevereiro
        transactions = self.transaction_service.get_transactions_by_period(
            '2025-01-01', '2025-02-28'
        )
        
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].date, '2025-01-01')
        self.assertEqual(transactions[1].date, '2025-02-01')
    
    def test_get_transactions_by_type(self):
        """Testa a obtenção de transações por tipo."""
        # Adiciona transações de diferentes tipos
        transaction1 = Transaction(
            transaction_type='receita',
            amount=100.0
        )
        
        transaction2 = Transaction(
            transaction_type='despesa',
            amount=50.0
        )
        
        transaction3 = Transaction(
            transaction_type='receita',
            amount=200.0
        )
        
        self.transaction_service.add_transaction(transaction1)
        self.transaction_service.add_transaction(transaction2)
        self.transaction_service.add_transaction(transaction3)
        
        # Obtém receitas
        receitas = self.transaction_service.get_transactions_by_type('receita')
        self.assertEqual(len(receitas), 2)
        
        # Obtém despesas
        despesas = self.transaction_service.get_transactions_by_type('despesa')
        self.assertEqual(len(despesas), 1)


class TestReportService(unittest.TestCase):
    def setUp(self):
        """Configuração para cada teste."""
        # Cria um arquivo temporário para os testes
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, 'test_data.json')
        self.file_handler = FileHandler(self.temp_file)
        self.transaction_service = TransactionService(self.file_handler)
        self.report_service = ReportService(self.transaction_service)
        
        # Adiciona algumas transações para os testes
        self.transaction_service.add_transaction(Transaction(
            transaction_type='receita',
            amount=1000.0,
            date='2025-01-15',
            category='Salário',
            description='Pagamento mensal'
        ))
        
        self.transaction_service.add_transaction(Transaction(
            transaction_type='despesa',
            amount=300.0,
            date='2025-01-20',
            category='Aluguel',
            description='Aluguel mensal'
        ))
        
        self.transaction_service.add_transaction(Transaction(
            transaction_type='despesa',
            amount=150.0,
            date='2025-01-25',
            category='Alimentação',
            description='Compras do mês'
        ))
        
        self.transaction_service.add_transaction(Transaction(
            transaction_type='receita',
            amount=500.0,
            date='2025-02-05',
            category='Freelance',
            description='Projeto de design'
        ))
    
    def tearDown(self):
        """Limpeza após cada teste."""
        self.temp_dir.cleanup()
    
    def test_generate_monthly_report(self):
        """Testa a geração de relatório mensal."""
        # Gera relatório para janeiro de 2025
        report = self.report_service.generate_monthly_report(2025, 1)
        
        # Verifica os totais
        self.assertEqual(report['total_income'], 1000.0)
        self.assertEqual(report['total_expense'], 450.0)
        self.assertEqual(report['balance'], 550.0)
        
        # Verifica as categorias
        self.assertEqual(report['income_by_category'], {'Salário': 1000.0})
        self.assertEqual(report['expense_by_category'], {'Aluguel': 300.0, 'Alimentação': 150.0})
        
        # Verifica as transações incluídas
        self.assertEqual(len(report['transactions']), 3)
    
    def test_generate_category_report(self):
        """Testa a geração de relatório por categoria."""
        # Gera relatório de despesas por categoria
        report = self.report_service.generate_category_report('despesa')
        
        # Verifica as categorias
        self.assertEqual(report, {'Aluguel': 300.0, 'Alimentação': 150.0})


if __name__ == '__main__':
    unittest.main()