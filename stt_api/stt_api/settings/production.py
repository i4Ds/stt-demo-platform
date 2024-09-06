import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'stt_api',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': os.environ['DB_HOST'],
            'port': int(os.environ['DB_PORT']),
            'username': os.environ['DB_USERNAME'],
            'password': os.environ['DB_PASSWORD'],
        },
    }
}
