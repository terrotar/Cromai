

# Desafio Cromai


## Como Rodar o Programa

Primeiramente é necessário ter instalado o Python e o pip.

Após essa etapa, é recomendado instalar a biblioteca pipenv para gerenciar as bibliotecas e ambientes virtuais.

<code>pip install --user pipenv</code>

Em seguida, com o pipenv, crie um ambiente virtual e instale as dependências do projeto encontradas no arquivo Pipfile.

- Criar um ambiente virtual com Python 3.x(recomendado Python=3.9)

    <code>pipenv --three</code>

- Instalar dependências encontradas em Pipfile

    <code>pipenv sync</code>


Finalmente, para iniciar a aplicação é necessário utilizar o server uvicorn no terminal DENTRO DA PASTA RAIZ("cromai/"):
- <code>uvicorn app.main:app</code>


Obs:

- Caso deseje instalar as bibliotecas a parte utilizando o pip invés do pipenv é necessário inserir manualmente os pacotes encontrados no arquivo Pipfile;

- Caso o server seja inicializado de outro diretório, como por exemplo "cromai/app/", irá gerar um erro de importação de módulos.


## Rotas da API

Caso deseje uma interface mais amigável e gráfica, é possível visualizar as rotas e consumir a API através dos swaggers padrões do framework FastAPI, localizado nas URI:
- http://127.0.0.1:8000/docs e http://127.0.0.1:8000/redoc.

Há também o arquivo "curl_api.txt" dentro do diretório "/Documents" com as linhas de commando para consumir a API com comentários sobre cada uma das mesmas.

Se desejar, também é possível utilizar diretamente no navegador as rotas da API a partir da URI http://127.0.0.1:8000 :

- <a href="http://127.0.0.1:8000/upload">/upload</a>

    POST para enviar uma imagem bitmap no formato "multipart/form-data" e retorna a confirmação do upload do arquivo.

- <a href="http://127.0.0.1:8000/get-image">/get-image</a>

    GET que envia uma variável "filename" na query contendo o nome do arquivo e retorna a imagem caso ela seja encontrada.

- <a href="http://127.0.0.1:8000/write-message-on-image">/write-message-on-image</a>

    POST que envia um "application/json" com os campos "filename" e "message" e retorna o nome da nova imagem(igual ao nome anterior mas com prefix="new_") com a mensagem esteganografada.

- <a href="http://127.0.0.1:8000/decode-message-from-image">/decode-message-from-image</a>

    GET que envia uma variável "filename" na query contendo o nome do arquivo e retorna a mensagem caso ela seja encontrada.


## Testes

O arquivo "test_app.py" localizado dentro do diretório principal da aplicação("cromai/app/") é responsável pelas funções de testar as funcionalidades e respostas das rotas da API. Foi utilizado a biblioteca <code>pytest</code> para desenvolver todos testes.

Para rodar os testes é necessário iniciar o server(uvicorn) antes, ou o "Client" dos testes não irá conseguir se conectar no servidor para gerar as respostas esperadas.

Com isso, basta estar localizado DENTRO da pasta da APLICAÇÃO("cromai/app/") e rodar o seguinte comando no terminal:
- <code>pytest</code>
