from os import getenv
from dotenv import load_dotenv
from .base import *


# Define the path to the .env file
env_path = Path(__file__).resolve().parents[2] / 'config' / '.env'


# Load the environment variables from the .env file
load_dotenv(env_path)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY')


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': getenv('MYSQL_DATABASE', 'db'),
        'USER': getenv('MYSQL_USER'),
        'PASSWORD': getenv('MYSQL_PASSWORD'),
        'HOST': getenv('DB_HOST', 'db'),
        'PORT': getenv('DB_PORT', '3306'),
    }
}

ALLOWED_HOSTS = []
