import os

DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')
print(f"Current DJANGO_ENV: {DJANGO_ENV}")

if DJANGO_ENV == 'production':
    print("Loading production settings...")
    from .production import *
else:
    print("Loading development settings...")
    from .development import *

print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")