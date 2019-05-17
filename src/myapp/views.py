import pathlib

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import (
    send_mail, send_mass_mail, mail_admins, mail_managers, EmailMessage, EmailMultiAlternatives
)
from django.core.mail.backends import console
from django.http import Http404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.views.generic import TemplateView, FormView

from myapp.forms import ShinshuFruitForm


def function_of_send_mail(request):
    """ send_mail()関数を使ったメール送信 """
    send_mail(subject='my subject',
              message='My Body',
              from_email=settings.REAL_MAIL_FROM,
              recipient_list=settings.REAL_MAIL_TO)
    return HttpResponse('function_of_send_mail!')


def display_name(request):
    """ メールアドレスに表示名を付けて送信 """
    email = EmailMessage(
        subject='EmailMessage',
        body='My Body',
        from_email='from_user <from@example.com>',
        to=['to_user <to@example.com>'],
        connection=console.EmailBackend(),
    )
    email.send()

    send_mail(subject='send_mail',
              message='My Body',
              from_email='from_user <from@example.com>',
              recipient_list=['to_user <to@example.com>'],
              connection=console.EmailBackend())

    return HttpResponse('display_name!')


def html_mail(request):
    """ HTMLメールを送信 """
    email = EmailMultiAlternatives(
        subject='EmailMessage',
        body='My Body',
        from_email=settings.REAL_MAIL_FROM,
        to=settings.REAL_MAIL_TO,
    )
    email.attach_alternative('<strong>HTMLメール</strong>です', 'text/html')
    email.send()

    send_mail(subject='send_mail',
              message='My Body',
              from_email=settings.REAL_MAIL_FROM,
              recipient_list=settings.REAL_MAIL_TO,
              html_message='<strong>HTMLメール</strong>です',
              )

    return HttpResponse('html_mail!')


def text_template(request):
    """ テンプレート(text)を使ったメール送信 """
    template_body = render_to_string('mail/content.txt', context={'message': '埋め込みます'})

    email = EmailMessage(
        subject='Email Message',
        body=template_body,
        from_email=settings.REAL_MAIL_FROM,
        to=settings.REAL_MAIL_TO,
    )
    email.send()

    send_mail(subject='send_mail',
              message=template_body,
              from_email=settings.REAL_MAIL_FROM,
              recipient_list=settings.REAL_MAIL_TO,
              )

    return HttpResponse('text_template!')


def text_jinja2_template(request):
    """ Jinja2テンプレートも使えるかを確認 """

    template_body = render_to_string('body.txt', context={'message': -123})

    send_mail(subject='send_mail',
              message=template_body,
              from_email=settings.REAL_MAIL_FROM,
              recipient_list=settings.REAL_MAIL_TO,
              )

    return HttpResponse('text_jinja2_template!')


def html_template(request):
    """ テンプレート(HTML)を使ったメール送信 """
    template_body = render_to_string('mail/image_content.html',
                                     context={'message': 'HTMLメールです'},
                                     request=request)
    email = EmailMultiAlternatives(
        subject='EmailMultiAlternatives',
        body='テキスト表示です',
        from_email=settings.REAL_MAIL_FROM,
        to=settings.REAL_MAIL_TO,
    )
    email.attach_alternative(template_body, 'text/html')
    email.send()

    send_mail(subject='send_mail',
              message='テキスト表示です',
              from_email=settings.REAL_MAIL_FROM,
              recipient_list=settings.REAL_MAIL_TO,
              html_message=template_body,
              )

    return HttpResponse('html_template!')


def attachment(request):
    """ 添付ファイル """

    # 静的ディレクトリにあるファイルを添付する
    static_file_dir = pathlib.Path(settings.STATICFILES_DIRS[0])
    image_file = static_file_dir.joinpath('images', 'shinanogold.png')

    # attach_file()を使う場合
    msg = EmailMessage(
        subject='attach_file',
        body='本文',
        from_email=settings.REAL_MAIL_FROM,
        to=settings.REAL_MAIL_TO,
    )
    msg.attach_file(image_file)
    msg.send()

    # __init__()を使う場合
    with image_file.open(mode='rb') as f:
        EmailMessage(
            subject='__init__',
            body='本文',
            from_email=settings.REAL_MAIL_FROM,
            to=settings.REAL_MAIL_TO,
            attachments=[('my.png', f.read(), 'image/png')],
        ).send()

    return HttpResponse('attachment!')


