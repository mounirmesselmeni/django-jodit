"""Django settings for testing django-jodit."""

# ruff: noqa: ERA001

SECRET_KEY = "test-secret-key-for-django-jodit"

DEBUG = True

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jodit",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = []

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

STATIC_URL = "/static/"

USE_TZ = True

# Jodit version settings (optional - defaults to bundled version)
# JODIT_JS_URL = 'https://unpkg.com/jodit@4.7.9/es2021/jodit.min.js'
# JODIT_CSS_URL = 'https://unpkg.com/jodit@4.7.9/es2021/jodit.min.css'

# Custom Jodit configurations for testing
JODIT_CONFIGS = {
    "default": {
        "height": 400,
        "width": "100%",
        "toolbar": True,
        "theme": "auto",  # Auto-detect theme
    },
    "simple": {
        "height": 200,
        "toolbar": False,
        "theme": "auto",
    },
    "advanced": {
        "height": 600,
        "buttons": ["bold", "italic", "underline", "link"],
        "theme": "auto",
    },
    "dark": {
        "height": 400,
        "theme": "dark",  # Force dark theme
    },
    "light": {
        "height": 400,
        "theme": "default",  # Force light theme
    },
}
