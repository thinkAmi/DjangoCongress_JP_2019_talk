import pathlib

from django.conf import settings
from django.core.mail import EmailMessage


def my_send_mail(encoding='utf-8', has_attachment=False):
    """ テスト対象の関数 """

    msg = EmailMessage(
        subject='件名',
        body='本文',
        from_email='差出人 <from@example.com>',
        to=['送信先1 <to1@example.com>', '送信先2 <to2@example.com>'],
        cc=['シーシー <cc@example.com>'],
        bcc=['ビーシーシー <bcc@example.com>'],
        reply_to=['返信先 <reply@example.com>'],
        headers={'Sender': 'sender@example.com'})

    # エンコーディングを変更する
    msg.encoding = encoding

    if has_attachment:
        # 静的ディレクトリにあるファイルを添付する
        img = pathlib.Path(settings.STATICFILES_DIRS[0]).joinpath(
            'images', 'shinanogold.png')
        msg.attach_file(img)

    msg.send()
