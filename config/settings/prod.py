from .base import *
import environs

env = environs.Env()

env.read_env(str(BASE_DIR / '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]
# CSRF_TRUSTED_ORIGINS= [
#     "*"
# ]

THIRD_PARTY_APPS = [
    # USER DEFINED APPS
]

MIDDLEWARE = MIDDLEWARE + ["whitenose.middleware.WhiteNoiseMiddleware"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str('DB_NAME'),
        "USER": env.str('DB_USER'),
        "PASSWORD": env.str('DB_PWD'),
        "PORT": env.str('DB_PORT'),
        "HOST": env.str('DB_HOST')
    }
}

STATIC_ROOT = str(BASE_DIR /"staticfiles")
STATICFILES_DIRS = (str(BASE_DIR / "static"),)


