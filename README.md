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
├── diario/                  # MentHA COG & CARE
├── mentha/                 # Frontend principal
├── protocolo/              # MentHA EVAL
├── gateway/                # Configuração NGINX
├── manage.py
├── requirements.txt
├── Dockerfile              # Para desenvolvimento
├── Dockerfile.prod         # Para produção (Gunicorn)
├── compose.yaml            # Docker Compose (dev)
├── compose.prod.yaml       # Docker Compose (prod)
├── dump_tests.sql          # Dump de testes (dados dummy)
└── .env                    # Variáveis de ambiente (dev/prod)
```



---

## 🔀 Ambientes do Projeto

O projeto MentHA Digital está preparado para funcionar em dois ambientes distintos, com infraestruturas adaptadas a cada caso:

---

## 🧪 Ambiente de Desenvolvimento

Este ambiente permite correr a aplicação localmente com dados de teste, facilitando o desenvolvimento iterativo, debug e validações funcionais sem risco para os dados de produção.

### 🐳 Docker & Orquestração

Este ambiente é orquestrado através do ficheiro compose.yaml, que define três serviços principais que trabalham em conjunto para simular o funcionamento completo da aplicação:

1. dbpostgresql
- É o serviço responsável pela execução da base de dados PostgreSQL.
- Utiliza a imagem oficial postgres:12.9.
- Os dados são armazenados num volume persistente Docker chamado postgres_data, garantindo que a informação não se perde entre reinícios do container.

2. dbpostgresql_init
- Serviço temporário que tem como função importar automaticamente o dump de dados de teste (dump_tests.sql) para a base de dados PostgreSQL.
- Usa a mesma imagem oficial postgres:12.9.
- Monta o ficheiro dump_tests.sql do sistema local para dentro do container.

3. web
- Serviço principal que executa a aplicação Django.
- Constrói a imagem localmente com base no Dockerfile.
- Aplica automaticamente todas as migrações necessárias para garantir que o esquema da base de dados está atualizado.
- Inicia o servidor de desenvolvimento Django (runserver) com suporte a hot reload, facilitando o desenvolvimento ágil.

### 🧠 Funcionalidades adicionais

- Live Reload (Hot Reload):
O código local está ligado ao container via volume (.:/app). Assim, quando alteras ficheiros, o servidor Django reinicia automaticamente. Isto permite ver as mudanças imediatamente sem reiniciar manualmente.

- Variáveis de Ambiente:
As configurações específicas do ambiente estão no ficheiro .env, separado do código. Facilita alterar dados sensíveis sem mexer no código-fonte.

- Isolamento da Produção:
O ambiente de desenvolvimento usa dados anónimos (dump_tests.sql), garantindo que testes não afetem dados reais.

- Debugging Simplificado:
Logs detalhados e compatibilidade com ferramentas como VSCode Debugger facilitam a deteção e correção de erros.

---

## 🚀 Ambiente de Produção
Este ambiente é utilizado em contexto de deploy real, com foco em segurança, estabilidade e performance.

### 🐳 Docker & Orquestração
Utiliza o ficheiro compose.prod.yaml.

Contém três serviços principais:

dbpostgresql: container da base de dados PostgreSQL, com volume persistente.

web: serviço Django executado com Gunicorn como WSGI server.

nginx: reverse proxy containerizado, responsável por:

servir ficheiros estáticos (/static/) e media (/media/)

redirecionar as requisições HTTP para o Gunicorn

aplicar headers de segurança e compressão

## 🔁 CI/CD com GitHub Actions
A infraestrutura de deploy está integrada num pipeline automatizado:

Workflow deploy.yml (CI/CD)
Fase de Testes:

Executa testes Django automaticamente em cada push para main.

Base de dados mentha_test é criada num container isolado no GitHub Runner.

Fase de Deploy:

Faz SCP dos ficheiros do projeto para o servidor remoto.

Gera dinamicamente o ficheiro .env no servidor com segredos armazenados no GitHub Secrets.

Executa os seguintes comandos no servidor:

docker-compose -f compose.prod.yaml down

docker-compose -f compose.prod.yaml up -d --build

python manage.py collectstatic --noinput




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
POSTGRES_PASSWORD=Password pedir grupo whatsApp
POSTGRES_DB=mentha

PGUSER=leda
PGPASSWORD=Password pedir grupo whatsApp
PGDB=mentha

POSTGRES_HOST=dbpostgresql
POSTGRES_PORT=5432
```

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

