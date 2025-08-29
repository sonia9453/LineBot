# https://github.com/line/line-bot-sdk-python->Synopsis

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

configuration = Configuration(access_token='3uCp6ADwnZ0RB+SiooROBOOmpWb32rip0H02Osm2nSAOYxdg1ig1ivyLRhWJE1pVRyZeetSlcNZIxrLkLFk37Nv3xwhaRemRhTvoDjVBmd0rGRb4PiDXOvy/6LBeiRkkIAoyK95lb1Wvxj1gc7+EkAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ec4b665efa1e09b9d3a7b3bda95ac34e')


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

    app.run()      # 預設5000
