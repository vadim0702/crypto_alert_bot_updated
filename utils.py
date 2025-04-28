import aiohttp

async def get_binance_futures():
    url = 'https://fapi.binance.com/fapi/v1/ticker/24hr'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise Exception(f"Error: {resp.status}")
    except Exception as e:
        print(f"Failed to fetch Binance futures data: {e}")
        return []

async def get_bybit_futures():
    url = 'https://api.bybit.com/v2/public/tickers'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('result', [])
                else:
                    raise Exception(f"Error: {resp.status}")
    except Exception as e:
        print(f"Failed to fetch Bybit futures data: {e}")
        return []
