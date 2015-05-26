"""
Django settings for testsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/



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
	'bootstrap3',
	'clustersizer',
	'django_rq',

)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'testsite.urls'

WSGI_APPLICATION = 'testsite.wsgi.application'



# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


# django bootstrap
BOOTSTRAP3 = {}
BOOTSTRAP3['include_jquery'] = True


## HEROKU SPECIFIC CONFIG

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config()}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static asset configuration
# import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

# django bootstrap
BOOTSTRAP3 = {}
BOOTSTRAP3['include_jquery'] = True
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

TEMPLATE_DIRS = (os.path.join(BASE_DIR,'templates'),)


# redis for worker queue
RQ_QUEUES = {
	# 'default': {
	# 	'HOST': 'localhost',
	# 	'PORT': 6379,
	# 	'DB': 0,
	# 	'PASSWORD': 'some-password',
	# 	'DEFAULT_TIMEOUT': 360,
	# },
	'default': {
		'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'), # If you're on Heroku
		'DB': 0,
		'PASSWORD': '04386354638749292502bb71228ffa3b',
		'DEFAULT_TIMEOUT': 500,
	},
# 	'low': {
# 		'HOST': 'localhost',
# 		'PORT': 6379,
# 		'DB': 0,
# 	}
}


try:
	from local_settings import *
except ImportError:
	pass

# private api keys, etc loaded from local_settings

SECRET_KEY = os.environ['SECRET_KEY']