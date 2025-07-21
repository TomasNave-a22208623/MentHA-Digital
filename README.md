# 🧠 MentHA – Guia de Instalação e Execução 






<img width="1906" height="902" alt="image" src="https://github.com/user-attachments/assets/1286e3cd-10b3-4e46-bb7a-1e9ac8547f2c" />

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

Este ambiente destina-se a programadores e equipas durante a fase de implementação, testes e validação local da aplicação. Permite um ciclo de desenvolvimento rápido e seguro, com dados anónimos, hot reload e isolamento completo da produção.

### 🐳 Arquitetura e Serviços Docker

O ambiente é orquestrado através do ficheiro `compose.yaml`, que define três serviços principais que trabalham em conjunto para simular o funcionamento completo da aplicação:

1. **dbpostgresql**  
   - Serviço responsável pela execução da base de dados PostgreSQL.  
   - Utiliza a imagem oficial `postgres:12.9`.  
   - Os dados são armazenados num volume persistente Docker chamado `postgres_data`, garantindo persistência entre reinícios.

2. **dbpostgresql_init**  
   - Serviço temporário responsável por importar automaticamente o dump de dados de teste (`dump_tests.sql`) para a base de dados.  
   - Usa a mesma imagem oficial `postgres:12.9`.  
   - Monta o ficheiro `dump_tests.sql` do sistema local para dentro do container, permitindo inicialização com dados anónimos.

3. **web**  
   - Serviço principal que executa a aplicação Django.  
   - Constrói a imagem localmente com base no `Dockerfile`.  
   - Aplica automaticamente todas as migrações para manter o esquema da base de dados atualizado.  
   - Inicia o servidor de desenvolvimento Django (`runserver`) com suporte a hot reload, facilitando um desenvolvimento ágil.

### 🧠 Funcionalidades Adicionais

- **Live Reload (Hot Reload):**  
  O código local está ligado ao container via volume (`.:/app`). Sempre que alteras ficheiros, o servidor Django reinicia automaticamente, permitindo visualizar as mudanças em tempo real, sem necessidade de reiniciar manualmente.

- **Variáveis de Ambiente:**  
  Todas as configurações específicas do ambiente estão definidas no ficheiro `.env`, separado do código-fonte. Isto facilita a alteração de dados sensíveis sem comprometer o código.

- **Isolamento da Produção:**  
  O ambiente utiliza um dump de dados anónimos (`dump_tests.sql`), garantindo que os testes locais não interferem nem comprometem dados reais de produção.

- **Debugging Simplificado:**  
  Logs detalhados e compatibilidade com ferramentas como o VSCode Debugger permitem uma deteção e resolução de erros mais eficiente.


---

## 🚀 Ambiente de Produção

Este ambiente corresponde à infraestrutura utilizada para o deploy real da aplicação, disponível ao público. O foco principal é garantir **segurança**, **estabilidade**, **performance** e **escalabilidade** para o sistema em produção.

### 🏗️ Visão Geral

O ambiente de produção é uma configuração mais robusta e otimizada, que inclui:

- Execução da aplicação Django com um servidor WSGI profissional (Gunicorn) para melhor desempenho e gestão de múltiplos pedidos simultâneos.
- Utilização de um **reverse proxy** (NGINX) containerizado, que serve ficheiros estáticos e media de forma eficiente, além de proteger e otimizar as comunicações HTTP.
- Base de dados PostgreSQL com armazenamento persistente e saudável.
- Configurações específicas de ambiente que garantem a separação total da lógica e dados de desenvolvimento.

### 🐳 Docker & Orquestração

O ambiente é gerido pelo ficheiro `compose.prod.yaml`, que define três serviços essenciais:

1. **dbpostgresql**  
   - Container da base de dados PostgreSQL, responsável por armazenar todos os dados da aplicação.  
   - Usa um volume Docker persistente para garantir que os dados se mantêm seguros entre reinícios e atualizações do container.  
   - Inclui um mecanismo de healthcheck para monitorar a disponibilidade do serviço.

