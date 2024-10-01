from .base import *

DEBUG = True

ALLOWED_HOSTS = ['143.198.34.20', 'admin.homebaba.com', 'www.admin.homebaba.com', 'homebaba.com', 'www.homebaba.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'homebabacom',
        'USER': 'naseeb',
        'PASSWORD': 'DatabaseNaseebPassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'https://admin.homebaba.com',
    'https://homebaba.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://admin.homebaba.com',
    'https://homebaba.com',
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
