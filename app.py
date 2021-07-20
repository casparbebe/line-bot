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

app = Flask(__name__)

line_bot_api = LineBotApi('CiHhBGKLL9doyaxeOSn1wKSUPt/mrzTvPF2Fd3c7i8ovv0ZZb+q4VJZ083RhJf1JmYa4UEP/aRhiYUQMKjTUTSYjeupmx0Ecjf9zDQjYvnh7o7UToiMmcOu8l+pcyMPwRGZo+ZxMg16KnFCjmsKx4gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d15741984150d21d5a3720544eac2efe')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()