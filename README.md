# API de Gerenciamento de Jogos

Este projeto consiste em uma API REST desenvolvida com Flask para controle de um catálogo de jogos. A aplicação permite manipular dados armazenados em um banco SQLite por meio de requisições HTTP.

---

## Finalidade

O sistema foi criado com o objetivo de aplicar conceitos de CRUD (Create, Read, Update e Delete) em uma API, utilizando Python e boas práticas de organização.

---

## Configuração do ambiente

1. Clonar o repositório:
git clone URL_DO_REPOSITORIO

2. Entrar na pasta do projeto:
cd projeto-api

3. Criar ambiente virtual:
python -m venv venv

4. Ativar:

Windows:
venv\Scripts\activate

5. Instalar dependências:
pip install flask

---

## Banco de Dados

Para criar o banco de dados, execute:

python init_db.py

Isso criará o arquivo `games.db` com a tabela necessária.

---

## Executando a aplicação

Rodar o servidor:

python app.py

A API estará disponível em:
http://localhost:5000/

---

## Endpoints

- GET /games → retorna todos os jogos  
- GET /games/{id} → retorna um jogo específico  
- POST /games → adiciona um novo jogo  
- PUT /games/{id} → atualiza um jogo  
- DELETE /games/{id} → remove um jogo  

---

## Exemplos

Adicionar:
curl -X POST http://127.0.0.1:5000/games -H "Content-Type: application/json" -d "{\"titulo\":\"GTA\",\"estoque\":5,\"valor\":100}"

Listar:
curl http://127.0.0.1:5000/games

---

## Tecnologias

- Python
- Flask
- SQLite

---

## Observações

A API funciona sem interface gráfica, sendo acessada via ferramentas como Postman ou terminal.

---

## Resultado

O projeto implementa um CRUD completo com estrutura simples, permitindo manipulação eficiente de dados e servindo como base para aplicações maiores.