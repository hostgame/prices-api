import aiosqlite
from yahoo_parser import YahooParser

def chunks(data, rows):
    for i in range(0, len(data), rows):
        yield data[i:i+rows]

async def init_db(app):
    db = await aiosqlite.connect("/data/app.db")
    db.row_factory = aiosqlite.Row
    app["DB"] = db

    try:
        await db.execute("""CREATE TABLE IF NOT EXISTS prices (
            ticker TEXT, 
            date TEXT, 
            open NUMERIC, 
            high NUMERIC, 
            low NUMERIC, 
            close NUMERIC, 
            adjustment_close NUMERIC, 
            volume NUMERIC, 
            UNIQUE(ticker, date) ON CONFLICT REPLACE)""")
    except Exception as e:
        pass

    yield
    await db.close()

async def update_prices_db(scheduler, db, ticker):
    yp = YahooParser(ticker)
    await yp.run()

    divData = chunks(yp.data, rows=10000)

    for chunk in divData:
        await db.execute('BEGIN')
        for date, open_price, close_price, high, low, adjustment_close, volume in chunk:
            await db.execute('INSERT OR IGNORE INTO prices \
                (date, ticker, open, close, high, low, adjustment_close, volume) \
                VALUES (?,?,?,?,?,?,?,?)', 
                (date, ticker, open_price, close_price, high, low, adjustment_close, volume)
            )
        await db.execute('END')

async def get_prices_db(db, ticker):
    cursor = await db.execute("SELECT * FROM prices WHERE ticker = ? \
        ORDER BY date(date) DESC", [ticker])
    prices = await cursor.fetchall()
    return {entity['date']: dict(entity) for entity in prices}