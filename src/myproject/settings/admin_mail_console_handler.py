from .base import *

# 後で確認できるよう、ファイルとして残しておく
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

# filebasedを使う場合は、メールの保存先も指定すること
# '.' の場合、カレントディレクトリに保存される
# EMAIL_FILE_PATH = '.'
EMAIL_FILE_PATH = str(pathlib.Path(BASE_DIR).joinpath('logs'))

ADMINS = [('Admin1', 'admin1@example.com')]

# 開発モードでもADMINSへエラー通知メールを送信する
DEBUG = True

# EMAIL_BACKENDの設定とは別に、エラー通知メールはコンソール出力にする
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend':
                'django.core.mail.backends.console.EmailBackend',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
    }
}