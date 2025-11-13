"""
Django settings for example_project project.
"""
# ruff: noqa: ERA001

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-example-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jodit',  # django-jodit
    'blog',  # Example blog app
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

ROOT_URLCONF = 'example_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'example_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Jodit Version Settings (Optional)
# By default, django-jodit uses the bundled Jodit version (4.7.9)
# You can override these to use a different version from CDN or local files

# Option 1: Use bundled version (default)
# JODIT_JS_URL = None
# JODIT_CSS_URL = None

# Option 2: Use specific version from CDN
# JODIT_JS_URL = 'https://unpkg.com/jodit@4.7.9/es2021/jodit.min.js'
# JODIT_CSS_URL = 'https://unpkg.com/jodit@4.7.9/es2021/jodit.min.css'

# Option 3: Use latest version from CDN (not recommended for production)
# JODIT_JS_URL = 'https://unpkg.com/jodit@latest/es2021/jodit.min.js'
# JODIT_CSS_URL = 'https://unpkg.com/jodit@latest/es2021/jodit.min.css'

# Option 4: Use custom local files
# JODIT_JS_URL = '/static/custom/jodit.min.js'
# JODIT_CSS_URL = '/static/custom/jodit.min.css'

# Jodit Editor Configuration
JODIT_CONFIGS = {
    'default': {
        'height': 400,
        'width': '100%',
        'toolbar': True,
        'spellcheck': True,
        'language': 'auto',
        'theme': 'auto',  # Auto-detect dark/light theme from Django admin or system
        'toolbarButtonSize': 'middle',
        'toolbarAdaptive': True,
        'showCharsCounter': True,
        'showWordsCounter': True,
        'showXPathInStatusbar': False,
        'askBeforePasteHTML': True,
        'askBeforePasteFromWord': True,
        'buttons': [
            'source',
            '|',
            'bold',
            'italic',
            'underline',
            'strikethrough',
            '|',
            'ul',
            'ol',
            '|',
            'outdent',
            'indent',
            '|',
            'font',
            'fontsize',
            'brush',
            'paragraph',
            '|',
            'image',
            'table',
            'link',
            '|',
            'align',
            'undo',
            'redo',
            '|',
            'hr',
            'eraser',
            'copyformat',
            '|',
            'symbol',
            'fullsize',
            'print',
        ],
        'uploader': {
            'insertImageAsBase64URI': True,
        },
    },
    'simple': {
        'height': 200,
        'width': '100%',
        'toolbar': True,
        'theme': 'auto',  # Auto-detect theme
        'showCharsCounter': False,
        'showWordsCounter': False,
        'showXPathInStatusbar': False,
        'buttons': [
            'bold',
            'italic',
            'underline',
            '|',
            'ul',
            'ol',
            '|',
            'link',
            '|',
            'undo',
            'redo',
        ],
    },
    'advanced': {
        'height': 600,
        'width': '100%',
        'toolbar': True,
        'theme': 'auto',  # Auto-detect theme
        'toolbarButtonSize': 'large',
        'buttons': [
            'source',
            '|',
            'bold',
            'italic',
            'underline',
            'strikethrough',
            '|',
            'superscript',
            'subscript',
            '|',
            'ul',
            'ol',
            '|',
            'outdent',
            'indent',
            '|',
            'font',
            'fontsize',
            'brush',
            'paragraph',
            '|',
            'image',
            'video',
            'table',
            'link',
            '|',
            'align',
            'undo',
            'redo',
            '|',
            'hr',
            'eraser',
            'copyformat',
            '|',
            'symbol',
            'fullsize',
            'preview',
            'print',
            '|',
            'about',
        ],
    },
    'dark': {
        'height': 400,
        'width': '100%',
        'toolbar': True,
        'theme': 'dark',  # Force dark theme
        'buttons': [
            'bold',
            'italic',
            'underline',
            '|',
            'ul',
            'ol',
            '|',
            'link',
            'image',
            '|',
            'undo',
            'redo',
        ],
    },
}
