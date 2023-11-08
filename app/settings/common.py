"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os.path
from pathlib import Path

from decouple import config, Csv


def __get_base_dir() -> str:
    """
    Returns the root project directory
    :return:
    """
    current_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(current_path, '..', '..')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str)

CRUNCHY_TOKEN = config("DJANGO_CRUNCHY_TOKEN", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())

# Application definition

INSTALLED_APPS = [
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphql_playground",
    "graphene_django",
    "django_filters",
    "django_q",
    "corsheaders",
    "app.modules.service",
    "core",
    "crunchy",
    "manami",
    "xem",
    "media",
    "home",
    "config",
    "navigation",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "core.middleware.HeaderMiddleware",
    "core.middleware.FeatureFlagMiddleware",
    'core.middleware.CustomRollbarNotifierMiddleware',
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": config("DJANGO_DATABASE_NAME", cast=str),
        "USER": config("DJANGO_DATABASE_USER", cast=str),
        "PASSWORD": config("DJANGO_DATABASE_PASSWORD", cast=str),
        "HOST": config("DJANGO_DATABASE_HOST", cast=str),
        "PORT": config("DJANGO_DATABASE_PORT", cast=int),
    },
}

# https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    "name": config("DJANGO_Q_NAME", cast=str),
    "orm": config("DJANGO_Q_ORM", cast=str),
    "workers": config("DJANGO_Q_WORKERS", cast=int),
    "recycle": config("DJANGO_Q_RECYCLE", cast=int),
    "timeout": config("DJANGO_Q_TIMEOUT", cast=int),
    "retry": config("DJANGO_Q_RETRY", cast=int),
    "label": config("DJANGO_Q_LABEL", cast=str),
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config("DJANGO_REDIS_URI", cast=str),
    }
}

GRAPHENE = {
    "SCHEMA": "app.graphql.schema.schema",
    "SCHEMA_OUTPUT": "static/schema.json",
    "SCHEMA_INDENT": 2,
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = config("DJANGO_LANGUAGE_CODE", default="en-us", cast=str)

TIME_ZONE = config("DJANGO_TIME_ZONE", default="UTC", cast=str)

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_METHODS = (
    "GET",
    "OPTIONS",
    "POST",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
            "style": "%",
        },
        "simple": {
            "format": "{name} at {asctime} ({levelname}) :: {message}",
            "style": "{"
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "rollbar": {
            "level": "WARNING",
            "filters": ["require_debug_false"],
            "access_token": config('ROLLBAR_TOKEN', cast=str),
            "environment": "development" if DEBUG else "production",
            "class": "rollbar.logger.RollbarHandler"
        },
        "logtail": {
            "level": "INFO",
            "class": "logtail.LogtailHandler",
            "formatter": "simple",
            "source_token": config("LOGTAIL_SOURCE_TOKEN", cast=str)
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "logtail"],
            "propagate": True,
        },
        "root": {
            "handlers": ["rollbar", "logtail"],
            "propagate": True,
        },
    },
}

GROWTH_BOOK = {
    "host": config("GROWTH_BOOK_HOST", cast=str),
    "key": config("GROWTH_BOOK_KEY", cast=str),
    "ttl": config("GROWTH_BOOK_TTL", cast=int),
}

ROLLBAR = {
    'access_token': config("ROLLBAR_TOKEN", cast=str),
    'environment': 'development' if DEBUG else 'production',
    'code_version': '1.0',
    'root': BASE_DIR,
}
