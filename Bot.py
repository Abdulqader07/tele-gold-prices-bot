import os
import json
import aiohttp
from datetime import datetime
from Config import Config
from Fetch import Price
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


class Bot:
    def __init__(self) -> None:
        self.conf = Config()
        self.price = Price()
        self.Data_File = self.conf.prices_file
        self.max_price = 0.0

    async def startCommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if self.conf.addChat(chat_id):
            await update.message.reply_text("Hi there, welcome to gold prices alerts")

        else:
            await update.message.reply_text("You're already subcribed.")

    async def stopCommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        if self.conf.removeChat(chat_id):
            await update.message.reply_text("You're unsubcribed from this bot.")
        
        else:
            await update.message.reply_text("You're not a subscriber.")
    
    async def priceCommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        current_price = self.price.getPrice()
        await update.message.reply_text(f"Current gold price: ${current_price}")

    async def run(self):
        app = Application.builder().token(self.conf.BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("stop", self.stop_command))
        app.add_handler(CommandHandler("price", self.price_command))
        
        print("Bot is listening for commands...")
        await app.run_polling()


    def loadPrice(self):
        if os.path.exists(self.Data_File):
            try:
                with open(self.Data_File, 'r') as rf:
                    data = json.load(rf)

                    return data.get('price')
                
            except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading price: {e}")
                    
                    return None
        
        return None
    

    def savePrice(self, price) -> None:
        now = datetime.now()
        
        data = {
            'price': price,
            'time': now.strftime("%Y-%m-%d %H:%M:%S")

        }

        with open(self.Data_File, 'w') as wf:
            json.dump(data, wf)


    async def calculate(self, thershold = 0.0) -> None:
        import time
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] calculate() was called")
        
        await self.price.setPrice()
        
        previous = self.loadPrice()
        current = self.price.getPrice()

        if current:
            print('Gold price: $' + current + '\n', end='', flush=True)
        
        if previous is not None and current:
            try:
                diff = ((float(current) - float(previous)) / float(previous)) * 100

                print(f' With {diff:.2f}% Change')

                if abs(diff) >= thershold:
                    msg = f"Gold price changed by {diff:.2f}% New price: ${current}"

                    print(msg)
                    await self.sendTelegramNotifications(message=msg)

                self.savePrice(current)
        
            except ZeroDivisionError:
                self.savePrice(current)
        

    async def sendTelegramNotifications(self, message):
        url = f'https://api.telegram.org/bot{self.conf.BOT_TOKEN}/sendMessage'
        chat_ids = self.conf.chats_file

        chatsList = self.conf.getChats()
        
        if not chat_ids:
            return 'No subs yet'
        
        async with aiohttp.ClientSession() as session:
            for id in chatsList:
                payload = {"chat_id": id, "text": message, "parse_mode": "HTML"}

                try:
                    await session.post(url, json=payload)
                except Exception as e:
                    print(f'Error {e}')