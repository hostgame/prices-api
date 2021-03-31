# Stock prices API

Start:
```
docker-compose up
```

Get prices history:
```
curl localhost:8000/prices/GOOG
```

Built with aiohttp and sqlite3. Price history parsed from Yahoo Finance