## 🗃️ Bases de Dados 

### 🧪 Ambiente de Testes

O ambiente de testes utiliza a base de dados definida no ficheiro `dump_tests.sql`, localizado na raiz do projeto. Este ficheiro contém dados **anónimos ou simulados**, próprios para desenvolvimento, debugging e testes.

#### ✅ Importar dump de testes

Para carregar um novo dump de testes no ambiente de desenvolvimento:

1. **Substitui** o ficheiro `dump_tests.sql` na raiz do projeto.
2. **Confirma** que está codificado em `UTF-8` **sem BOM** (sem Byte Order Mark).
3. **Reinicia os serviços Docker** com remoção dos volumes para forçar a importação:

```bash
# Apaga volumes antigos e força importação do novo dump
docker-compose down -v
docker-compose up --build
```
O serviço dbpostgresql_init irá executar automaticamente o psql -f dump_tests.sql.

#### 📤 Exportar novo dump de testes

Caso queiras gerar um novo ficheiro `dump_tests.sql` a partir da base de dados atual (por exemplo, para partilhar com colegas), segue os passos abaixo:

```bash
docker exec dbpostgresql pg_dump -U leda -d mentha > dump_testsNovo.sql
```

✅ Garante que o ficheiro exportado está em UTF-8 sem BOM antes de reutilizá-lo ou partilhá-lo com outros.

🔎 Como verificar se o ficheiro está em UTF-8 sem BOM

**No VSCode**:
1. Abre o ficheiro `dump_tests.sql`.
2. No canto inferior direito, verifica a codificação (ex: `UTF-8`, `UTF-16 LE`, etc.).
3. Clica na codificação e, se necessário, converte para `UTF-8`.
4. **Muito importante**: se vires `UTF-8 with BOM`, clica e escolhe **Reopen with Encoding > UTF-8** (sem BOM) e guarda novamente.

**🔄 Como converter para UTF-8 sem BOM**

**Windows (PowerShell):**

```powershell
Get-Content dump_tests.sql | Set-Content -Encoding utf8 dump_tests_clean.sql
```


### 🚀 Ambiente de Produção

A base de dados de produção usa um dump específico chamado `dump_file.sql`. Este ficheiro contém dados reais e sensíveis, 

> ⚠️ Este ficheiro para ser colocado no servidor da lusofona no futuro tem de ser pedido ao professor

#### ✅ Importar dump de produção no servidor
Para importar o ficheiro dump_file.sql:

Envia o ficheiro para o servidor (exemplo com SCP):

```bash
scp dump_file.sql root@IP_DO_SERVIDOR:/caminho/do/projeto/
```
Garante que o nome do ficheiro no servidor é exatamente dump_file.sql.

```bash
docker-compose down -v
docker-compose up --build
```
O volume do PostgreSQL será criado ou reescrito, e o dump será carregado automaticamente.

#### 📥 Exportar dump da produção (Backup)
Para criar um backup da base de dados de produção diretamente no servidor:

```
# 1. Acede ao container da base de dados
docker exec -it dbpostgresql bash

# 2. Gera um novo dump com data para organização
pg_dump -U leda -d mentha > /backups/dump_YYYYMMDD.sql
Substitui YYYYMMDD pela data atual, ex: dump_20250620.sql.
```

#### ⬇️ Transferir o backup para a tua máquina local:
```bash
scp root@IP_DO_SERVIDOR:/backups/dump_20250620.sql ./backups/
```

#### 📁 Pasta de Backups
Por padrão, a pasta /backups não está criada automaticamente, mas é altamente recomendada criar no servido. Esta pasta deve ser usada para:

- Guardar versões anteriores dos dumps (ex: dump_YYYYMMDD.sql)
- Facilitar a recuperação rápida da base de dados em caso de falha ou corrupção de dados

⚠️ Cria esta pasta manualmente se ainda não existir:
mkdir backups 

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

