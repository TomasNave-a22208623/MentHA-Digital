# 🧠 MentHA – Guia de Instalação e Execução 

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

A base de dados utilizada é PostgreSQL, gerida por um container Docker.
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

- ```git clone https://github.com/MentHA-ULHT/mentha_digital/```

- ```cd <diretorio_do_projeto>```

- ```code .```

![image](https://github.com/user-attachments/assets/f491478c-76ff-4fb3-a57e-04256f589e29)

---

### 2. Preparar os Ficheiros
Certifique-se de que está presente:
-	docker-compose.yml
- dump_file.sql

---

### 3. Criar Ficheiros `.env`
Colocar no ficheiro estas informações:
```
POSTGRES_USER=leda
POSTGRES_PASSWORD=AiraeZeech6Bis
POSTGRES_DB=mentha

PGUSER=leda
PGPASSWORD=AiraeZeech6Bis
PGDB=mentha

POSTGRES_HOST=dbpostgresql
POSTGRES_PORT=5432
```
![image](https://github.com/user-attachments/assets/434e44ea-11b4-4b21-826f-99aa77b982b1)

---

### 4. Inicializar os Serviços pela Primeira Vez (um a um)
Este passo é necessário apenas uma vez, para criar e preparar os serviços. Esta configuração inicial faz o seguinte:
- Cria os containers necessários (base de dados, app Django)
- Importa os dados iniciais da base de dados (dump_file.sql)
- Inicia o servidor de desenvolvimento Django com as aplicações integradas
#### a) Iniciar a base de dados
```docker compose up dbpostgresql```

![image](https://github.com/user-attachments/assets/68ef3362-7c83-468d-873e-6915df994ace)

Isto vai criar e executar o container da base de dados PostgreSQL. Os dados são armazenados num volume persistente (chamado postgres_data), que garante que a base de dados mantém a sua informação mesmo após paragens ou reinícios do container.

#### b) Importar ficheiro SQL
```docker compose up dbpostgresql_init```

![image](https://github.com/user-attachments/assets/9d7f9a1b-7915-4581-810c-824a6f4abddb)

Este é um container temporário que se liga ao container da base de dados e importa o conteúdo do dump_file.sql. Este passo só é necessário na primeira execução do projeto ou caso queira se dar reset à base de dados.

#### c) Iniciar a aplicação Django
```docker compose up web```

![image](https://github.com/user-attachments/assets/feaade1e-94e6-4a5b-88eb-d6ff4a0bba11)

Este serviço constrói a imagem da aplicação Django, instala as dependências, aplica migrações e inicia o servidor de desenvolvimento. Inclui as apps diario, mentha e protocolo.

#### d) Verificar conteiners
No Docker desktop verificar se todos os conteiners foram criados , e verificar se os conteiners dbpostgresql e Web estão ativos

![image](https://github.com/user-attachments/assets/4a840f02-9d1d-48d2-947c-c9b35582d980)

O container dbpostgresql_init é temporário e termina automaticamente após importar os dados.

#### e) Verificar volume

- O volume postgres_data pode ser visualizado no Docker Desktop (seção "Volumes").
- Este volume guarda todos os dados da base de dados PostgreSQL e não é apagado ao parar os containers, garantindo persistência entre sessões.

![image](https://github.com/user-attachments/assets/86a4d558-572c-4447-88fa-8aaf4a9e8438)


#### f) Abrir a aplicação no browser

![image](https://github.com/user-attachments/assets/c41c7772-3730-4933-baf7-3c4e4f41ec6a)

Trocar o http por : localhost:8000

![image](https://github.com/user-attachments/assets/e4855d2a-4c9b-4064-ba5c-03c63462dcfa)

Login:
- Username: Ver no Grupo do WhatsApp
- Password: Ver no Grupo do WhatsApp

---

### 5. Inicializar Todos os Serviços de Uma Vez

Este passo deve ser efetuado sempre para inicializar o website, após a primeira vez que se faça o passo 4, o passo 4 nunca mais volta a ser preciso ser efetuado.

Sempre que se quiser inicializar o website faz -se:

```docker-compose up```

Este comando levanta todos os serviços de forma automática: base de dados e aplicação Django. A importação do dump_file.sql não será repetida, pois o container dbpostgresql_init apenas corre uma vez.

---

### 6. Observação

O serviço web está configurado para atualizar ao serem feitas alterações no código, ou seja ao serem feitas alterações ao código basta fazer refresh na página.

---

### 7. Comandos Úteis Adicionais (para Desenvolvimento)

#### Reiniciar Tudo com Build (força nova instalação de dependências, útil após editar o Dockerfile ou requirements.txt)

```docker-compose up –build```

#### Limpar Recursos Docker Não Utilizados

```docker system prune -a```

Este comando:

- Remove todos os containers parados
- Remove todas as imagens não utilizadas (não referenciadas por nenhum container ativo)
- Remove volumes não utilizados
- Liberta espaço em disco

Uso recomendado:

-	Quando estás com problemas de espaço
-	Quando queres limpar completamente o ambiente Docker
-	Após muitos testes e builds antigos

--- 

## 🚀 Deploy no Servidor (Produção)

### Acesso à VM

* DNS: jupiter.ulusofona.pt
* IP: 193.137.75.199
* Portas: 80 (http), 443 (https), 8822 (ssh)
* user: ***
* password: ***

### Passos para Deploy

1.	Fazer push para a branch master no GitHub
2.	Aceder à VM via SSH
3.	Fazer pull do código:
```git pull origin master```
4.	Ativar o ambiente virtual:
```source env/bin/activate```
5.	Migrar a base de dados:
```
python manage.py makemigrations
python manage.py migrate
```
6.	Reiniciar o servidor:
```sudo systemctl restart gunicorn```

---

## 🌐 Acesso Online (Versão Produção)

Site: https://menthadigital.com/

Credenciais:

- Username: Ver no Grupo do WhatsApp
- Password: Ver no Grupo do WhatsApp

---

## 🌱 Workflow de Git

No relatório de TFC de 2024/2025 está presente um capítulo que explica o que workflow que adotamos no git. Este workflow é baseado no método usado em empresas com projetos grandes para evitar problemas de controlo de versões. É recomendada a leitura deste capítulo e utilização deste workflow.

---

## 📄 Documentação

No relatório de TFC de 2024/2025 está presente um capítulo que explica o estilo de documentação utilizado. É recomendado a continuidade de utilização deste estilo de documentação, visto que ajuda bastante no desenvolvimento do projeto.

---

## 📝 Observações Importantes

### Ficheiro requirements.txt:

Todas as bibliotecas Python utilizadas no projeto devem estar listadas neste ficheiro. Sempre que uma nova biblioteca for instalada (ex: via pip install), é obrigatório atualizar o requirements.txt.
Isto garante que o ambiente de produção, bem como qualquer outro ambiente de desenvolvimento, possa instalar exatamente as mesmas dependências do projeto original.

### Alterações gerais ao projeto:

Sempre que forem feitas alteracoes que influenciem este processo de instalação local do projeto , deploy para o servidor , alterações da arquitetura geral do projeto e tecnologias utilizadas este ficheiro deve ser atualizado , para dessa forma o guia de instalação ficar em conformidade com o estado atual do projeto.

