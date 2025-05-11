import unittest
from models.account import Account
from models.transaction import Transaction


class TestAccount(unittest.TestCase):
    def test_valid_account_creation(self):
        """Testa a criação de uma conta válida."""
        account = Account(initial_balance=1000.0)
        
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.transactions, [])
    
    def test_negative_initial_balance(self):
        """Testa a validação de saldo inicial negativo."""
        with self.assertRaises(ValueError):
            Account(initial_balance=-100.0)
    
    def test_add_income_transaction(self):
        """Testa a adição de uma transação de receita."""
        account = Account(initial_balance=1000.0)
        
        transaction = Transaction(
            transaction_type='receita',
            amount=500.0,
            date='2025-01-01',
            category='Salário',
            description='Pagamento mensal'
        )
        
        account.add_transaction(transaction)
        
        self.assertEqual(account.balance, 1500.0)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0], transaction)
    
    def test_add_expense_transaction(self):
        """Testa a adição de uma transação de despesa."""
        account = Account(initial_balance=1000.0)
        
        transaction = Transaction(
            transaction_type='despesa',
            amount=300.0,
            date='2025-01-01',
            category='Aluguel',
            description='Aluguel mensal'
        )
        
        account.add_transaction(transaction)
        
        self.assertEqual(account.balance, 700.0)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0], transaction)


if __name__ == '__main__':
    unittest.main()