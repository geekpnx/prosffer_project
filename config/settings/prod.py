from .base import *
import environs

env = environs.Env()

env.read_env(str(BASE_DIR / '.env.prod'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"] # This is where you will add your public "IP Address", "localhost", "domain.com", also below you need to activate the CSRF_TRUSTED_ORIGINS add your "http://ip-public" or "http://domain.com"
# CSRF_TRUSTED_ORIGINS= [
#     "*"
# ] 

THIRD_PARTY_APPS = [
    # USER DEFINED APPS
]

MIDDLEWARE = MIDDLEWARE + ["whitenoise.middleware.WhiteNoiseMiddleware"]

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

MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "media")