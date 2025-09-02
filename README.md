# portal-transparencia-ro
Projeto para coleta de dados no Portal da Transparência de Rondonia

## Execução

- Instalar as dependências nas versões corretas descritas no arquivo requirements.txt
- Definir as variáveis de ambiente conforme o arquivo .env
- Rodar a API com o comando `flask --app src.api.app run`

## Schemas

**SERVIDORES**: Tabela que contém o registro de todos os servidores públicos de Rondônia.
```
id: Indentificador único do servidor no banco de dados. TIPO INTEIRO.

nome: Nome do servidor público. TIPO TEXTO.

dsccargo: Cargo do servidor público. TIPO TEXTO.

dsclotacao: Lotação do servidor público. TIPO TEXTO.
```

**REMUNERAÇÕES**: Tabela que contém informações sobre os salários dos servidores.

```commandline
codigo: Serve como identificador único. TIPO INTEIRO.

remuneracao: Remuneração base mensal do servidor. TIPO DECIMAL.

total_liquido: Salário líquido do servidor. TIPO DECIMAL.

id_servidor: Identificador do servidor, serve para relação com a tabela SERVIDORES. TIPO INTEIRO.
```

**VERBAS INDENIZATÓRIAS**: Tabela com a data e valor pago de indenizações para os servidores.
```
id: Indentificador único da indenização no banco de dados. TIPO INTEIRO.

data: Data contendo o mês/ano do pagamento da indenização, exemplo... A indenização paga em 02/06/2025 e 28/06/2025 irão constar como 01/06/2025. TIPO DATA.

lote: Categoria para o qual o dinheiro foi destinado. TIPO TEXTO.

total_pago: Total pago em indenizações. Pode conter mais de um registro por servidor por conta do campo "lote". TIPO DECIMAL.

id_servidor: Identificador do servidor, serve para relação com a tabela SERVIDORES. TIPO INTEIRO.
```
**DETALHES DAS INDENIZAÇÕES**: Tabela com mais detalhes sobre os valores pagos em indenizações.
```
id: Indentificador único da informação no banco de dados. TIPO INTEIRO.

data: Data contendo o dia/mês/ano do pagamento da indenização. TIPO DATA.

prestador: Razão Social do prestador de serviço. TIPO TEXTO.

classe: Tipo do serviço para o qual o dinheiro foi utilizado. TIPO TEXTO.

valor: Valor pago na indenização. TIPO DECIMAL.

id_verba_indenizatoria: Identificador da verba indenizatória, serve para relação com a tabela VERBAS INDENIZATÓRIAS. TIPO INTEIRO. 
```

**DIÁRIAS DEPUTADOS**: Tabela que contabiliza a quantidade de diárias dos servidores em viagens, contendo todos os detalhes das mesmas.
```commandline
id: Indentificador único da diária no banco de dados. TIPO INTEIRO.

destino: Destino da viagem. TIPO TEXTO.

finalidade: Motivo da viagem. TIPO TEXTO.

data_saida: Data de saída. TIPO DATA.

meio_transporte: Meio de transporte da viagem. TIPO TEXTO.

numero_diarias: Quantidade de diárias. TIPO INTEIRO.

valor_unitario: Valor por diária. TIPO DECIMAL.

valor_total: Valor total das diárias pagas. TIPO DECIMAL.

ordem_bancaria: Ordem bancária. TIPO TEXTO.

empenho: Empenho. TIPO TEXTO.

id_servidor: Identificador do servidor, serve para relação com a tabela SERVIDORES. TIPO INTEIRO.
```


