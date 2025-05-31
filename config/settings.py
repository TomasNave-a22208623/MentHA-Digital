"""
Django settings for config project.

"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ENVIRONMENT
DJANGO_ENV = os.getenv("DJANGO_ENV", "development")
DEBUG = DJANGO_ENV != "production"


# SECRET KEY
SECRET_KEY = os.getenv('SECRET_KEY', 'insecure-default-key')


# ALLOWED HOSTS 
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
else:
    ALLOWED_HOSTS = ['jupiter.ulusofona.pt', 'menthadigital.com' , 'menthadigital.pt']


# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Application definition

INSTALLED_APPS = [
    #Sockets
    'channels',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #CARE & COG
    'diario',
    #Protocolo de Avaliacao
    'protocolo',
    #Site estático
    'clients',
    'mentha',
    
    'markdownify',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# URLS 
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = "config.asgi.application"


# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}




# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# CHANNELS (InMemory para dev/testes)
CHANNEL_LAYERS = {
    'default':{
        'BACKEND':'channels.layers.InMemoryChannelLayer'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pt-pt'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# STATIC FILES
STATIC_URL = '/static/'

if DJANGO_ENV == "production":
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#Markdownify
MARKDOWNIFY_STRIP = False
MARKDOWNIFY = {
   "default": {
      "WHITELIST_TAGS": [
        'a', 'abbr', 'acronym',
        'strong', 'b',
        'blockquote', 'em', 'i',
        'ul', 'li', 'ol',
        'p',
        'h1', 'h2', 'h3', 'h4',
          'table',
          'thead',
          'tbody',
          'th',
          'tr',
          'td',
      ],
"MARKDOWN_EXTENSIONS": ["markdown.extensions.fenced_code", "markdown.extensions.extra",]
   },

   "alternative": {
      "WHITELIST_TAGS": ["a", "p"],
      "MARKDOWN_EXTENSIONS": ["markdown.extensions.fenced_code", "markdown.extensions.extra",]
   }
}

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True # Your email address
EMAIL_HOST_USER = 'info.methadigital@gmail.com'
EMAIL_HOST_PASSWORD = 'ndxwpwdjpxggvjta'  # usar uma google app password
USE_L10N = False
DECIMAL_SEPARATOR = '.'