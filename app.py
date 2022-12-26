import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", 
            "chatGPT" , "chatGPTresponse" , "chatGPTexit" ,
            "search"  , "searchresult"    , "searchexit",
            "help" ],
    transitions=[
        #chatGPT state
        {
            "trigger"    : "advance",
            "source"     : "user",
            "dest"       : "chatGPT",
            "conditions" : "is_going_to_chatGPT",
        },
        {
            "trigger"    : "advance",
            "source"     : "chatGPT",
            "dest"       : "chatGPTexit",
            "conditions" : "is_going_to_chatGPTexit",
        },
        {
            "trigger"    : "advance",
            "source"     : "chatGPT",
            "dest"       : "chatGPTresponse",
            "conditions" : "is_going_to_chatGPTresponse",
        },
        {
            "trigger"    : "go_back_chatGPT", 
            "source"     : "chatGPTresponse", 
            "dest"       : "chatGPT"
        },
        #google search state
        {
            "trigger"    : "advance",
            "source"     : "user",
            "dest"       : "search",
            "conditions" : "is_going_to_search",
        },
        {
            "trigger"    : "advance",
            "source"     : "search",
            "dest"       : "searchexit",
            "conditions" : "is_going_to_searchexit",
        },
        {
            "trigger"    : "advance",
            "source"     : "search",
            "dest"       : "searchresult",
            "conditions" : "is_going_to_searchresult",
        },
        {
            "trigger"    : "go_back_search", 
            "source"     : "searchresult", 
            "dest"       : "search"
        },
        #help state
        {
            "trigger"    : "advance",
            "source"     : ["user" , "chatGPT" , "search"],
            "dest"       : "help",
            "conditions" : "is_going_to_help", 
        },
        #go back user
        {
            "trigger"    : "go_back", 
            "source"     : ["chatGPTexit","searchexit","help"],
            "dest"       : "user"
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        print(event.message.text)
        response = machine.advance(event)
        
        if response == False:
            send_text_message(event.reply_token, "很抱歉 沒有這項服務功能\n\n輸入chat 與chatGPT聊天\n輸入search 可以爬蟲所需圖片\n輸入help 查看所有指令")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    print("fdfdf")
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
