from .base import *

SECRET_KEY = 'eeu&ozb(4qd%e7))wch!9-4)0n&__wy!-eikv)k2ov3i9y_#vt'
DEBUG = True
ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}