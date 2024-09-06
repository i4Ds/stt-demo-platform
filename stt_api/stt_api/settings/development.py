from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'stt_api',
        'ENFORCE_SCHEMA': False,
    }
}
