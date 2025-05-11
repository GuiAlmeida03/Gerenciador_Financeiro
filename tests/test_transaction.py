import unittest
from datetime import datetime
from models.transaction import Transaction


class TestTransaction(unittest.TestCase):
    def test_valid_transaction_creation(self):
        """Testa a criação de uma transação válida."""
        transaction = Transaction(
            transaction_type='receita',
            amount=100.0,
            date='2025-01-01',
            category='Salário',
            description='Pagamento mensal'
        )
        
        self.assertEqual(transaction.transaction_type, 'receita')
        self.assertEqual(transaction.amount, 100.0)
        self.assertEqual(transaction.date, '2025-01-01')
        self.assertEqual(transaction.category, 'Salário')
        self.assertEqual(transaction.description, 'Pagamento mensal')
    
    def test_invalid_transaction_type(self):
        """Testa a validação de tipo de transação inválido."""
        with self.assertRaises(ValueError):
            Transaction(
                transaction_type='investimento',  # Tipo inválido
                amount=100.0
            )
    
    def test_invalid_amount(self):
        """Testa a validação de valor inválido."""
        with self.assertRaises(ValueError):
            Transaction(
                transaction_type='receita',
                amount=0  # Valor inválido
            )
            
        with self.assertRaises(ValueError):
            Transaction(
                transaction_type='receita',
                amount=-50  # Valor inválido
            )
    
    def test_invalid_date_format(self):
        """Testa a validação de formato de data inválido."""
        with self.assertRaises(ValueError):
            Transaction(
                transaction_type='receita',
                amount=100.0,
                date='01/01/2025'  # Formato inválido
            )
    
    def test_default_date(self):
        """Testa a data padrão quando não é fornecida."""
        transaction = Transaction(
            transaction_type='receita',
            amount=100.0
        )
        
        # Verifica se a data é a atual no formato YYYY-MM-DD
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(transaction.date, today)


if __name__ == '__main__':
    unittest.main()