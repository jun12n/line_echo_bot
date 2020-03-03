import os
import sys
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from weather_forecast import get_day5_data

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
    # メッセージでもテキストの場合はオウム返しする
    if event.message.text == 'weather':
        all_data = get_day5_data()
        line_bot_api.reply_message(
            event.reply_token,
            make_text_template(all_data=all_data)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=event.message.text),
                TextSendMessage(text='Echo!')
            ]
        )


def make_text_template(all_data):
    text_list = []
    for i in all_data:
        if i['Weather'] == 'Rain':
            emoji = chr(0x1000AA)
        elif i['Weather'] == 'Clouds':
            emoji = chr(0x1000AC)
        else:
            emoji = chr(0x1000A9)
        text = """Date: {date}
天気は、{weather}{emoji}
温度は、{temperature}""".format(date=i['Datetime'], weather=i['Weather'], emoji=emoji, temperature=i['Temperature'])
        text_list.append(TextSendMessage(text=text))
    return text_list


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
