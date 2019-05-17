from .base import *


EMAIL_BACKEND = 'myapp.email_backends.SlackBackend'

# channels:readとchat:write:botをScopeに持つSlack API Appを追加し、OAuth Access Tokenを取得
SLACK_OAUTH_ACCESS_TOKEN = 'Your OAuth Access Token'


# 以下をREPLで実行し、対象のChannel IDを取得する
# ref: https://realpython.com/getting-started-with-the-slack-api-using-python-and-flask/
"""
from slackclient import SlackClient

slack_client = SlackClient(SLACK_OAUTH_ACCESS_TOKEN)
ch = slack_client.api_call("channels.list")['channels']
for c in ch:
    print(f'{c["name"]} -> id: {c["id"]}')
"""
SLACK_CHANNEL = 'Your Channel ID'
