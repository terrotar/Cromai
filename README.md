

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


## Sobre

O desafio foi realizado buscando seguir as exigências do Case localizado na pasta "/Documents". Foi extremamente desafiador realizar esse projeto, principalmente pelo fato de eu nunca ter manipulado imagens ou outros arquivos em nível de bytes e bits. O tema do desafio foi muito legal como esperado da Cromai, o que novamente me auxiliou e incentivou durante todo meu processo de desenvolvimento, assim como meus dois gatos fazendo bagunça durante o andamento da aplicação.

A esteganografia é um método relativamente simples e com um poder muito alto, fiquei impressionado com o resultado das imagens com as mensagens embutidas. Tive grande dificuldade na parte de inserir e retirar as mensagens secretas, tendo um longo tempo ai de muitos testes e "brincadeiras" com as manipulações de bytes/bits. Conforme os dias foram passando fui me familiarizando cada vez mais com o formato da proposta do desafio, tendo conseguido realizar de fato o resultado que desejava na madrugada do ultimo dia. Esse em dúvida nenhuma foi o teste mais difícil e de fé que tive desde o início de meus estudos, a persistência de continuar tentando acho que foi o que mais obtive de valor ao finalizar o teste.

Estou estudando há algum tempo o FastAPI, um framework que gostei muito do formato e proposta dele e decidi por deenvolver utilizando o mesmo pois além de suas funcionalidades serem muito eficientes e claras, ainda vem com o bônus incrível de ter duas opções de swagger e todo código implementado segundo o OpenAPI. Poderia ter explorado mais ainda o framework usando e abusando das funções <code>async</code> mas por conta do tempo que demorei para completar os requisitos do desafio não consegui fazer essas implementações.

As imagens foram transformadas em escala cinza para uma melhor e mais fácil decodificação das mensagens embutidas. Além disso, em todas imagens geradas com mensagens foi adicionado o prefixo "new_", facilitando e padronizando assim as imagens alteradas das originais. Todos os arquivos são salvos em um diretório temporário criado a cada vez que o server é iniciado e deletado toda vez em que é encerrado, garantindo assim que nenhuma imagem e/ou mensagem fique armazenada como a proposta do Case.

Os testes realizados não são muitos mas eles contemplam toda a aplicação na sua totalidade, com testes bem sucedidos e mal-sucedidos, inputs corretos e errados.

Muito obrigado pela oportunidade de poder participar novamente de outro processo seletivo da Cromai, e pelo mais divertido background de desafio que já existiu. Cresci e me aprimorei muito com o teste e fiquei muito feliz com o resultado obtido.

Viva a revolução contra a ditadura dos gatos!


---

# Heroku

O projeto foi subido para o Heroku no link <link>https://cromaistegano.herokuapp.com</link>


# Docker

Adicionado Dockerfile e publicado o container com nome <strong>cromaistegano</strong> o qual pode ser encontrado no DockerHub https://hub.docker.com/ e utilizado através do comando:
- docker pull terrotar/cromaistegano:version1
