import pytest
from utils import get_binance_futures

@pytest.mark.asyncio
async def test_get_binance_futures():
    data = await get_binance_futures()
    assert isinstance(data, list), "Data should be a list"
