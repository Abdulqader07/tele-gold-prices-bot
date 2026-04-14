import os
import json
import asyncio
import aiohttp
from datetime import datetime
from fetch_pric3 import fetchPrices
from config import BOT_TOKEN

Data_File = 'gold_prices.json'
Chat_Ids_File = 'chat.json'

def loadPrice():
    if os.path.exists(Data_File):
        with open(Data_File, 'r') as rf:
            data = json.load(rf)
            return data.get('previous_price')
    return None

def savePrice(price):
    data = {
        'previous_price': price,
        'time': str(datetime.now())
    }
    with open(Data_File, 'w') as wf:
        json.dump(data, wf)

def loadChats():
    if os.path.exists(Chat_Ids_File):
        with open(Chat_Ids_File, 'r') as rf:
            data = json.load(rf)
            return data.get('chat_id', [])
    return []

async def sendTelegramNotifications(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    chat_ids = loadChats()
    
    if not chat_ids:
        return
    
    async with aiohttp.ClientSession() as session:
        for cid in chat_ids:
            payload = {"chat_id": cid, "text": message, "parse_mode": "HTML"}
            try:
                await session.post(url, json=payload)
            except Exception as e:
                print(f"Error: {e}")

async def bot():
    previous = loadPrice()
    
    while True:
        current = await fetchPrices()
        
        if current:
            print(current)
            
            if previous is not None:
                diff = abs((float(current) - float(previous)) / float(previous)) * 100
                
                if diff >= 0.5:
                    message = f"Gold price changed by {diff:.2f}% New price: ${current}"
                    print(message)
                    await sendTelegramNotifications(message)
            
            savePrice(current)
            previous = current
            await asyncio.sleep(120)

if __name__ == '__main__':
    print('Starting gold prices monitor')
    print('Press Ctrl + C to stop')
    
    try:
        asyncio.run(bot())
    except KeyboardInterrupt:
        print('\nBot stopped')