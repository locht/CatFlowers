import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'crispy_forms',
    'django_countries',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'stripe',

    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'CatFlowers.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = "E:/HRLAPP/shopL/static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Auth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_VERIFICATION = 'none'  # Fix Error [Windows 10061]

# CRISPY FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STRIPE KEY
STRIPE_SECRET_KEY = 'sk_test_51HBehgKHBhzwvZk1OtcoZQETPbDz2jYPeUVNvmc7O1Hy2ZBTgP8vhWemuePvuxh3gXYechkIyWHp2j9yi1vq9urf00aPCDtE2N'
# if DEBUG:
#     STRIPE_PUBLISHABLE_KEY = ''
#     STRIPE_SECRET_KEY = ''
# else:
#     STRIPE_PUBLISHABLE_KEY = 'pk_test_51HBehgKHBhzwvZk10P5A2R1JeBAD4XM0fE5fm9SR15ZbffUAsrdwF8UTFQRh5V2bDB8MmYkIFOzUFUxyZNWUPXjL00ZA9FgPK3'
#     STRIPE_SECRET_KEY = 'sk_test_51HBehgKHBhzwvZk1OtcoZQETPbDz2jYPeUVNvmc7O1Hy2ZBTgP8vhWemuePvuxh3gXYechkIyWHp2j9yi1vq9urf00aPCDtE2N'

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)

# STATICFILES_STORAGE = (
#     'whitenoise.django.GzipManifestStaticFilesStorage'
# )
