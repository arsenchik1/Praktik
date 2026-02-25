"""
Настройки Django для асинхронного API (без сессий и ORM)
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-key-for-dev'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Только необходимые приложения
INSTALLED_APPS = [
    'rest_framework',
    'api',
]

# Минимальный middleware без сессий и аутентификации
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [],
        },
    },
]

# Отключаем сессии
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Простая база данных (не будет использоваться)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = False
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки 1С
ONEC_CONFIG = {
    'url': 'http://176.192.70.122:90/fitnes_t_nfc_mobile/hs/nfc_mobile/v1',
    'login': 'FitnessKit',
    'password': 'vY0xodyg',
    'club_id': '59115d1e-9052-11eb-810c-6eae8b56243b',
    'request_id': 'e1477272-88d1-4acc-8e03-7008cdedc81e',
}

# REST Framework настройки
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
}