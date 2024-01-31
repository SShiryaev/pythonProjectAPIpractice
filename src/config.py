import os

API_KEY: str = os.getenv('EXCHANGE_RATE_API_KEY')
TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
CURRENCY_RATES_FILE = 'currency_rate.json'
