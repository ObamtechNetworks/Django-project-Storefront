from .common import *

INSTALLED_APPS += [
    'debug_toolbar',
    'silk',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
] + MIDDLEWARE

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hs6j037urx6iav+7#10%-vu4l4f5@@-1_zo)oft4g7$vf2$jmp'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}
