"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from pathlib import Path
import os
from dotenv import dotenv_values


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_data = dotenv_values(dotenv_path=os.path.abspath(os.path.join(BASE_DIR, '..', 'venv', '.env')))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = dotenv_data.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'news.apps.NewsConfig',
    'accounts',
    'django_filters',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',
    'django_apscheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': dotenv_data.get('GOOGLE_CLIENT_ID'),
            'secret': dotenv_data.get('GOOGLE_SECRET'),
            'key': ''
        }
    }
}

ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomAllauthSignupForm'}

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


EMAIL_HOST = 'smtp.rambler.ru' # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465 # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = dotenv_data.get('rambler_EMAIL_HOST_USER') # ваше имя пользователя, например если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_USE_SSL = True # Яндекс использует ssl, подробнее о том, что это, почитайте на Википедии, но включать его здесь обязательно
EMAIL_HOST_PASSWORD = dotenv_data.get('rambler_EMAIL_HOST_PASSWORD')


DEFAULT_FROM_EMAIL = EMAIL_HOST_USER + '@rambler.ru'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  # позволит избежать дополнительных действий и активирует аккаунт сразу, как только мы перейдём по ссылке (не обяз)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1 # количество дней, в течение которых будет доступна ссылка на подтверждение регистрации и так далее (не обяз)
# все поля для настроек allauth:  https://django-allauth.readthedocs.io/en/latest/configuration.html


# Строка формата для отображения меток времени выполнения на сайте администрирования Django. Значение по умолчанию
# просто добавляет секунды к стандартному формату Django, что полезно для отображения временных меток
# для заданий, выполнение которых запланировано с интервалом менее одной минуты.
# См. https://docs.djangoproject.com/en/dev/ref/settings/#datetime-format для получения информации о синтаксисе # строки формата
APSCHEDULER_DATETIME_FORMAT = "j.m.Y G:i:s"
# если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше, но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),  # Указываем, куда будем сохранять кэшируемые файлы
    }
}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
