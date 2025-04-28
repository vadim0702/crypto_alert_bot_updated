# Crypto Alert Telegram Bot (красивая версия)

Этот бот отслеживает рост объема и открытого интереса монет на Binance и Bybit (USDT Futures) и отправляет КРАСИВО ОФОРМЛЕННЫЕ уведомления в Telegram.

## Как запустить

1. Установите зависимости:

```
pip install -r requirements.txt
```

2. Создайте файл `config.py` и вставьте туда ваш `TELEGRAM_TOKEN`.

3. Запустите бота:

```
python bot.py
```

## Для деплоя на Render:

- Добавить Procfile.
- Выставить переменную окружения `TELEGRAM_TOKEN`.
- Использовать SQLite или подключить внешний DB.