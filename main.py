from flask import Flask, request
import openai
import telegram

import os
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))


app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    msg = data['message']['text']

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a seductive, sales-focused OF assistant."},
            {"role": "user", "content": msg}
        ]
    )

    reply = response['choices'][0]['message']['content']
    bot.send_message(chat_id=chat_id, text=reply)
    return "ok"

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)