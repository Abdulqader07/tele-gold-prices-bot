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
    
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data and 'message' in data:
        user = data['message']['from']
        
        print(f"NEW SUBSCRIBER: {user['id']} - @{user.get('username', 'no username')} - {user.get('first_name', '')}")
        
        with open('subscribers.txt', 'a') as f:
            f.write(f"{user['id']},{user.get('username', '')},{user.get('first_name', '')}\n")
    
    return 'ok', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    
    app.run(host='0.0.0.0', port=port)