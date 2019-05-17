from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

# filebasedを使う場合は、メールの保存先も指定すること
# '.' の場合、manage.py のディレクトリにメールがファイルとして保存される
EMAIL_FILE_PATH = '.'
