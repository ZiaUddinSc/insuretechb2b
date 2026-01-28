from .base import *
from config.env import env
env.read_env(os.path.join(BASE_DIR, '.env.production'))
DEBUG = env.bool('DJANGO_DEBUG',default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
# SECRET_KEY='django-insecure-l$v6%d6nk%j8wq)_1b)=pjkf5=i0a)l)@sj-@xwoammq-_h2%x'

"""SERVER POSTGRESQUL DATABASE SETUP"""

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE", default="django.db.backends.postgresql_psycopg2"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST", default="localhost"),
        "PORT": env.int("DATABASE_PORT", default=5432)
    }
}

"""Email Configuration"""

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # pwaw terg qlws dmlo
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
