from .base import *
from decouple import config
import sentry_sdk
import dj_database_url

DEBUG = False

SECRET_KEY = config(
  'SECRET_KEY'
)

CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = config(
  'ALLOWED_HOSTS'
).split(',')

SENTRY_DSN = config(
  'SENTRY_DSN',
  default=''
)

if SENTRY_DSN:
  sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0
  )

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
}