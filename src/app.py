import asyncio
import logging

from aiohttp import web
from aiojobs.aiohttp import setup, get_scheduler
from datetime import date, timedelta, datetime

from utils import init_db, get_prices_db, update_prices_db

logging.basicConfig(level=logging.INFO)

async def prices(request):
    ticker = request.match_info.get('ticker')
    db = request.config_dict["DB"]
    prices = await get_prices_db(db, ticker)
    if len(prices) and (date.today()- timedelta(days=1)).isoformat() in prices.keys():
        return web.json_response(prices)
    else:
        scheduler = get_scheduler(request)
        await scheduler.spawn(update_prices_db(scheduler, db, ticker))
        return web.json_response('Prices are updating. Try later')

def main():
    app = web.Application()
    app.router.add_route('GET', '/prices/{ticker}', prices)
    app.cleanup_ctx.append(init_db)
    setup(app)
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
