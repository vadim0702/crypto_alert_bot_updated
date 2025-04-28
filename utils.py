import aiohttp

async def get_binance_futures():
    url = 'https://fapi.binance.com/fapi/v1/ticker/24hr'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def get_bybit_futures():
    url = 'https://api.bybit.com/v2/public/tickers'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data.get('result', [])

async def get_binance_open_interest(symbol):
    url = f'https://fapi.binance.com/futures/data/openInterestHist?symbol={symbol}&period=5m&limit=2'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if isinstance(data, list) and len(data) >= 2:
                oi_old = float(data[0]['sumOpenInterest'])
                oi_new = float(data[1]['sumOpenInterest'])
                return round(((oi_new - oi_old) / oi_old) * 100, 2)
            return 0

def generate_tradingview_link(symbol):
    return f"https://www.tradingview.com/symbols/{symbol}/"

def generate_coinglass_link(symbol):
    return f"https://www.coinglass.com/future/{symbol.replace('USDT', '')}"