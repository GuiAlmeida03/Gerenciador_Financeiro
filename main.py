import os
from config.settings import DATA_FILE_PATH
from services.file_handler import FileHandler
from services.transaction_service import TransactionService
from services.report_service import ReportService
from ui.menu import Menu


def main():
    """Função principal que inicia a aplicação."""
    try:
        # Cria o diretório de dados se não existir
        data_dir = os.path.dirname(DATA_FILE_PATH)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Inicializa os serviços
        file_handler = FileHandler(DATA_FILE_PATH)
        transaction_service = TransactionService(file_handler)
        report_service = ReportService(transaction_service)
        
        # Inicializa e executa o menu
        menu = Menu(transaction_service, report_service)
        menu.run()
        
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")
        raise


if __name__ == "__main__":
    main()