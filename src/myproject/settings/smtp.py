from .base import *

# デフォルトのEMAIL_BACKENDはSMTPなので省略可
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'your host name or ip address'
EMAIL_PORT = 'your host port'
EMAIL_HOST_USER = 'your host user'
EMAIL_HOST_PASSWORD = 'your host password'
