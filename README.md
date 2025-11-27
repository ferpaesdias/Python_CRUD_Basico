# CRUD Web em Python com Flask, SQLite e Docker

Este projeto é um exemplo simples de aplicação **CRUD (Create, Read, Update, Delete)** usando:

- **Python 3**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLite** (banco salvo no diretório `/data`)
- **Docker**

A aplicação expõe uma interface web para cadastrar, listar, editar e excluir itens.

---

## 1. Pré-requisitos

- Docker instalado  
- (Opcional) Docker Compose instalado

Você não precisa ter Python instalado na máquina host para rodar a aplicação via Docker.

---

## 2. Estrutura de diretórios

Após extrair o projeto, você terá algo como:

```text
crud-web-container/
├── app.py
├── Dockerfile
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── list_items.html
│   ├── form_item.html
│   ├── detail_item.html
│   └── confirm_delete.html
└── docker-compose.yml   (opcional, usado com Docker Compose)
```

O banco de dados SQLite será criado em:

```text
/data/items.db
```

> Dentro do container esse caminho também é `/data/items.db`.  
> Se você usar volume persistente, o diretório `./data` da sua máquina será mapeado para `/data` no container.

---

## 3. Construindo a imagem Docker

Dentro da pasta do projeto (`crud-web-container/`), execute:

```bash
docker build -t crud-web-python:0.1 .
```

- `crud-web-python` é o nome da imagem (pode mudar se quiser).
- `0.1` é a versão da sua imagem. Sempre que alterar o código do programa incremente este número.
- O `.` indica que o Dockerfile está no diretório atual.

---

## 4. Executando o container **sem volume persistente**

> Neste modo, o banco de dados ficará armazenado **apenas dentro do container**.  
> Se o container for removido, os dados serão perdidos.

```bash
docker run -d -p 5000:5000 --name crud-web crud-web-python:0.1
```

- A aplicação ficará acessível em: <http://localhost:5000/items>
- Banco de dados: `/data/items.db` **dentro do container**.

---

## 5. Executando o container **com volume persistente**

> Neste modo, o banco de dados será salvo em um diretório da sua máquina host, garantindo **persistência** mesmo se o container for removido.


```bash
docker run -d -p 5000:5000 -v $(pwd)/data:/data --name crud-web crud-web-python:0.1
```


- A pasta `./data` será criada automaticamente no diretório do projeto (se não existir).
- Dentro dela ficará o arquivo do banco: `data/items.db`.

---

## 6. Usando Docker Compose

Você também pode subir a aplicação usando **Docker Compose**.

### 6.1. Arquivo `docker-compose.yml`

Exemplo de arquivo:

```yaml
version: "3.9"

services:
  web:
    build: .
    container_name: crud-web
    ports:
      - "5000:5000"
    volumes:
      - ./data:/data
    restart: unless-stopped
```

### 6.2. Subindo a aplicação com Docker Compose

Dentro da pasta do projeto (`crud-web-container/`), execute:

```bash
docker compose up -d
```

ou, em versões mais antigas:

```bash
docker-compose up -d
```

- A imagem será construída (se ainda não existir).
- O serviço `web` será iniciado em segundo plano.
- A aplicação ficará disponível em: <http://localhost:5000/items>
- O banco será persistido em `./data/items.db`.

### 6.3. Parar e remover containers

Para parar os containers:

```bash
docker compose down
```

ou:

```bash
docker-compose down
```

Os dados continuarão salvos em `./data/items.db`, pois o volume mapeia a pasta `data` do host.

---

## 7. Resumo dos comandos principais

### Criar imagem

```bash
docker build -t crud-web-python:0.1 .
```

### Rodar sem persistência de dados

```bash
docker run -d -p 5000:5000 --name crud-web crud-web-python:0.1
```

### Rodar com volume persistente

```bash
docker run -d -p 5000:5000 -v $(pwd)/data:/data --name crud-web crud-web-python:0.1
```

### Subir com Docker Compose

```bash
docker compose up -d
```

### Parar e remover containers (Docker Compose)

```bash
docker compose down
```

---

## 8. Acessando a aplicação

Abra o navegador e acesse:

```text
http://localhost:5000/items
```

Você verá:

- Lista de itens cadastrados
- Botão para criar novo item
- Opções para editar, ver detalhes e excluir cada item

---
