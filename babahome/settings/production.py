print("Loading production settings...")

from .base import *

DEBUG = True  # Disable debug mode in production


ALLOWED_HOSTS = [
    '143.198.34.20', 
    'admin.homebaba.com', 
    'www.admin.homebaba.com', 
    'homebaba.com', 
    'www.homebaba.com'
]

# PostgreSQL database settings for production
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

# Secure cookies settings for production
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CORS settings for production
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Allow all origins temporarily for debugging
CORS_ALLOW_ALL_ORIGINS = True  # For development/debugging only
# CORS_ALLOWED_ORIGINS = [
#     'http://admin.homebaba.com',
#     'https://admin.homebaba.com',
#     'http://localhost:3000',
#     'http://127.0.0.1:3000',
#     'http://localhost:3001',
#     'http://127.0.0.1:3001',
#     'https://homebaba.com',
#     'http://homebaba.com',
#     'https://www.homebaba.com',
# ]

# Media files configurations
MEDIA_URL = 'https://admin.homebaba.com/media/'  # Update this to your domain

# CSRF trusted origins for production
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://homebaba.com',
    'http://homebaba.com',
    'https://www.homebaba.com',
    'http://admin.homebaba.com',
    'https://www.admin.homebaba.com',
]
