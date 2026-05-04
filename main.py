import os
import requests
from flask import Flask, request, Response
import threading
import asyncio
from Bot import Bot

# Flask app for Render health checks
app = Flask(__name__)

bot = Bot()

@app.route('/')
@app.route('/health')
def health():
    return "Bot running\n", 200


@app.route('/run-bot')
def run_bot():
    try:
        asyncio.run(bot.calculate())
        return 'Bot ran successfully\n'
    
    except Exception as e:
        return f'Error {e}\n', 500

@app.route(f'/webhook/{bot.conf.BOT_TOKEN}', methods=['POST'])
def webhook():
    try:
        update_data = request.get_json()

        if 'message' in update_data:
            message = update_data['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')

            thread = threading.Thread(target=process_command_background, args=(chat_id, text))
            thread.start()

        return Response('ok', status=200)
    
    except Exception as e:
        print(f"Webhook error: {e}")
        
        return Response('error', status=500)

def process_command_background(chat_id, command):
    try:
        asyncio.run(bot.process_command(chat_id, command))

    except Exception as e:
        print(f"Command error: {e}")

def set_webhook():
    webhook_url = f"https://tele-gold-prices-bot.onrender.com/webhook/{bot.conf.BOT_TOKEN}"
    url = f"https://api.telegram.org/bot{bot.conf.BOT_TOKEN}/setWebhook?url={webhook_url}"

    try:
        response = requests.get(url)
        print(f"Webhook set response: {response.json()}")

    except Exception as e:
        print(f"Failed to set webhook: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    
    set_webhook()

    app.run(host='0.0.0.0', port=port)