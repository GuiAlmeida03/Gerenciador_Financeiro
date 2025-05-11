import os

# Diretório raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Diretório de dados
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Arquivo de transações
DATA_FILE_PATH = os.path.join(DATA_DIR, 'transactions.json')