# https://github.com/line/line-bot-sdk-python->Synopsis
import os                                # 在 Render 使用環境變數
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage    
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN")) # 在 Render 上設定這兩個環境變數
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))                         # 在 Render 上設定這兩個環境變數


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']   # 專屬Line

    # get request body as text
    body = request.get_data(as_text=True)             # 取出
    app.logger.info("Request body: " + body)          # 可用print(body)輸出

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent) # TextMessageContent接收,TextMessage發送
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,         # 只能回一次，最好30秒內回
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) # 加入 port（配合Render 需要）
    app.run(host="0.0.0.0", port=port)       # 加入 port（配合Render 需要）
    # app.run()      # 預設5000 


