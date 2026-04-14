import aiohttp
from bs4 import BeautifulSoup as bs

async def fetchPrices() -> str:
	url = 'https://www.investing.com/currencies/xau-usd'

	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0'
	}

	async with aiohttp.ClientSession() as session:
		try:
			async with session.get(url, headers=headers) as response:
				html = await response.text()
				soup = bs(html, 'html.parser')

				price = soup.find('div', class_='text-5xl/9')

				floatPrice = price.string.replace(',', '')

				return floatPrice

		except Exception as e:
			return f"Something happened while fetching price: {e}"