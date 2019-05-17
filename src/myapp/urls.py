from django.urls import path

from myapp import views

app_name = 'myapp'

urlpatterns = [
    # 簡単Djangoメール
    path('send_mail', views.function_of_send_mail, name='send_mail'),

    # 表示名
    path('display_name', views.display_name, name='display_name'),

    # HTMLメール
    path('html_mail', views.html_mail, name='html_mail'),

    # テンプレートファイルを使ったメール
    path('text_template', views.text_template, name='text_template'),   # テキストテンプレート
    path('html_template', views.html_template, name='html_template'),   # HTMLテンプレート
    path('jinja2_template', views.text_jinja2_template, name='jinja2'), # Jinja2テンプレート

    # 添付ファイル
    path('attachment', views.attachment, name='attachment'),

    # エンコーディング変更
    path('encoding', views.encoding, name='encoding'),

    # メールヘッダの追加
    path('additional_header', views.additional_header, name='additional_header'),

    # EmailBackendの拡張
    path('extend_backend', views.extend_backend, name='extend_backend'),

    # EmailBackendの自作
    path('custom_backend', views.custom_backend, name='custom_backend'),

    # ショートカット関数
    path('user', views.user_model_shortcut, name='user_shortcut'),
    path('send_mail_shortcut', views.send_mail_shortcut, name='send_mail_shortcut'),
    path('send_mass_mail_shortcut', views.send_mass_mail_shortcut, name='send_mass_mail_shortcut'),

    # 管理者宛メール
    path('mail_admins_shortcut', views.mail_admins_shortcut,
         name='mail_admins_shortcut'),    # ADMINS宛
    path('mail_managers_shortcut', views.mail_managers_shortcut,
         name='mail_managers_shortcut'),  # MANAGERS宛

    # エラー通知メールの送信
    path('breaking_link', views.BreakingLinkView.as_view(), name='link'),
    path('force_404', views.force_404, name='http_404'),  # HTTP 404 強制エラー
    path('ignore_404', views.force_404, name='http_404'), # HTTP 404 強制エラー(通知は無し)
    path('force_500', views.force_500, name='http_500'),  # HTTP 500 強制エラー

    # エラー通知メールにおける、ローカル変数のマスク
    path('local_variables', views.FullOpenLocalVariableView.as_view(),
         name='local_variables'),          # マスクなし
    path('sensitive_variables', views.MaskedLocalVariableView.as_view(),
         name='sensitive_variables'),      # 一部
    path('all_sensitive_variables', views.AllMaskedLocalVariableView.as_view(),
         name='all_sensitive_variables'),  # すべて

    # エラー通知メールにおける、POSTデータのマスク
    path('post_parameters', views.PostParameterView.as_view(),
         name='post_parameters'),                # マスクなし
    path('sensitive_post_parameters', views.MaskedPostParameterView.as_view(),
         name='sensitive_post_parameters'),      # 一部
    path('all_sensitive_post_parameters', views.AllMaskedPostParameterView.as_view(),
         name='all_sensitive_post_parameters'),  # すべて

    # エラー通知メールにおける、ローカル変数とPOSTデータの両方をマスク
    path('double_mask', views.DoubleMaskedView.as_view(),
         name='double_mask'),

    # デコレータではなく、SafeExceptionReporterFilterのサブクラスを自作してマスク
    # この場合、settingsは `custom_reporter_filter` を想定
    path('no_decorator', views.NoDecoratorView.as_view(), name='no_decorator'),
]
