"""
Django settings for litsey_exam project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import dj_database_url
#DATABASES['default'] = dj_database_url.config()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0g%d$o40l_2nnmv$z4xj=^aa-x8nwt%1dk)*e-3m1loesf@s01'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'journal',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'litsey_exam.urls'

WSGI_APPLICATION = 'litsey_exam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# #lyceedja
DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
 'NAME': 'journal2018', # Or path to database file if using sqlite3.
 'USER': 'postgres', # Not used with sqlite3.
 'PASSWORD': 'pyfybtcbkf', # Not used with sqlite3.
 'HOST': '46.101.124.2', # Set to empty string for localhost. Not used with sqlite3.
 'PORT': '', # Set to empty string for default. Not used with sqlite3.
 }
}
#
# DATABASES = {
#  'default': {
#  'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#  'NAME': 'litsey', # Or path to database file if using sqlite3.
#  'USER': 'postgres', # Not used with sqlite3.
#  'PASSWORD': 'tarhush', # Not used with sqlite3.
#  'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
#  'PORT': '5432', # Set to empty string for default. Not used with sqlite3.
#  }
# }

# DATABASES = {
#  'default': {
#  'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#  'NAME': 'litsey', # Or path to database file if using sqlite3.
#  'USER': 'postgres', # Not used with sqlite3.
#  'PASSWORD': 'tarhush', # Not used with sqlite3.
#  'HOST': 'it.in-education.ru', # Set to empty string for localhost. Not used with sqlite3.
#  'PORT': '5432', # Set to empty string for default. Not used with sqlite3.
#  }
# }

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
#     }
# }

#DATABASES = { 'default' : dj_database_url.config()}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# MEDIA_ROOT = '/home/lyceedja/domains/lycee7.djangohost.name/public_html/media/'
# MEDIA_URL = '/media/'
# STATIC_ROOT = '/home/lyceedja/domains/lycee7.djangohost.name/public_html/static/'
# STATIC_URL = '/static/'
LOGIN_URL = '/journal/login'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
pth = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')
MEDIA_ROOT = pth
MEDIA_URL = '/media/'
