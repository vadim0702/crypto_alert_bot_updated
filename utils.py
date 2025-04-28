def generate_tradingview_link(symbol):
    return f"https://www.tradingview.com/symbols/{symbol}/"

def generate_coinglass_link(symbol):
    return f"https://www.coinglass.com/future/{symbol.replace('USDT', '')}"
