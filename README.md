# protocolo_de_avaliacao

⚙️ Requisitios
======
1. Python 3.10 ou superior

🔧 Deployment
======
1. Abrir o cmd
2. Fazer cd para o dir onde está o "requirements.txt"
3. Correr o comando "pip install -r requirements.txt"
4. Fazer cd para o dir onde está o manage.py
5. Correr o comando "py manage.py runserver"
6. Abrir http://127.0.0.1:8000/ no browser
7. Fazer login com as credenciais user:"superuser" pw:"super123"

📶 Acesso Online
======

1. Abrir o Link https://menthadigital.com/
2. Fazer login com as credenciais user:"superuser" pw:"super123"

🔖 Passar DB para PSQL
======

1. Se quisermos importar dados da bd antiga em sqlite, temos de exportar a bd em UTF-8, senão vai dar erro de encoding,  para isso fazemos: 
```
python manage.py -Xutf8 dumpdata > <nome_ficheiro>.json
```
2. Instalar psycogpg2 (package adaptador de PostgreSQL para Django)
```
pip install psycopg2
```
3. Editar a variável DATABASES no settings.py para:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ‘<nome_bd>’,
        'USER': '<username_bd>',
        'PASSWORD': '<password>',
        'HOST': '<ip_bd>',
        'PORT': '<port_bd>',
    }
}
```
4. Como demos expor da bd em UTF-8 vamos ter caracteres estranhos no lugar de de caracteres portuguêses.
5. Para corrigir todos os caracteres errados em todos os modelos da bd, fazemos um dicionario onde metemos como chave o char errado e como valor char correto
6. Para isto usamos tb smart_str() para dar para correr em linux senão vai dar erro de encoding
```
from django.utils.encoding import smart_str

char_map = {
    smart_str("<char_errado>", encoding='utf-8', strings_only=True, errors='strict'): smart_str("<char_correto>", encoding='utf-8', strings_only=True, errors='strict'),
}
```
7. Depois definimos uma função para substituir esses caracteres num texto recebido
```
def replace_chr(text):
    if text is not None:
        smart_txt = smart_str(text, encoding='utf-8', strings_only=True, errors='strict')
        for incorrect_char, correct_char in char_map.items():
            smart_txt = text.replace(incorrect_char, correct_char)
        return smart_txt
    return text 
```
8. Executar o environment e abrir a python shell
```
source bin/activate
python manage.py shell
```
9. Importar o que for necessário (onde está a funçao decode() e executá-la) p.ex, se a funçao estiver no views.py:
```
from mentha.views import * 
decode()
```
