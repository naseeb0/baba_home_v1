print("Loading development settings...")

from .base import *

# Override debug setting for development
DEBUG = True

# Allowed hosts for development
ALLOWED_HOSTS = ["*"]

# Database settings for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Media settings for development
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
