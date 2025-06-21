from flask import Flask, request
from openai import OpenAI
import telegram
import os

# Load API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

client = OpenAI(api_key=openai_api_key)
bot = telegram.Bot(token=telegram_bot_token)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if 'message' not in data:
        return "No message", 200

    chat_id = data['message']['chat']['id']
    msg = data['message']['text']

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a seductive, sales-focused OF assistant."},
            {"role": "user", "content": msg}
        ]
    )

    reply = response.choices[0].message.content
    bot.send_message(chat_id=chat_id, text=reply)

    return "ok", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
