import time
from aiohttp_requests import requests

class YahooParser(object):
	url = "https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start}&period2={end}&interval=1d&events=history&includeAdjustedClose=true"

	def __init__(self, ticker):
		self.ticker = ticker
		self.data = []

	async def run(self):
		r = await requests.get(self.url.format(ticker=self.ticker, start=0, end=int(time.time())))
		history = await r.text()
		for line in history.splitlines()[1:]:
			# date, open_price, high_price, low_price, close_price, adj_close_price, volume
			self.data.append(line.split(','))

if __name__ == '__main__':
	p = YahooParser("PD")
	p.run()
	print(p.data)