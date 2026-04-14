import json
import asyncio
from datetime import datetime
from fetch_pric3 import fetchPrices

file = 'gold_prices.json'

async def main():
    price = await fetchPrices()

    with open(file, 'w+') as wf:
        json.dump({"previous_price": price, "time": str(datetime.now())}, wf)

        data = json.load(wf)
        print(data.get('previous_price'))


if __name__ == '__main__':
    asyncio.run(main())