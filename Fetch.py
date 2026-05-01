import aiohttp
from bs4 import BeautifulSoup as bs

class Price:
    def __init__(self) -> None:
        self.price = ''

        self.headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0'
	    }

    async def setPrice(self) -> None:
        self.price = await self.fetchPriceAPI()

    def getPrice(self) -> str:
        return self.price

    async def fetchPrice(self) -> str:
        url = 'https://www.investing.com/currencies/xau-usd'

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    html = await response.text()
                    soup = bs(html, 'html.parser')

                    price = soup.find('div', class_='text-5xl/9')

                    floatPrice = price.string.replace(',', '')

                    return floatPrice
            
            except Exception as e:
                return f"Something happened while fetching price: {e}"
            
    async def fetchPriceAPI(self) -> str:
        url = 'https://api.gold-api.com/price/XAU'

        async with aiohttp.ClientSession() as session:

            try:
                async with session.get(url, headers=self.headers) as response:
                    data = await response.json()

                    return f"{data['price']:.2f}"
            
            except Exception as e:
                print(f'Error {e}')

                return None