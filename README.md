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

1. Temos de dar export da bd em UTF-8 senão vai dar erro de encoding,  para isso fazemos: 
```
python manage.py -Xutf8 dumpdata > <nome_ficheiro>.json
```
2. Instalar psycogpg2 
```
pip install psycopg2
```
3. Editar a varivel DATABASES no settings.py para:
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
4. Como demos expor da bd em UTF-8 vamos ter caracteres estranhos no lugar de de caracteres portugueses.
5. Para substituir todos os caracteres estranhos em todos os modelos da base de dados fazemos um dicionario onde metemos como chave o caracter estranho e como valor o que é suposto ser em portugues
6. Para isto usamos tb smart_str para dar para correr em linux senão vai dar erro de encoding
```
char_map = {
    smart_str("+º", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ç", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+ú", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ã", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+¬", encoding='utf-8', strings_only=True, errors='strict'): smart_str("é", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+¦", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ó", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+¬", encoding='utf-8', strings_only=True, errors='strict'): smart_str("ê", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+é", encoding='utf-8', strings_only=True, errors='strict'): smart_str("Â", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+Ò", encoding='utf-8', strings_only=True, errors='strict'): smart_str("é", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+í", encoding='utf-8', strings_only=True, errors='strict'): smart_str("á", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+¡", encoding='utf-8', strings_only=True, errors='strict'): smart_str("í", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+á", encoding='utf-8', strings_only=True, errors='strict'): smart_str("à", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+ë", encoding='utf-8', strings_only=True, errors='strict'): smart_str("É", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+ü", encoding='utf-8', strings_only=True, errors='strict'): smart_str("Á", encoding='utf-8', strings_only=True, errors='strict'),
    smart_str("+ó", encoding='utf-8', strings_only=True, errors='strict'): smart_str("â", encoding='utf-8', strings_only=True, errors='strict'),
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
9. Importar o que for necessário ( onde está a funçao decode() e executá-la) p.ex, se a funçao estiver no views.py:
```
from mentha.views import * 
decode()
```
