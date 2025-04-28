import aiohttp
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_binance_futures():
    url = 'https://fapi.binance.com/fapi/v1/ticker/24hr'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.json()
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при запросе к Binance: {e}")
        return []

async def get_bybit_futures():
    url = 'https://api.bybit.com/v2/public/tickers'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data.get('result', [])
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при запросе к Bybit: {e}")
        return []

async def get_binance_open_interest(symbol):
    url = f'https://fapi.binance.com/futures/data/openInterestHist?symbol={symbol}&period=5m&limit=2'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                if isinstance(data, list) and len(data) >= 2:
                    oi_old = float(data[0]['sumOpenInterest'])
                    oi_new = float(data[1]['sumOpenInterest'])
                    return round(((oi_new - oi_old) / oi_old) * 100, 2) if oi_old != 0 else 0
                return 0
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при запросе OI для {symbol}: {e}")
        return 0

def generate_tradingview_link(symbol):
    return f"https://www.tradingview.com/symbols/{symbol}/"

def generate_coinglass_link(symbol):
    return f"https://www.coinglass.com/future/{symbol.replace('USDT', '')}"
