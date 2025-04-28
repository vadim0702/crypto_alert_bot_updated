import requests

async def get_binance_futures():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    return response.json()

def generate_tradingview_link(symbol):
    return f"https://www.tradingview.com/symbols/{symbol}/"

def generate_coinglass_link(symbol):
    return f"https://www.coinglass.com/future/{symbol.replace('USDT', '')}"
