import pathlib
from tempfile import TemporaryDirectory

import pyminizip
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.utils.log import AdminEmailHandler


class MyAdminEmailHandler(AdminEmailHandler):
    """ エラーレポートHTMLを、パスワード付zipファイル化し、メールに添付して送信 """
    def send_mail(self, subject, message, *args, **kwargs):
        with TemporaryDirectory() as temp_dir:
            html_file = pathlib.Path(temp_dir).joinpath('report.html')
            with html_file.open('w') as f:
                f.write(kwargs.get('html_message'))
            zip_file = pathlib.Path(temp_dir).joinpath('dst.zip')
            pyminizip.compress(str(html_file), None,
                               str(zip_file), 'pass', 0)
            msg = EmailMessage('my subject', 'My Body',
                               settings.REAL_MAIL_FROM,
                               settings.REAL_MAIL_TO)
            msg.attach_file(zip_file)
            msg.send()
