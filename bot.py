import os
import json
import asyncio
from datetime import datetime
from fetch_pric3 import fetchPrices
from main import sendTelegramBotNotifications

Data_File = 'gold_prices.json'

def loadPrice():
    if os.path.exists(Data_File):
        try:

            with open(Data_File, 'r') as rf:
                data = json.load(rf)

                return data.get('previous_price')
            
        except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading price: {e}")
                
                return None
    
    return None

def savePrice(price) -> None:
    data = {
        'previous_price': price,
        'time': str(datetime.now())

    }
    with open(Data_File, 'w') as wf:
        json.dump(data, wf)

async def fnBot() -> None:
    previous = loadPrice()

    while True:
        current = await fetchPrices()

        if current:
            print(current)

            if previous is not None:
                diff = abs((float(current) - float(previous)) / float(previous)) * 100

                if diff >= 1:
                    msg = (f"Gold price changed in more 1%: New price ${diff}")
                    print(msg)

                    await sendTelegramBotNotifications(msg)

            savePrice(current)
            previous = current

            await asyncio.sleep(120)