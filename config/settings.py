import os
from datetime import timedelta

import environ

root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(env.str(root(), default='.env'))

BASE_DIR = root()

SECRET_KEY = env.str(var='SECRET_KEY')
DEBUG = env.bool(var='DEBUG', default=False)
ALLOWED_HOSTS = env.str(var='ALLOWED_HOSTS', default='').split(' ')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #packages
    'rest_framework'
    'corsheaders',
    'djoser',
    'drf_spectacular',
    'debug_toolbar',
    #apps
    'api',
    'users',
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

ROOT_URLCONF = 'config.urls'

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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# region -------------------------- DATABASE ----------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str(var='PG_DATABASE', default='postgres'),
        'USER': env.str(var='PG_USER', default='postgres'),
        'PASSWORD': env.str(var='PG_PASSWORD', default='postgres'),
        'HOST': env.str(var='DB_HOST', default='localhost'),
        'PORT': env.int(var='DB_PORT', default=5432),
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# endregion -------------------------------------------------------------------------

# region --------------------- DJANGO REST FRAMEWORK --------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATED_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.BasePagination',
}
# endregion -------------------------------------------------------------------------


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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# region --------------------------- LOCALIZATION -----------------------------------
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
# endregion -------------------------------------------------------------------------

# region ------------------------- STATIC AND MEDIA ---------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_TEST_ROOT = os.path.join(BASE_DIR, 'media/test/')
# endregion -------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# region --------------------------- CORS HEADERS -----------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CSRF_COOKIE_SECURE = False
# endregion -------------------------------------------------------------------------

# region ------------------------ DRF SPECTACULAR -----------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Online Store',
    'DESCRIPTION': 'Online Store',
    'VERSION': '1.0.0',

    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated'
    ],

    'SERVE_AUTHENTICATION': [
        'rest_framework.authentication.BasicAuthentication'
    ],

    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayOperationId': True,
        'syntaxHighlight.active': True,
        'syntaxHighlight.theme': 'arta',
        'defaultModelsExpandDepth': -1,
        'displayRequestDuration': True,
        'filter': True,
        'requestSnippetsEnabled': True,
    },

    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}
# endregion -------------------------------------------------------------------------


# region ------------------------------ SMTP ----------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# Настройка почтового сервера по SMTP-протоколу
EMAIL_HOST = env.str(var='EMAIL_HOST')
EMAIL_PORT = env.int(var='EMAIL_PORT')
EMAIL_USE_TLS = env.bool(var='EMAIL_USE_TLS')
EMAIL_HOST_USER = env.str(var='EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str(var='EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER
# endregion -------------------------------------------------------------------------


# region ----------------------- DJOSER AND SIMPLE JWT-------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SERIALIZERS': {
        'user_create': 'users.serializers.api.users.RegistrationSerializer',
        'user': 'users.serializers.api.users.UserSerializer',
        'current_user': 'users.serializers.api.users.UserSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    },
}
# endregion -------------------------------------------------------------------------

# region ------------------ CUSTOM USER, CUSTOM BACKEND -----------------------------
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ('users.backends.AuthBackend',)
# endregion -------------------------------------------------------------------------

# # region ------------------------------- REDIS --------------------------------------
# REDIS_URL = env.str(var='REDIS_URL', default='redis://localhost:6379/0')
# # Кэш с помощью => Redis.
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': REDIS_URL,
#     }
# }
# # endregion -------------------------------------------------------------------------


# # region ------------------------------ YOOKASSA ------------------------------------
# YOOKASSA_SHOP_ID = env.int(var='YOOKASSA_SHOP_ID')
# YOOKASSA_SECRET_KEY = env.str(var='YOOKASSA_SECRET_KEY')
# YOOKASSA_RETURN_URL = env.str(var='YOOKASSA_RETURN_URL')
# # endregion -------------------------------------------------------------------------
