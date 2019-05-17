import re

from django.utils.log import DEFAULT_LOGGING

from .base import *

# 後で確認できるよう、ファイルとして残しておく
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

# filebasedを使う場合は、メールの保存先も指定すること
# '.' の場合、カレントディレクトリに保存される
# EMAIL_FILE_PATH = '.'
EMAIL_FILE_PATH = str(pathlib.Path(BASE_DIR).joinpath('logs'))

# 管理者系の設定
# mail_admins()で使用する
# https://docs.djangoproject.com/en/2.2/topics/email/#mail-admins
ADMINS = [('Admin1', 'admin1@example.com')]

# mail_managers()で使用する
# https://docs.djangoproject.com/en/2.2/topics/email/#mail-managers
MANAGERS = [('Manager1', 'manager1@example.com')]

# mail_admins()とmail_managers()の両方で使う設定
SERVER_EMAIL = 'server@example.com'
EMAIL_SUBJECT_PREFIX = '[DjangoCongress JP]'

# エラーレポートメールを受信可能にするため、本番運用モードにしておく
DEBUG = False

# settingsのうち、エラーレポートでフィルタされる設定名を定義
# https://docs.djangoproject.com/ja/2.2/ref/settings/#debug
DJANGO_CONGRESS_PASSWORD = '123'
DJANGO_CONGRESS_PASSPORT = '456'
DJANGO_CONGRESS_PASTA = '789'

# エラーレポートメールでローカル変数も出力するように修正
DEFAULT_LOGGING['handlers']['mail_admins']['include_html'] = True

# HTTP404でMAILを送信するために必要
# https://docs.djangoproject.com/ja/2.2/howto/error-reporting/#errors
MIDDLEWARE += ['django.middleware.common.BrokenLinkEmailsMiddleware']

# HTTP404でもエラーレポートメールを送信したくないURLがある場合は、正規表現で指定
IGNORABLE_404_URLS = [
    re.compile(r'^/ignore_404$'),
]

