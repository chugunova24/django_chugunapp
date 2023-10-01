"""
Django settings for generation project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, '.env')

if os.path.exists(env_path):
    load_dotenv(env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_COOKIE_AGE = 60 * 5
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-oeizjy+e2gsf6d36tvh8!&30*7yx%!wehc0tjbgo$19!u*%&pl"
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG')

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', os.getenv('DJANGO_CONTAINER_NAME')]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "text_gen.apps.TextGenConfig",
    "users.apps.UsersConfig",
    "rest_framework",
    "django.contrib.postgres",
    "phonenumber_field",
    "debug_toolbar",
    # "silk",
    # 'django_extensions',
    # "store",
]

MIDDLEWARE = [
    # "silk.middleware.SilkyMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",

]


ROOT_URLCONF = "generation.urls"
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_EXTENDED_FILE_NAME = True
SILKY_META = True

# SILKY_DYNAMIC_PROFILING = [{
#     'module': 'text_gen.views',
#     'function': 'CsvReaderHome.dispatch',
# }]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "generation.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# django.db.backends.postgresql



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_NAME'),
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'test_db',
#         'USER': 'postgres',
#         'PASSWORD': '123456',
#         'HOST': 'localhost',
#         'PORT': '15432',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'OPTIONS': {
#             'service': 'db_service',
#             'passfile': '.pgpass',
#         },
#     }
# }



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/",
        # "LOCATION": "redis://redis_chugunapp:6379/",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "SOCKET_CONNECT_TIMEOUT": 5,  # seconds
            # "SOCKET_TIMEOUT": 5,  # seconds
            # "IGNORE_EXCEPTIONS": True,
            # "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        }
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "OPTIONS": {
#             "service": "text_gen",
#             "passfile": ".my_pgpass",
#         },
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = "ru-RU"
LANGUAGE_CODE = "en-EN"

TIME_ZONE = "UTC"
# TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

INTERNAL_IPS = [
    "127.0.0.1",
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'var', 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'chugun_host'
# EMAIL_PORT = '8080'
# EMAIL_USE_TLS = 'False'
# EMAIL_HOST_USER = 'chugun_host_user'
# DISPLAY_NAME = "chugun@boo.com"
# DONOT_REPLY_EMAIL_PASSWORD = 'true'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_TEMPLATE_PACK = 'bootstrap4'


context_processors = [
    'django.template.context_processors.media',
]


# Silk SQL Debbagger

