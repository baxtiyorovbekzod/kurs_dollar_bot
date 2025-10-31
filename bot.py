import os
import requests
from flask import Flask, request

TOKEN = os.getenv("TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return "no data"

    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '')

    if text == '/start':
        send_message(chat_id, "Salom, botga xush kelibsiz!")
    elif text.isdigit():
        summa = int(text)
        send_message(chat_id, f"{summa:,} so'm kiritdingiz!")
    else:
        send_message(chat_id, "Son yuboring!")

    return "ok"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    requests.post(url, json={'chat_id': chat_id, 'text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))