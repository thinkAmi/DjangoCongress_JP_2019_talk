from django.conf import settings
from django.core.mail.backends import console, smtp
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
from slackclient import SlackClient


class ReadableSubjectEmailBackend(console.EmailBackend):
    """ console.EmailBackendを拡張し、コンソールに件名(日本語)も表示 """

    def write_message(self, message):
        from email.header import decode_header
        subject = message.message().get('Subject')
        decoded_tuple = decode_header(subject)

        print(decoded_tuple)
        # => [('Django', None)]  # MIMEヘッダエンコーディングなし
        # => [(b'\xe3\x82\xb8\xe3\x83\xa3\xe3\x83\xb3\xe3\x82\xb4', 'utf-8')]  # あり

        if decoded_tuple[0][1] is not None:
            readable_subject = decoded_tuple[0][0].decode(
                decoded_tuple[0][1])

            self.stream.write('-' * 30)
            self.stream.write(f'\nSubject (日本語表示): {readable_subject}\n')
            self.stream.write('-' * 30)
            self.stream.write('\n')

        super().write_message(message)


class SlackBackend(BaseEmailBackend):
    """ SlackへポストするEmailBackendを自作 """

    def send_messages(self, email_messages):
        # 本文を取得し、SlackへPOSTする
        payload = email_messages[0].message().get_payload()
        print(payload)
        client = SlackClient(settings.SLACK_OAUTH_ACCESS_TOKEN)
        client.api_call(
            'chat.postMessage',
            channel=settings.SLACK_CHANNEL,
            text=payload,
        )


class Iso2022JpEmailBackend(smtp.EmailBackend):
    """ 常にメールエンコード ISO-2022-JP で送信する smtp.EmailBackend """

    def _send(self, email_message):
        if isinstance(email_message, EmailMessage):
            email_message.encoding = 'iso-2022-jp'
        return super()._send(email_message)
