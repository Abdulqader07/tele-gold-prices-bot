import os
import json
import aiohttp
from datetime import datetime
from Config import Config
from Fetch import Price

class Bot:
    def __init__(self) -> None:
        self.conf = Config()
        self.price = Price()
        self.Data_File = self.conf.prices_file
        self.max_price = 0.0

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


    async def calculate(self, thershold = 0.3) -> None:
        await self.price.setPrice()
        
        previous = self.loadPrice()
        current = self.price.getPrice()

        if current:
            print('Gold price: $' + current, end='')
        
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
            return
        
        async with aiohttp.ClientSession() as session:
            for id in chatsList:
                payload = {"chat_id": id, "text": message, "parse_mode": "HTML"}

                try:
                    await session.post(url, json=payload)
                except Exception as e:
                    print(f'Error {e}')