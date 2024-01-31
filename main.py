from datetime import datetime

import telebot
from telebot import types

from src.config import TOKEN, CURRENCY_RATES_FILE
from src.utils import get_currency_rate, save_to_json, get_read_json

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    После нажатия на start инициализирует интерфейс - кнопки с валютами.
    Для выбранной валюты будет представлен ее курс к рублю.
    """

    currency_button = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_usd = types.InlineKeyboardButton("Доллар (USD)", callback_data='USD')
    button_eur = types.InlineKeyboardButton("Евро (EUR)", callback_data='EUR')
    button_jpy = types.InlineKeyboardButton("Йена (JPY)", callback_data='JPY')
    button_kzt = types.InlineKeyboardButton("Тенге (KZT)", callback_data='KZT')
    button_lkr = types.InlineKeyboardButton("Шри-ланкийская рупия (LKR)", callback_data='LKR')
    button_vnd = types.InlineKeyboardButton("Вьетнамский донг (VND)", callback_data='VND')
    currency_button.add(button_usd, button_eur, button_jpy, button_kzt, button_lkr, button_vnd)
    bot.send_message(message.chat.id, 'Нажми кнопку с названием валюты чтобы узнать текущий курс к рублю',
                     reply_markup=currency_button)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Отправляет пользователю курс рубля к выбранной валюте"""

    if call.data == "USD":
        currency = "USD"
    elif call.data == "EUR":
        currency = "EUR"
    elif call.data == "LKR":
        currency = "LKR"
    elif call.data == "JPY":
        currency = "JPY"
    elif call.data == "KZT":
        currency = "KZT"
    else:
        currency = "VND"

    rate_rub = get_currency_rate(currency)
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
    data = {'currency': currency, 'rate': rate_rub, 'timestamp': timestamp}
    save_to_json(data, CURRENCY_RATES_FILE)
    read_json = get_read_json(CURRENCY_RATES_FILE)
    rate: float = read_json[-1].get("rate")
    bot.send_message(call.message.chat.id, f"Курс рубля к {currency} на {timestamp} составляет {rate}.")


bot.polling(non_stop=True)
