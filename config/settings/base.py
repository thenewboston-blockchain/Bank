import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Requirements
    'channels',
    'corsheaders',
    'django_filters',
    'rest_framework',

    # API (v1) network nodes
    'v1.banks.apps.BanksConfig',
    'v1.validators.apps.ValidatorsConfig',

    # API (v1)
    'v1.accounts.apps.AccountsConfig',
    'v1.bank_transactions.apps.BankTransactionsConfig',
    'v1.blocks.apps.BlocksConfig',
    'v1.confirmation_blocks.apps.ConfirmationBlocksConfig',
    'v1.connection_requests.apps.ConnectionRequestsConfig',
    'v1.invalid_blocks.apps.InvalidBlocksConfig',
    'v1.self_configurations.apps.SelfConfigurationsConfig',
    'v1.validator_confirmation_services.apps.ValidatorConfirmationServicesConfig',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
ASGI_APPLICATION = 'config.routing.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'thenewboston'),
        'USER': os.getenv('POSTGRES_USER', 'thenewboston'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'thenewboston'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432')
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_WORKER_CONCURRENCY = 1
CELERY_BROKER_URL = f'redis://{os.getenv("REDIS_HOST", "localhost")}'
CELERY_RESULT_BACKEND = f'redis://{os.getenv("REDIS_HOST", "localhost")}'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{os.getenv("REDIS_HOST", "localhost")}:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

LOGGING = {
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'error.handler': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'error.log'),
            'formatter': 'verbose',
            'level': 'ERROR',
        },
        'warning.handler': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'warning.log'),
            'formatter': 'verbose',
            'level': 'WARNING',
        },
    },
    'loggers': {
        'thenewboston': {
            'handlers': ['error.handler', 'warning.handler'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
    'version': 1,
}

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'v1.third_party.rest_framework.pagination.LimitOffsetPagination',
}

PAGINATION_DEFAULT_LIMIT = 50
PAGINATION_MAX_LIMIT = 100

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.getenv('REDIS_HOST', '127.0.0.1'), 6379)],
        },
    },
}
