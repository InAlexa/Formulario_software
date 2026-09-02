from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY", default="clave-de-desarrollo-cambiar-en-produccion")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "apps.registro",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

# --- Base de datos: PostgreSQL/MySQL ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql", #postgresql
        "NAME": config("DB_NAME", default="registro_db"),
        "USER": config("DB_USER", default="root"),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="3306"),
        "OPTIONS": {"charset": "utf8mb4"}, # Quitar en postgresql
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Guatemala"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# --- CORS (ajustar en producción) ---
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", default="http://localhost:5173"
).split(",")

EMAIL_VERIFICATION_PROVIDER = config("EMAIL_VERIFICATION_PROVIDER", default="resend")

# --- Supabase (usado solo para verificación de correo) ---
SUPABASE_URL = config("SUPABASE_URL", default="")
SUPABASE_ANON_KEY = config("SUPABASE_ANON_KEY", default="")
SUPABASE_JWT_SECRET = config("SUPABASE_JWT_SECRET", default="")
SUPABASE_EMAIL_REDIRECT_URL = config(
    "SUPABASE_EMAIL_REDIRECT_URL", default="http://localhost:5173/verificado"
)

# --- Resend (usado solo para verificación de correo) ---
RESEND_API_KEY = config("RESEND_API_KEY", default="")
RESEND_FROM_EMAIL = config("RESEND_FROM_EMAIL", default="")
EMAIL_VERIFICATION_REDIRECT_URL = config(
    "EMAIL_VERIFICATION_REDIRECT_URL", default="http://localhost:5173/verificado"
)