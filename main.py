import asyncio
from Bot import Bot

async def main():
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