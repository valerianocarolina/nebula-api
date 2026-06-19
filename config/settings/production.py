from .base import *
from decouple import config
import sentry_sdk

DEBUG = False

SECRET_KEY = config(
  'SECRET_KEY'
)

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