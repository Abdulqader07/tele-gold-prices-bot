import os
from flask import Flask
import threading
import time
import asyncio
import requests
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
    

def callBot():
    time.sleep(10)
    
    url = f'http://localhost:{os.environ.get('PORT', 8080)}/run-bot'

    while True:
        requests.get(url)
        time.sleep(3600)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    threading.Thread(target=callBot, daemon=True).start()

    app.run(host='0.0.0.0', port=port)

'''
async def main():

    # Start Flask in background
    threading.Thread(target=run_flask, daemon=True).start()
    await asyncio.sleep(3)

    print('To stop the bot press Ctrl + C')
    print('Hello I am the bot here to send you alerts about gold prices')

    try:

        await bot.calculate()

        iteration = 0

        while True:
            logger.info(f'Waiting 3600 seconds until next iteration (iteration {iteration})...')
            await asyncio.sleep(3600)

            logger.info(f'Running calculation iteration {iteration + 1}...')

            try:
                await bot.calculate()
                logger.info(f'Calculation iteration {iteration + 1} completed successfully')
            
            except Exception as e:
                logger.error(f'Error in calculation iteration {iteration + 1}: {e}', exc_info=True)
           
            iteration += 1

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
        pass'''