def encoding(request):
    """ エンコーディングの変更 """

    # デフォルトのまま送信
    EmailMessage(
        subject='件名です',
        body='My Body',
        from_email='from@example.com',
        to=['to@example.com'],
        connection=console.EmailBackend(),
    ).send()

    # ISO-2022-JPに変更して送信
    email = EmailMessage(
        subject='件名です',
        body='My Body',
        from_email='from@example.com',
        to=['to@example.com'],
        connection=console.EmailBackend(),
    )
    email.encoding = 'iso-2022-jp'
    email.send()

    return HttpResponse('encoding!')


def additional_header(request):
    """ メールヘッダへの追加 """
    email = EmailMessage(
        subject='my subject',
        body='My Body',
        from_email='from@example.com',
        to=['to@example.com'],
        headers={
            'Sender': 'sender@example.com',
        },
    )
    email.send()

    return HttpResponse('additional_header!')


def extend_backend(request):
    """ console.EmailBackendを拡張し、日本語件名をコンソール出力する

        settingsは、 `readable_subject`
    """

    # 件名がASCII文字列のみ
    EmailMessage(
        subject='Django',
        body='本文はテキスト表示です',
        from_email=settings.REAL_MAIL_FROM,
        to=settings.REAL_MAIL_TO,
    ).send()

    # 件名に日本語を含む
    EmailMessage(
        subject='ジャンゴ',
        body='こちらも本文はテキスト表示です',
        from_email=settings.REAL_MAIL_FROM,
        to=settings.REAL_MAIL_TO,
    ).send()

    return HttpResponse('extend_backend!')


def custom_backend(request):
    """ 自作したEmailBackendを使う

        settings.EMAIL_BACKEND に自作したEmailBackendを設定してあることを想定

        - SlackBackend -> `slack` を自分の環境に合わせて変更 ( `my_slack` など)
        - Iso2022JpEmailBackend -> `smtp_iso2022jp` を自分の環境に合わせて変更
    """
    EmailMessage(
        subject='ジャンゴ',
        body='DjangoCongress JP 2019 にようこそ！',
        from_email=settings.REAL_MAIL_FROM,
        to=settings.REAL_MAIL_TO).send()
    return HttpResponse('custom_backend!')


def user_model_shortcut(request):
    foo_user = User.objects.get(username='foo')
    if not foo_user:
        foo_user = User.objects.create_user(
            username='foo',
            email='foo@example.com',
            password=make_password('Passw0rd'),
        )
        foo_user.save()

    foo_user.email_user(
        subject='Hello',
        message='Welcome!',
        from_email='from@example.com',
        connection=console.EmailBackend(),
    )

    return HttpResponse('user_model_shortcut!')


def send_mail_shortcut(request):
    """ メール送信を行う send_mail() ショートカット関数 """
    send_mail(subject='shortcut subject',
              message='Shortcut Body',
              from_email=settings.REAL_MAIL_FROM,
              recipient_list=settings.REAL_MAIL_TO,  # Toのみ設定可能
              connection=console.EmailBackend())
    return HttpResponse('send_mail_shortcut!')


def send_mass_mail_shortcut(request):
    """ メール一括送信を行う send_mass_mail() ショートカット関数 """
    msg1 = ('shortcut subject1', 'Shortcut Body',
            'from1@example.com',
            ['to1_1@example.com', 'to1_2@example.com'])  # Toのみ設定可能
    msg2 = ('shortcut subject2', 'Shortcut Body',
            'from2@example.com',
            ['to2_1@example.com', 'to2_2@example.com'])

    send_mass_mail((msg1, msg2), connection=console.EmailBackend())
    return HttpResponse('send_mass_mail_shortcut!')


def mail_admins_shortcut(request):
    """ ADMINS宛メール送信を行う mail_admins() ショートカット関数

        settingsは、 `admins_and_managers`
    """
    mail_admins('dir admins', 'mail_adminsを実行しました', connection=console.EmailBackend())

    return HttpResponse('mail_admins_shortcut!')


def mail_managers_shortcut(request):
    """ MANAGERS宛メール送信を行う mail_managers() ショートカット関数

        settingsは、 `admins_and_managers`
    """
    mail_managers('dir managers', 'mail_managersを実行しました', connection=console.EmailBackend())

    return HttpResponse('mail_managers_shortcut!')


class BreakingLinkView(TemplateView):
    """ HTTP 404 を表示するためのリンクが含まれるHTMLを表示するためのView """
    template_name = 'myapp/breaking_link.html'


def force_404(request):
    """ 強制的に HTTP 404 を送出するView

        MAIL_MANGERSにエラーレポートが送信されることを想定
        ただし、直接アクセスした場合は、Refererがないため、エラーレポートは送信されない

        settingsは、 `admins_and_managers`
    """
    raise Http404('404!')


def force_500(request):
    """ 強制的に HTTP 500 を送出するView

        MAIL_ADMINSにエラーレポートが送信されることを想定

        settingsは、 `admins_and_managers`
    """
    my_local_value = 'ハロー'
    raise Exception('Error')


class FullOpenLocalVariableView(TemplateView):
    """ ローカル変数のマスク無し """
    template_name = 'myapp/breaking_link.html'

    def get(self, request, *args, **kwargs):
        conference = 'DjangoCongress'
        region = 'JP'
        year = '2019'

        raise Exception


@method_decorator(sensitive_variables('region', 'year'), name='dispatch')
class MaskedLocalVariableView(TemplateView):
    """ 一部ローカル変数をマスク """
    template_name = 'myapp/breaking_link.html'

    def get(self, request, *args, **kwargs):
        conference = 'DjangoCongress'
        region = 'JP'  # マスクする
        year = '2019'  # マスクする

        raise Exception


@method_decorator(sensitive_variables(), name='dispatch')
class AllMaskedLocalVariableView(TemplateView):
    """ 全ローカル変数をマスク """
    template_name = 'myapp/breaking_link.html'

    def get(self, request, *args, **kwargs):
        conference = 'DjangoCongress'
        region = 'JP'
        year = '2019'

        raise Exception


class PostParameterView(FormView):
    """ POSTデータのマスク無し """
    template_name = 'myapp/my_form.html'
    form_class = ShinshuFruitForm
    success_url = reverse_lazy('myapp:post_parameters')

    def post(self, request, *args, **kwargs):
        raise Exception


@method_decorator(sensitive_post_parameters('grape', 'pear'),
                  name='dispatch')
class MaskedPostParameterView(FormView):
    """ POSTデータを一部マスク """
    template_name = 'myapp/my_form.html'
    form_class = ShinshuFruitForm
    success_url = reverse_lazy('myapp:sensitive_post_parameters')

    def post(self, request, *args, **kwargs):
        raise Exception


@method_decorator(sensitive_post_parameters(), name='dispatch')
class AllMaskedPostParameterView(FormView):
    """ POSTデータをすべてマスク """
    template_name = 'myapp/my_form.html'
    form_class = ShinshuFruitForm
    success_url = reverse_lazy('myapp:all_sensitive_post_parameters')

    def post(self, request, *args, **kwargs):
        raise Exception


class NoDecoratorView(FormView):
    """ ローカル変数とPOSTデータ、decoratorでのマスク無し """
    template_name = 'myapp/my_form.html'
    form_class = ShinshuFruitForm
    success_url = reverse_lazy('myapp:double_mask')

    def post(self, request, *args, **kwargs):
        conference = 'DjangoCongress'
        region = 'JP'
        year = '2019'

        raise Exception


@method_decorator(sensitive_variables('year'), name='dispatch')
@method_decorator(sensitive_post_parameters('grape'), name='dispatch')
class DoubleMaskedView(FormView):
    """ ローカル変数とPOSTデータの両方マスクする """
    template_name = 'myapp/my_form.html'
    form_class = ShinshuFruitForm
    success_url = reverse_lazy('myapp:double_mask')

    def post(self, request, *args, **kwargs):
        conference = 'DjangoCongress'
        region = 'JP'
        year = '2019'

        raise Exception
