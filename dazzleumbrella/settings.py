"""
Django settings for dazzleumbrella project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv



load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
# }

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '3.109.166.213','www.dazzleumbrella.shop']


AUTH_USER_MODEL = 'core.CustomUser'


INSTALLED_APPS = [
    # 'admin_tools_stats',
    # 'django_nvd3',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #custom_apps
    'core',
    'store',
    #Third_party_apps
    "debug_toolbar",
    "colorfield",
    'django_celery_results',
  

]

JET_DEFAULT_THEME = 'green'

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'dazzleumbrella.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #custom context_processor
                'store.context_processors.count',
                'store.context_processors.custom_admin_context'
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',  
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': os.environ.get('DB_NAME'),
       'USER': os.environ.get('DB_USER'),
       'PASSWORD': os.environ.get('DB_PASSWORD'),
       'HOST': os.environ.get('HOST'),
       'PORT': os.environ.get('PORT'),
   }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/staticfiles/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_ROOT = '/home/ubuntu/Dazzle_ecom/static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    'https://www.dazzleumbrella.shop',  
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

#email verification

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')

# CELERY SETTINGS
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
# CELERY_ACCEPT_CONTENT = {'application/json'}
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Kolkata'
# CELERY_RESULT_BACKEND = 'django-db'

#custom admin interface

JAZZMIN_SETTINGS = {
    "site_title": "DAZZLE Admin",
    'site_header': 'DAZZLE',
    "site_brand": "Dazzle",
    'site_logo': '/images/logo.png',
    'copyright':'https://github.com/ajin-em',
}
# JAZZMIN_SETTINGS["show_ui_builder"] = True

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "superhero",
    "dark_mode_theme": "slate",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-success",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-warning"
    },
    "actions_sticky_top": False
}

INTERNAL_IPS = [
    "INTERNAL_IPS",
]

AUTHENTICATION_BACKENDS = ['core.backends.CustomUserBackend']

SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'

LOGIN_URL = 'signin'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'home'

# razor_pay
RAZORPAY_API_KEY = os.environ.get('razor_pay_key_id')
RAZORPAY_API_SECRET = os.environ.get('key_secret') 
