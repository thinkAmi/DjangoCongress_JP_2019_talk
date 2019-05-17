from .base import *
import os

TEMPLATES = [
    {
        # Viewは、Djangoエンジン
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        # メールは、Jinja2エンジン
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'template_jinja2')],
    },
]

# 念のため、コンソール出力
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
