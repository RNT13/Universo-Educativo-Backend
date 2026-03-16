import os
import sys
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

load_dotenv()

# -----------------------------------------

# Detectar se estamos no Render
IS_RENDER = os.getenv("RENDER", "false").lower() == "true"

# SECRET_KEY
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-chave-local-para-desenvolvimento")

# Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# resend
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# DEBUG
# A lógica `if not IS_RENDER` garante que DEBUG seja sempre False em produção no Render.
DEBUG = bool(int(os.getenv("DEBUG", 1))) if not IS_RENDER else False

# ALLOWED_HOSTS
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1 localhost").split()
if IS_RENDER:
    RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

# Aplicações instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_extensions",
    "rest_framework.authtoken",
    "drf_spectacular",
    "corsheaders",

    # APPS PROJETO
    "products",
    "orders",
    "payments",
    "emails",
    "access",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )
    INTERNAL_IPS = ["127.0.0.1"]

# URL e WSGI
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Banco de dados
if IS_RENDER:
    DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("SQL_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.getenv("SQL_DATABASE"),
            "USER": os.getenv("SQL_USER"),
            "PASSWORD": os.getenv("SQL_PASSWORD"),
            "HOST": os.getenv("SQL_HOST"),
            "PORT": os.getenv("SQL_PORT"),
        }
    }


# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Auto field padrão
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# DRF Spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Backend Template API",
    "DESCRIPTION": "Documentação da API do projeto",
    "VERSION": "1.0.0",
}
