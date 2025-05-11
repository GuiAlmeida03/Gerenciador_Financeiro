from typing import Dict, Any, List, Callable
from datetime import datetime

from models.transaction import Transaction
from services.transaction_service import TransactionService
from services.report_service import ReportService
from ui.input_handlers import (
    get_float_input, get_date_input, get_transaction_type, 
    get_menu_option, get_valid_input
)


class Menu:
    def __init__(self, transaction_service: TransactionService, report_service: ReportService):
        """
        Inicializa o menu com os serviços necessários.
        
        Args:
            transaction_service: Serviço de transações
            report_service: Serviço de relatórios
        """
        self.transaction_service = transaction_service
        self.report_service = report_service
        self.running = True
        
    def display_main_menu(self) -> None:
        """Exibe o menu principal."""
        print("\n===== GESTOR FINANCEIRO PESSOAL =====")
        print(f"Saldo atual: R$ {self.transaction_service.get_balance():.2f}")
        print("1. Registrar transação")
        print("2. Visualizar transações")
        print("3. Gerar relatórios")
        print("4. Consultar saldo")
        print("0. Sair")
    
    def handle_main_menu(self) -> None:
        """Gerencia a interação com o menu principal."""
        self.display_main_menu()
        option = get_menu_option(4)
        
        if option == 0:
            self.running = False
            print("Obrigado por usar o Gestor Financeiro Pessoal. Até logo!")
        elif option == 1:
            self.register_transaction()
        elif option == 2:
            self.view_transactions_menu()
        elif option == 3:
            self.reports_menu()
        elif option == 4:
            self.check_balance()
    
    def register_transaction(self) -> None:
        """Registra uma nova transação."""
        print("\n===== REGISTRAR TRANSAÇÃO =====")
        
        transaction_type = get_transaction_type()
        amount = get_float_input("Valor: R$ ")
        
        # Data é opcional, usa a data atual se não for fornecida
        use_current_date = get_valid_input("Usar data atual? (S/N): ", 
                                           lambda x: x.upper() in ['S', 'N'], 
                                           "Por favor, digite S ou N.")
        
        if use_current_date.upper() == 'S':
            date = None
        else:
            date = get_date_input("Data (YYYY-MM-DD): ")
        
        category = input("Categoria: ")
        description = input("Descrição: ")
        
        try:
            transaction = Transaction(
                transaction_type=transaction_type,
                amount=amount,
                date=date,
                category=category,
                description=description
            )
            
            self.transaction_service.add_transaction(transaction)
            print(f"\nTransação registrada com sucesso! Novo saldo: R$ {self.transaction_service.get_balance():.2f}")
            
        except ValueError as e:
            print(f"Erro ao registrar transação: {e}")
    
    def view_transactions_menu(self) -> None:
        """Exibe o menu de visualização de transações."""
        print("\n===== VISUALIZAR TRANSAÇÕES =====")
        print("1. Todas as transações")
        print("2. Transações por período")
        print("3. Receitas")
        print("4. Despesas")
        print("5. Transações por categoria")
        print("0. Voltar")
        
        option = get_menu_option(5)
        
        if option == 0:
            return
        elif option == 1:
            self.view_all_transactions()
        elif option == 2:
            self.view_transactions_by_period()
        elif option == 3:
            self.view_transactions_by_type('receita')
        elif option == 4:
            self.view_transactions_by_type('despesa')
        elif option == 5:
            self.view_transactions_by_category()
    
    def view_all_transactions(self) -> None:
        """Exibe todas as transações."""
        transactions = self.transaction_service.get_all_transactions()
        self._display_transactions(transactions, "TODAS AS TRANSAÇÕES")
    
    def view_transactions_by_period(self) -> None:
        """Exibe transações em um período específico."""
        print("\nInforme o período:")
        start_date = get_date_input("Data inicial (YYYY-MM-DD): ")
        end_date = get_date_input("Data final (YYYY-MM-DD): ")
        
        transactions = self.transaction_service.get_transactions_by_period(start_date, end_date)
        self._display_transactions(transactions, f"TRANSAÇÕES DE {start_date} A {end_date}")
    
    def view_transactions_by_type(self, transaction_type: str) -> None:
        """
        Exibe transações de um tipo específico.
        
        Args:
            transaction_type: Tipo de transação ('receita' ou 'despesa')
        """
        transactions = self.transaction_service.get_transactions_by_type(transaction_type)
        title = "RECEITAS" if transaction_type == 'receita' else "DESPESAS"
        self._display_transactions(transactions, title)
    
    def view_transactions_by_category(self) -> None:
        """Exibe transações de uma categoria específica."""
        category = input("\nInforme a categoria: ")
        transactions = self.transaction_service.get_transactions_by_category(category)
        self._display_transactions(transactions, f"TRANSAÇÕES DA CATEGORIA: {category}")
    
    def _display_transactions(self, transactions: List[Transaction], title: str) -> None:
        """
        Exibe uma lista de transações.
        
        Args:
            transactions: Lista de transações a serem exibidas
            title: Título da listagem
        """
        print(f"\n===== {title} =====")
        
        if not transactions:
            print("Nenhuma transação encontrada.")
            return
        
        print(f"{'TIPO':<10} {'DATA':<12} {'VALOR (R$)':<12} {'CATEGORIA':<15} {'DESCRIÇÃO':<30}")
        print("-" * 80)
        
        for transaction in transactions:
            transaction_type = "RECEITA" if transaction.transaction_type == 'receita' else "DESPESA"
            print(f"{transaction_type:<10} {transaction.date:<12} {transaction.amount:<12.2f} "
                  f"{transaction.category[:15]:<15} {transaction.description[:30]:<30}")
        
        print("-" * 80)
        print(f"Total: {len(transactions)} transação(ões)")
    
    def reports_menu(self) -> None:
        """Exibe o menu de relatórios."""
        print("\n===== RELATÓRIOS =====")
        print("1. Relatório mensal")
        print("2. Relatório por categorias")
        print("0. Voltar")
        
        option = get_menu_option(2)
        
        if option == 0:
            return
        elif option == 1:
            self.monthly_report()
        elif option == 2:
            self.category_report()
    
    def monthly_report(self) -> None:
        """Gera e exibe um relatório mensal."""
        print("\nInforme o mês e ano para o relatório:")
        
        def validate_year(value: str) -> bool:
            try:
                year = int(value)
                return 2000 <= year <= 2100
            except ValueError:
                return False
        
        year_str = get_valid_input("Ano (YYYY): ", validate_year, "Por favor, insira um ano válido entre 2000 e 2100.")
        year = int(year_str)
        
        def validate_month(value: str) -> bool:
            try:
                month = int(value)
                return 1 <= month <= 12
            except ValueError:
                return False
        
        month_str = get_valid_input("Mês (1-12): ", validate_month, "Por favor, insira um mês válido entre 1 e 12.")
        month = int(month_str)
        
        report = self.report_service.generate_monthly_report(year, month)
        
        print(f"\n===== RELATÓRIO MENSAL: {report['period']} =====")
        print(f"Total de receitas: R$ {report['total_income']:.2f}")
        print(f"Total de despesas: R$ {report['total_expense']:.2f}")
        print(f"Saldo do período: R$ {report['balance']:.2f}")
        
        print("\nReceitas por categoria:")
        for category, amount in report['income_by_category'].items():
            print(f"  {category}: R$ {amount:.2f}")
        
        print("\nDespesas por categoria:")
        for category, amount in report['expense_by_category'].items():
            print(f"  {category}: R$ {amount:.2f}")
        
        view_transactions = get_valid_input("\nDeseja visualizar as transações deste período? (S/N): ", 
                                           lambda x: x.upper() in ['S', 'N'], 
                                           "Por favor, digite S ou N.")
        
        if view_transactions.upper() == 'S':
            self._display_transactions(report['transactions'], f"TRANSAÇÕES DE {report['period']}")
    
    def category_report(self) -> None:
        """Gera e exibe um relatório por categorias."""
        print("\nEscolha o tipo de transação:")
        print("1. Receitas")
        print("2. Despesas")
        
        option = get_menu_option(2)
        
        if option == 0:
            return
            
        transaction_type = 'receita' if option == 1 else 'despesa'
        report = self.report_service.generate_category_report(transaction_type)
        
        title = "RECEITAS" if transaction_type == 'receita' else "DESPESAS"
        print(f"\n===== {title} POR CATEGORIA =====")
        
        if not report:
            print(f"Nenhuma {title.lower()[:-1]} encontrada.")
            return
        
        total = sum(report.values())
        
        for category, amount in report.items():
            percentage = (amount / total) * 100
            print(f"{category}: R$ {amount:.2f} ({percentage:.1f}%)")
        
        print(f"\nTotal: R$ {total:.2f}")
    
    def check_balance(self) -> None:
        """Exibe o saldo atual."""
        balance = self.transaction_service.get_balance()
        print(f"\n===== SALDO ATUAL =====")
        print(f"R$ {balance:.2f}")
    
    def run(self) -> None:
        """Executa o loop principal do menu."""
        while self.running:
            self.handle_main_menu()