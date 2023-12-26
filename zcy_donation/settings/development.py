from os import getenv

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': getenv('DB_NAME'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASSWORD'),
        'HOST': getenv('DB_HOST'),
        'PORT': getenv('DB_PORT', '3306'),
    }
}

ALLOWED_HOSTS = []
