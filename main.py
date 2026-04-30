import asyncio
from Bot import Bot
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot running")

def run_health_server():
    HTTPServer(('0.0.0.0', 8080), HealthHandler).serve_forever()

async def main():
    bot = Bot()

    threading.Thread(target=run_health_server, daemon=True).start()
    
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