import asyncio
from aiogram import Bot, Dispatcher, types
from config import TELEGRAM_TOKEN
from utils import get_binance_futures, get_bybit_futures, get_binance_open_interest, generate_tradingview_link, generate_coinglass_link
from database import init_db, save_settings, get_settings

bot = Bot(token=TELEGRAM_TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет! 👋\nЯ помогу тебе следить за крипторынком!")

async def send_crypto_alert(chat_id, symbol, price, volume_change, oi_change):
    tradingview_link = f"https://www.tradingview.com/symbols/{symbol}/"
    coinglass_link = f"https://www.coinglass.com/future/{symbol.replace('USDT', '')}"

    text = (
        f"🚀 <b>{symbol}</b>\n\n"
        f"💵 <b>Цена:</b> {price}$\n"
        f"📈 <b>Рост объема:</b> +{volume_change}%\n"
        f"📊 <b>Рост OI:</b> +{oi_change}%\n\n"
        f"🔗 <a href='{tradingview_link}'>Открыть график TradingView</a>\n"
        f"🔗 <a href='{coinglass_link}'>Посмотреть на Coinglass</a>"
    )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="📊 TradingView", url=tradingview_link),
            types.InlineKeyboardButton(text="📈 Coinglass", url=coinglass_link),
        ]
    ])

    await bot.send_message(chat_id, text=text, reply_markup=keyboard)

async def main_loop():
    init_db()
    while True:
        binance_data = await get_binance_futures()
        # Тут пример обработки монет и вызова send_crypto_alert
        # await send_crypto_alert(chat_id, symbol, price, volume_change, oi_change)
        await asyncio.sleep(300)  # Проверять каждые 5 минут

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())