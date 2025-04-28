import asyncio
import sqlite3
import logging
from aiogram import Bot, Dispatcher, types, DefaultBotProperties
from aiogram.filters import Command
from config import TELEGRAM_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from utils import get_binance_futures, get_bybit_futures, get_binance_open_interest, generate_tradingview_link, generate_coinglass_link
    from database import init_db, save_settings, get_settings
except ImportError as e:
    logger.error(f"Ошибка при импорте модулей: {e}")
    raise

# Инициализация бота с использованием DefaultBotProperties
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer("Привет! 👋\nЯ помогу тебе следить за крипторынком!\nИспользуй /settings для настройки уведомлений.")

# Обработчик команды /settings
@dp.message(Command(commands=["settings"]))
async def cmd_settings(message: types.Message):
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Используйте: /settings <volume_threshold> <oi_threshold>\nПример: /settings 50 5")
        return
    try:
        volume_threshold = float(args[1])
        oi_threshold = float(args[2])
        save_settings(message.chat.id, {"volume_threshold": volume_threshold, "oi_threshold": oi_threshold})
        await message.answer(f"Настройки сохранены: объем {volume_threshold}%, OI {oi_threshold}%")
    except ValueError:
        await message.answer("Укажите числовые значения для порогов.")

async def send_crypto_alert(chat_id, symbol, price, volume_change, oi_change):
    tradingview_link = generate_tradingview_link(symbol)
    coinglass_link = generate_coinglass_link(symbol)

    text = (
        f"🚀 <b>{symbol}</b>\n\n"
        f"💵 <b>Цена:</b> {price}$\n"
        f"📈 <b>Рост объема:</b> +{volume_change}%\n"
        f"📊 <b>Рост OI:</b> +{oi_change}%\n\n"
        f"🔗 <a href='{tradingview_link}'>TradingView</a> | <a href='{coinglass_link}'>Coinglass</a>"
    )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="📊 TradingView", url=tradingview_link),
            types.InlineKeyboardButton(text="📈 Coinglass", url=coinglass_link),
        ]
    ])

    try:
        await bot.send_message(chat_id, text=text, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в чат {chat_id}: {e}")

async def main_loop():
    init_db()
    while True:
        try:
            # Получаем данные с Binance
            binance_data = await get_binance_futures()
            if not binance_data:
                logger.warning("Не удалось получить данные с Binance")
                await asyncio.sleep(300)
                continue

            # Обрабатываем каждого пользователя
            conn = sqlite3.connect('settings.db')
            cursor = conn.cursor()
            cursor.execute('SELECT chat_id FROM user_settings')
            chat_ids = [row[0] for row in cursor.fetchall()]
            conn.close()

            for chat_id in chat_ids:
                settings = get_settings(chat_id)
                volume_threshold = settings.get("volume_threshold", 50)
                oi_threshold = settings.get("oi_threshold", 5)

                for item in binance_data:
                    symbol = item.get("symbol", "")
                    if not symbol.endswith("USDT"):
                        continue

                    volume_change = float(item.get("volume", 0))
                    price = float(item.get("lastPrice", 0))
                    oi_change = await get_binance_open_interest(symbol)

                    if volume_change >= volume_threshold and oi_change >= oi_threshold:
                        await send_crypto_alert(chat_id, symbol, price, volume_change, oi_change)

            await asyncio.sleep(300)  # Пауза 5 минут
        except Exception as e:
            logger.error(f"Ошибка в main_loop: {e}")
            await asyncio.sleep(60)  # Пауза 1 минута при ошибке

async def main():
    try:
        # Запускаем main_loop в фоновом режиме
        asyncio.create_task(main_loop())
        # Запускаем polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка в главном цикле бота: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise
