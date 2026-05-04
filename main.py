import os
from flask import Flask
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
    
def run_telegram_bot():
    """Run the telegram bot in a separate event loop"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(bot.run())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    
    # Start Telegram bot in background thread
    telegram_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    telegram_thread.start()


    app.run(host='0.0.0.0', port=port)