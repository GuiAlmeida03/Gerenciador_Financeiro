# Gestor Financeiro Pessoal

Um sistema de gestão financeira pessoal via terminal, desenvolvido em Python, que permite controlar receitas, despesas, consultar saldo e gerar relatórios financeiros.

## Funcionalidades

- Registro de receitas e despesas
- Categorização de transações
- Consulta de saldo atual
- Visualização de transações por período, tipo ou categoria
- Geração de relatórios mensais
- Relatórios por categoria
- Persistência de dados em arquivo JSON

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/gestor-financeiro.git
   cd gestor-financeiro

2. ( Opcional ) Crie um ambiente virtual: 

python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

3. Instale as dependências:

pip install -r requirements.txt

## Utilização

Para iniciar a aplicação, execute:

python main.py

## Menu Principal

O menu principal oferece as seguintes opções:

1. Registrar transação: Adiciona uma nova receita ou despesa
2. Visualizar transações: Mostra transações existentes com várias opções de filtro
3. Gerar relatórios: Gera relatórios mensais ou por categoria
4. Consultar saldo: Exibe o saldo atual da conta
5. Sair: Encerra a aplicação

## Exemplos de Uso

Registrar uma receita

1. Selecione a opção "1" no menu principal
2. Escolha "1" para receita
3. Digite o valor (ex: 1500.50)
4. Escolha se usará a data atual ou não
5. Defina uma categoria (ex: Salário)
6. Adicione uma descrição (ex: Pagamento mensal)

Visualizar transações do mês atual

1. Selecione a opção "2" no menu principal
2. Escolha "2" para transações por período
3. Digite a data inicial (ex: 2025-05-01)
4. Digite a data final (ex: 2025-05-31)

Gerar relatório mensal

1. Selecione a opção "3" no menu principal
2. Escolha "1" para relatório mensal
3. Digite o ano (ex: 2025)
4. Digite o mês (ex: 5 para maio)

## Estrutura do Projeto

O projeto segue uma arquitetura modular com separação de responsabilidades:

gestor_financeiro/
│
├── main.py                    # Ponto de entrada da aplicação
├── README.md                  # Documentação do projeto
├── requirements.txt           # Dependências do projeto
│
├── config/                    # Configurações gerais
│   └── settings.py            # Configurações da aplicação
│
├── data/                      # Diretório para armazenamento de dados
│   └── transactions.json      # Arquivo JSON para salvar as transações
│
├── models/                    # Modelos de dados
│   ├── __init__.py            
│   ├── transaction.py         # Classe para representar transações (receitas/despesas)
│   └── account.py             # Classe para representar a conta e seu saldo
│
├── services/                  # Serviços e lógica de negócios
│   ├── __init__.py            
│   ├── file_handler.py        # Serviço para leitura/escrita de arquivos JSON
│   ├── transaction_service.py # Serviço para gerenciar transações
│   └── report_service.py      # Serviço para geração de relatórios
│
├── ui/                        # Interface de usuário
│   ├── __init__.py            
│   ├── menu.py                # Menu principal e navegação
│   └── input_handlers.py      # Funções para validação de entradas do usuário
│
└── tests/                     # Testes automatizados
    ├── __init__.py            
    ├── test_transaction.py    # Testes para a classe Transaction
    ├── test_account.py        # Testes para a classe Account
    └── test_services.py       # Testes para os serviços

## Executando os Testes

Para executar os testes automatizados, use:

python -m unittest discover tests

## Integrantes 

Guilherme Almeida - 559977

Vitor Adauto - 560247

Renato Barros - 559702
