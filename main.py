import os
from flask import Flask
import threading
import asyncio
from Bot import Bot

# Flask app for Render health checks
app = Flask(__name__)

@app.route('/')
@app.route('/health')
def health():
    return "Bot running", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    
    print(f"Starting Flask on port {port}")
    
    app.run(host='0.0.0.0', port=8080)

async def main():

    # Start Flask in background
    threading.Thread(target=run_flask, daemon=True).start()

    asyncio.sleep(3)
    
    print('Starting the bot')
    bot = Bot()

    print('To stop the bot press Ctrl + C')
    print('Hello I am the bot here to send you alerts about gold prices')

    try:

        await bot.calculate()

        while True:
            await asyncio.sleep(3600)
            await bot.calculate()

    except KeyboardInterrupt:
        print('\nBot stopped by developer')

    except asyncio.CancelledError:
        print('\nBot stopped')

    except Exception as e:
        print(f'\nError {e}')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass