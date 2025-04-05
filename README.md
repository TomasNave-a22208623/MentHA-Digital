# 🧠 MentHA – Guia de Execução e Desenvolvimento

## 🔧 Requisitos de Software

- Python 3.11 ou superior  
- Docker e Docker Compose instalados  
- Git instalado  
- Sistema operativo: Linux, macOS ou Windows  

---

## 🏗️ Arquitetura Geral do Projeto

O projeto consiste num website construído com Django, que integra três aplicações distintas:

- `diario/`: Aplicação responsável pelo registo de atividades (integra MentHA COG e MentHA CARE).
- `mentha/`: Website principal do projeto MentHA.
- `protocolo/`: Aplicação dedicada à avaliação neuropsicológica (MentHA EVAL – "Protocolo MentHA").

### Diretório principal:
```
/raiz_do_projeto
├── diario/ # Aplicação MentHA COG e CARE
├── mentha/ # Website MentHA
├── protocolo/ # Protocolo MentHA EVAL
├── manage.py
├── requirements.txt # Dependências do projeto Python
├── compose.yml # Configuração do Docker Compose
├── Dockerfile # Instruções de build da imagem da aplicação
├── dump_file.sql # Script de importação inicial da base de dados
└── .env # Variáveis de ambiente (DB, Django, etc.)
```

### Base de Dados:

A base de dados utilizada é PostgreSQL, gerida por meio de um container Docker.
Na primeira execução, é automaticamente carregado um ficheiro dump_file.sql com dados previamente definidos, garantindo que o projeto arranca com uma base de dados populada e funcional.

---

## ⚙️ Serviços Docker Compose

A aplicação é orquestrada com Docker Compose, permitindo levantar todos os componentes do projeto com um único comando. Este sistema garante que os serviços necessários são iniciados na ordem correta e com as dependências satisfeitas.

### Funções principais do Docker Compose no projeto:

1.	Inicia e configura a base de dados PostgreSQL com persistência de dados.
2.	Executa um script SQL inicial (dump_file.sql) para carregar dados base na primeira execução.
3.	Constrói a imagem da aplicação Django, instala dependências, aplica migrações e lança o servidor.
4.	Garante a ordem de arranque correta entre os serviços (ex: o servidor Django só arranca após a base de dados estar disponível).

### Serviços definidos:

`dbpostgresql`:

Executa o container oficial do PostgreSQL, com base nas variáveis de ambiente definidas no .env.
Um volume persistente (postgres_data) assegura que os dados são mantidos entre reinícios.

`dbpostgresql_init`:

Container temporário responsável por importar o ficheiro dump_file.sql com dados iniciais para a base de dados.
Este serviço depende do dbpostgresql e apenas é executado após a base de dados estar operacional.

`web`:

Serviço principal da aplicação Django.
Constrói a imagem com base no Dockerfile, instala as dependências (via pip), executa as migrações e inicia o servidor de desenvolvimento.
Inclui as três apps: diario, mentha e protocolo.

---

## 🔄 Configurar Projeto Localmente com Docker Compose

### 1. Clonar o Repositório

- ```git clone <link_do_repositorio>```

- ```cd <diretorio_do_projeto>```

- ```code .```

![image](https://github.com/user-attachments/assets/f491478c-76ff-4fb3-a57e-04256f589e29)

### 2. Preparar os Ficheiros

Certifique-se de que está presente:
-	docker-compose.yml
- dump_file.sql

### 3. Criar Ficheiros `.env`

