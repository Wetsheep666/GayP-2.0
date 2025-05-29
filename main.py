from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage  # 👈 這行要加上
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from linebot_handler import handle_event

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 👇 這邊綁定 Line 訊息事件
@handler.add(MessageEvent, message=TextMessage)
def message_handler(event):
    handle_event(event, line_bot_api)

if __name__ == "__main__":
    app.run()
