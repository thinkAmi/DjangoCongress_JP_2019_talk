from django.utils.log import DEFAULT_LOGGING

from .base import *

# 後で確認できるよう、ファイルとして残しておく
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

# filebasedを使う場合は、メールの保存先も指定すること
# '.' の場合、カレントディレクトリに保存される
# EMAIL_FILE_PATH = '.'
EMAIL_FILE_PATH = str(pathlib.Path(BASE_DIR).joinpath('logs'))

ADMINS = [('Admin1', 'admin1@example.com')]

# エラーレポートメールを受信可能にするため、本番運用モードにしておく
DEBUG = False

# エラーレポートメールでローカル変数も出力するように修正
DEFAULT_LOGGING['handlers']['mail_admins']['include_html'] = True

# エラーレポートをカスタマイズする
DEFAULT_EXCEPTION_REPORTER_FILTER = 'myapp.reporter_filter.MyReporterFilter'
