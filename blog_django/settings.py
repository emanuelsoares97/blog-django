"""
Django settings for blog_django project.

- Works for local development and production on Render
- Static files: WhiteNoise (hashed + gzip/brotli)
- Media files: Cloudinary (uploads only)
"""

import os
import sys
from pathlib import Path


# Base paths and environment

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env in development only (Render injects env vars)
DJANGO_ENV = os.environ.get("DJANGO_ENV", "development")
if DJANGO_ENV != "production":
    try:
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR / ".env")
    except Exception:
        pass


# Core security flags

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY not found! Define in .env (dev) or provider (prod).")

DEBUG = DJANGO_ENV != "production"

# Allowed hosts:
# - in prod we read a single host from RENDER_DOMAIN (e.g., myapp.onrender.com or custom domain)
# - in dev we allow localhost
if DJANGO_ENV == "production":
    RENDER_DOMAIN = os.environ.get("RENDER_DOMAIN")
    if not RENDER_DOMAIN:
        raise Exception("RENDER_DOMAIN not found in environment!")
    ALLOWED_HOSTS = [RENDER_DOMAIN]
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Applications

INSTALLED_APPS = [
    # Django contrib (keep staticfiles here to use default collectstatic pipeline)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",

    # Third-party
    "crispy_forms",
    "crispy_bootstrap4",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",

    # Cloudinary for MEDIA only (do not override STATIC)
    "cloudinary",
    "cloudinary_storage",

    # Project apps
    "users.apps.UsersConfig",
    "blog.apps.BlogConfig",
    "private_messages",
    "notifications.apps.NotificationsConfig",
]

SITE_ID = 1


# Middleware

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise must be directly after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "blog_django.urls"
WSGI_APPLICATION = "blog_django.wsgi.application"


# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "blog.context_processors.sidebar_data",
                "notifications.context_processors.unread_notifications_count",
            ],
        },
    },
]


# Database
# - In prod: set DB_* env vars (Render Postgres)
# - In tests: use in-memory SQLite for speed and isolation

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }


# Email

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend"
)


# Authentication / Allauth

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_ADAPTER = "users.adapters.MySocialAccountAdapter"

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {"client_id": GOOGLE_CLIENT_ID, "secret": GOOGLE_CLIENT_SECRET},
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online", "prompt": "select_account"},
        "METHOD": "oauth2",
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# I18N

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS/JS) via WhiteNoise
# - We use Manifest + compression for cache-busting and performance
# - Sources:
#   - App static: <app>/static/<app>/...
#   - Optional project static: <BASE_DIR>/static  (if it exists)
# - Output:
#   - <BASE_DIR>/staticfiles  (collectstatic destination)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Ensure default finders are in place
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",      # for STATICFILES_DIRS
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",  # for <app>/static
]

# Hashed names + gzip/brotli (WhiteNoise will handle compression files)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Media files via Cloudinary (uploads only, not static)

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}


# Auth redirects

LOGIN_REDIRECT_URL = "blog-home"
LOGOUT_REDIRECT_URL = "login"
LOGIN_URL = "login"
CRISPY_TEMPLATE_PACK = "bootstrap4"


# Production security

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"


# Logging

LOGS_DIR = BASE_DIR / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"standard": {"format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"}},
    "handlers": {
        "general_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "logs_geral.log",
            "formatter": "standard",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "logs_erros.log",
            "formatter": "standard",
        },
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "logs_debug.log",
            "formatter": "standard",
        },
    },

}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
