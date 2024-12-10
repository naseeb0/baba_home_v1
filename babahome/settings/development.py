print("Loading development settings...")

from .base import *

# Override debug setting for development
DEBUG = True

# Allowed hosts for development
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database settings for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Media URL for development
MEDIA_URL = 'http://localhost:8000/media/'
