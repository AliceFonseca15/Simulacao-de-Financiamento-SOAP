# Simulacao-de-financiamento-SOAP
Projeto desenvolvido em Java (Cliente) e Python (Servidor SOAP) para gerenciamento de veículos e simulação de financiamentos baseada em risco.
## Como executar

### Pré requesitos:
Java JDK (versão 8 ou superior).

Python 3 (com as bibliotecas flask e lxml instaladas).

### Configurando o servidor backend:

1. Instale as dependências
    
       pip install flask lxml
   
2. Execute o servidor
   
       python server.py

### Configurando o Cliente (Fronend Terminal - CLI):

1. Compile os arquivos Java na pasta src
   
       javac -d bin src/**/*.java

2. Execute a aplicação
   
       java -cp bin Main

## Funcionalidades

Listagem: Visualização de todos os veículos disponíveis.

Inserção: Cadastro de novos veículos na base de dados.

Simulação: Cálculo de financiamento

Exclusão: Remoção de veículos por ID.


