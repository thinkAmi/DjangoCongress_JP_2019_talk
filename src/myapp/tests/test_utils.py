import pathlib

from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
from django.test import TestCase


class TestSendMail(TestCase):
    def _callFUT(self, encoding='utf-8', has_attachment=False):
        from myapp.utils import my_send_mail
        my_send_mail(encoding=encoding, has_attachment=has_attachment)

    def test_send_multiple(self):
        # 実行前はメールボックスに何もない
        self.assertEqual(len(mail.outbox), 0)

        # 1回実行すると、メールが1通入る
        self._callFUT()
        self.assertEqual(len(mail.outbox), 1)

        # もう1回実行すると、メールが2通入る
        self._callFUT()
        self.assertEqual(len(mail.outbox), 2)

    def test_types(self):
        self._callFUT()

        # list(EmailMessage(), ...) な型
        self.assertTrue(isinstance(mail.outbox, list))
        self.assertTrue(isinstance(mail.outbox[0], EmailMessage))

    def test_mail_fields(self):
        self._callFUT()
        actual = mail.outbox[0]

        self.assertEqual(actual.subject, '件名')
        self.assertEqual(actual.body, '本文')
        self.assertEqual(actual.from_email, '差出人 <from@example.com>')

        # 宛先系はlistとして設定
        self.assertEqual(actual.to,
                         ['送信先1 <to1@example.com>',
                          '送信先2 <to2@example.com>'],)
        self.assertEqual(actual.cc, ['シーシー <cc@example.com>'])
        self.assertEqual(actual.bcc, ['ビーシーシー <bcc@example.com>'])
        self.assertEqual(actual.reply_to, ['返信先 <reply@example.com>'])

        # 追加ヘッダも含まれること
        self.assertEqual(actual.extra_headers['Sender'], 'sender@example.com')

    def test_encoding_of_iso2022jp(self):
        self._callFUT(encoding='iso-2022-jp')
        actual = mail.outbox[0]

        # EmailMessageには、utf-8で格納されている
        self.assertEqual(actual.subject, '件名')

    def test_attachment(self):
        self._callFUT(has_attachment=True)
        actual = mail.outbox[0]

        self.assertTrue(isinstance(actual.attachments, list))
        # (filename, content, mimetype) なtuple
        self.assertTrue(isinstance(actual.attachments[0], tuple))
        # 添付ファイルの中身の型はbytes
        self.assertTrue(isinstance(actual.attachments[0][1], bytes))

        # 添付ファイル自体を検証
        img = pathlib.Path(settings.STATICFILES_DIRS[0]).joinpath(
            'images', 'shinanogold.png')
        with img.open('rb') as f:
            expected_img = f.read()
            self.assertEqual(actual.attachments[0][1], expected_img)
