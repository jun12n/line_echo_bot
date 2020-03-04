import os
import sys
import re
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReplyButton, QuickReply, MessageAction
)
from weather_forecast import get_day5_data, make_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    locations = ['神戸', '岡山']
    if re.findall('天気|weather', event.message.text):
        items = [QuickReplyButton(action=MessageAction(label=f"{loc}", text=f"{loc}")) for loc in locations]
        messages = TextSendMessage(text='どこの天気ですか？', quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(
            event.reply_token,
            messages=messages
        )
    elif event.message.text in locations:
        all_data = get_day5_data(event.message.text)
        send_text_list = []
        for text in make_template(all_data):
            send_text_list.append(TextSendMessage(text=text))
        line_bot_api.reply_message(
            event.reply_token,
            send_text_list
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
