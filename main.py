import os
from flask import Flask
import threading
import logging
import asyncio
from Bot import Bot

# Flask app for Render health checks
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
@app.route('/health')
def health():
    return "Bot running", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    
    print(f"Starting Flask on port {port}")
    print(f"Health check available at http://0.0.0.0:{port}/health")
    
    app.run(host='0.0.0.0', port=port)

async def main():

    # Start Flask in background
    threading.Thread(target=run_flask, daemon=True).start()
    await asyncio.sleep(3)
    
    logger.info('Starting the bot')
    bot = Bot()

    print('To stop the bot press Ctrl + C')
    print('Hello I am the bot here to send you alerts about gold prices')

    try:

         # First calculation
        logger.info('Running initial calculation...')
        await bot.calculate()
        logger.info('Initial calculation completed successfully')

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
        pass