2. **web**  
   - Serviço principal que executa a aplicação Django utilizando o servidor **Gunicorn**, um servidor WSGI leve e eficiente, indicado para produção.  
   - Recebe as requisições encaminhadas pelo NGINX e responde com conteúdos dinâmicos da aplicação.  
   - Aplica migrações e configurações otimizadas para o ambiente de produção.  
   - Não expõe funcionalidades de hot reload, garantindo estabilidade.

3. **nginx**  
   - Reverse proxy containerizado que atua como intermediário entre os clientes e o serviço Django.  
   - Serve diretamente ficheiros estáticos (`/static/`) e media (`/media/`) para otimizar a entrega de conteúdo e reduzir carga no servidor de aplicação.  
   - Aplica headers de segurança importantes (ex: Content Security Policy, X-Frame-Options) e compressão (gzip) para melhorar performance e segurança.  
   - Encaminha requisições HTTP para o serviço `web` (Gunicorn), mantendo a arquitetura limpa e modular.  

### 🔐 Segurança e Boas Práticas

Para garantir a segurança da aplicação em produção, especialmente em relação às credenciais e dados sensíveis, adotamos as seguintes práticas:

- **Variáveis de Ambiente para Configurações Sensíveis**  
  As informações confidenciais, como a `SECRET_KEY` do Django (usada para criptografia interna e proteção da sessão), as credenciais da base de dados, e outras configurações críticas, são armazenadas exclusivamente em variáveis de ambiente definidas num ficheiro `.env` no servidor de produção.  
  Isto evita que estas chaves sejam incluídas diretamente no código-fonte ou no repositório Git, protegendo-as de acessos não autorizados e facilitando a sua atualização sem necessidade de alterar o código.

- **Camada de proteção via NGINX**  
  O NGINX funciona como reverse proxy e firewall, filtrando requisições maliciosas, aplicando cabeçalhos de segurança HTTP e servindo conteúdos estáticos, reduzindo a exposição da aplicação e melhorando o desempenho.

- **Servidor WSGI profissional (Gunicorn)**  
  O Gunicorn oferece uma gestão eficiente das conexões, permitindo lidar com múltiplos pedidos simultâneos, garantindo estabilidade e escalabilidade em produção.

---

## 🔁 CI/CD com GitHub Actions

A infraestrutura do projeto está totalmente integrada num pipeline automatizado de CI/CD (Continuous Integration / Continuous Deployment) usando o GitHub Actions. Isto permite que, sempre que um código novo é enviado para o repositório (push para a branch `main`), todo o processo de testes e deployment seja executado de forma automática e controlada, garantindo qualidade e rapidez.

### Fluxo do Workflow `deploy.yml`

1. **Fase de Testes (CI)**
   - Cada vez que ocorre um push para a branch principal (`main`), o GitHub Actions inicia uma pipeline de testes.
   - Nesta fase, é criado um ambiente isolado com um container PostgreSQL temporário (`mentha_test`) para simular a base de dados durante os testes.
   - A aplicação Django executa os seus testes automatizados, validando que todas as funcionalidades principais estão corretas e que não existem regressões.
   - Apenas se todos os testes forem aprovados, o workflow avança para a próxima fase.

2. **Fase de Deploy (CD)**
   - Depois dos testes serem bem sucedidos, a pipeline inicia o deploy automático da aplicação para o servidor remoto.
   - Os ficheiros do projeto são copiados via SCP (Secure Copy Protocol) para o diretório do servidor destinado ao projeto.
   - O ficheiro `.env` é gerado dinamicamente no servidor, utilizando segredos (como chaves secretas e credenciais) guardados em segurança no GitHub Secrets, garantindo que informações sensíveis nunca ficam expostas no código-fonte público.
   - O workflow executa comandos SSH no servidor para:
     - Parar quaisquer serviços Docker em execução (`docker-compose -f compose.prod.yaml down`), garantindo uma atualização limpa.
     - Recriar e iniciar os serviços em modo destacado, reconstruindo as imagens se necessário (`docker-compose -f compose.prod.yaml up -d --build`).
     - Executar a coleta dos ficheiros estáticos da aplicação Django (`python manage.py collectstatic --noinput`), preparando-os para serem servidos pelo NGINX.

### Benefícios deste CI/CD automatizado

- **Automação total:** O processo de testes, build e deploy ocorre sem intervenção manual, reduzindo erros humanos.
- **Segurança reforçada:** As credenciais e segredos ficam guardados de forma segura no GitHub e nunca no repositório.
- **Velocidade e fiabilidade:** Permite lançar atualizações rapidamente com menor risco de falhas em produção.
- **Isolamento dos ambientes:** Os testes correm num ambiente separado, evitando interferência nos dados reais.

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

## 🖥️ Configuração local do Ambiente de Desenvolvimento 

Esta secção detalha o processo completo para configurar o ambiente de desenvolvimento localmente, desde a preparação inicial até à execução da aplicação localmente, garantindo que todos os serviços essenciais estão corretamente configurados e a funcionar.

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

### 🚀 Guia de adaptação da pipeline de Deploy no Servidor (Produção) a uma nova VM
Este guia mostra como ligar a infraestrutura de produção a uma nova VM (Ubuntu).

### ✅ 1. Pré-requisitos na Nova VM (Ubuntu)

```
# Atualizar e instalar Docker
sudo apt update && sudo apt install docker.io -y
sudo systemctl enable docker && sudo systemctl start docker

# Instalar Docker Compose v2
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 🔐 2. Atualizar Secrets no GitHub
No repositório, vai a Settings > Secrets and variables > Actions > Repository secrets e atualiza estes valores:

- **SERVER_HOST** - IP ou domínio da nova VM
- **SERVER_USER** - Nome do utilizador SSH da VM (ex: root, ubuntu)
- **SERVER_SSH_KEY** - Chave privada SSH (sem password)

⚠️ O .env será gerado automaticamente na VM com estes secrets!

### 📦 3. Preparar o Dump Inicial (uma só vez)
Como a pipeline não envia o dump_file.sql, precisas de o colocar manualmente apenas na primeira vez:
```
# Envia o ficheiro para a VM
scp dump_file.sql user@ip_da_vm:~/mentha_project/
```

### 📂 4. Importar o Dump Manualmente (Primeira Vez)
Só precisas de fazer isto uma vez na VM nova:

```
# Aceder ao container da base de dados
docker exec -it dbpostgresql bash

# Importar o dump
psql -U leda -d mentha -f /code/dump_file.sql
```

### 🔁 5. Reiniciar os Serviços (só se alterares manualmente o dump)
```
cd ~/mentha_project
docker-compose -f compose.prod.yaml down
docker-compose -f compose.prod.yaml up -d --build
```
### 🗃️ 7. Criar Pasta de Backups
```
cd ~/mentha_project
mkdir backups
mv dump_file.sql backups/
```

--- 

## 🌍 Infraestrutura de Produção – Acesso e Contexto
Atualmente, o projeto MentHA Digital encontra-se em dois ambientes distintos em producao:

### 🧪 Ambiente de Staging (Versão Atualizada e Estável)
A versão mais recente e funcional do projeto encontra-se alojada numa VM da DigitalOcean.
Este ambiente foi criado para testar o processo de deploy, infraestrutura, CI/CD e validação geral do MVP com dados reais.

✅ Esta é a versão mais atualizada do projeto, com deploy automatizado via GitHub Actions e base de dados configurada.

Acesso à plataforma:

- URL: http://menthadigital.pt/
- Credenciais: Ver no Grupo do WhatsApp

### 🏛️ Servidor da Lusófona (Versão Oficial, Desatualizada)
O servidor oficial da Universidade Lusófona está atualmente com uma versão antiga do projeto.
O objetivo principal para as equipas futuras será migrar a infraestrutura estável da DigitalOcean para este servidor, usando a pipeline de CI/CD existente.
O passo a passo para adptar a pipeline existente á VM da Lusófona encontra se explicada

**Dados da VM da Lusófona:**

- **DNS:** jupiter.ulusofona.pt
- **IP:** 193.137.75.199
- **Utilizador:** ***
- **Password:** ***

Acesso à plataforma:

- URL: https://menthadigital.com/
- Credenciais: Ver no Grupo do WhatsApp

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

