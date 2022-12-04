import os
import re
import time
from threading import Thread
from slack_bolt import App
from revChatGPT.revChatGPT import Chatbot

ChatGPTConfig = {
        "Authorization": "<Your Bearer Token Here>", # This is optional
        "session_token": os.environ['CHATGPT_SESSION_TOKEN']
    }

app = App()
chatbot = Chatbot(ChatGPTConfig, conversation_id=None)

# Listen for an event from the Events API
@app.event("app_mention")
def event_test(event, say):
    prompt = re.sub('(?:\s)<@[^, ]*|(?:^)<@[^, ]*', '', event['text'])
    response = chatbot.get_chat_response(prompt)
    user = event['user']
    user = f"<@{user}> you asked:"
    asked = ['>',prompt]
    asked = "".join(asked)
    send = [user,asked,response["message"]]
    send = "\n".join(send)
    say(send)

def chatgpt_refresh():
    while True:
        chatbot.refresh_session()
        time.sleep(60)

if __name__ == "__main__":
    thread = Thread(target=chatgpt_refresh)
    thread.start()
    app.start(4000)  # POST http://localhost:4000/slack/events
    