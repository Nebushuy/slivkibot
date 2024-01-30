import requests
import logging
import time
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


logging.basicConfig(level=logging.INFO)
# Токен бота
TOKEN = '6933425414:AAEsJVwHhOCzfW3dhzI0swz7sI4yAmojfIg'

# Идентификатор чата, в который будем отправлять сообщения
CHAT_ID = ('-1002138041570')
#CHAT_ID = None
#Slivki ID -1002138041570
#My ID 196032615

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
#button = InlineKeyboardButton('Получить курсы', callback_data='get_rates')
#markup = InlineKeyboardMarkup().add(button)

# Функция для получения курсов валют и криптовалют
def get_rates():
    # Получаем курс доллара
    response = requests.get('https://openexchangerates.org/api/latest.json?app_id=edf031209d2241899c1d4da53330be08&base=USD&symbols=RUB')
    usd_rate = response.json()['rates']['RUB']

    # Получаем курс доллара ЦБ
    response = requests.get(
        'https://www.cbr-xml-daily.ru/daily_json.js')
    cbusd_rate_today = response.json()['Valute']['USD']['Value']
    cbusd_rate_yesterday = response.json()['Valute']['USD']['Previous']
    usd_din = cbusd_rate_today/cbusd_rate_yesterday - 1

    # Получаем курс Евро ЦБ
    response = requests.get(
        'https://www.cbr-xml-daily.ru/daily_json.js')
    cbeur_rate_today = response.json()['Valute']['EUR']['Value']
    cbeur_rate_yesterday = response.json()['Valute']['EUR']['Previous']
    eur_din = cbeur_rate_today / cbeur_rate_yesterday - 1

    # Получаем курс биткоина
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/usd.json')
    btc_rate = response.json()['bpi']['USD']['rate_float']

    # Получаем курс эфириума
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=USD')
    eth_rate = response.json()['ethereum']['usd']

    # Возвращаем курсы валют и криптовалют в виде строки
    return f'✌️🌱Ловим актуальные курсы:\n💵USD_CB: <b>{cbusd_rate_today:.2f}</b> RUB ({usd_din:.2%})\n💶EUR_CB: <b>{cbeur_rate_today:.2f}</b> RUB ({eur_din:.2%})\n🔥BTC: <b>{btc_rate:.2f}</b> USD\n🌐ETH: <b>{eth_rate:.2f}</b> USD'
#🚀USD: <b>{usd_rate:.2f}</b> RUB\n
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    await bot.send_message(chat_id=CHAT_ID, text="Привет, я бот, который отправляет 3 раза в день курсы валют и криптовалют!")

@dp.message_handler(commands=['getrate'])
async def start_command(message: types.Message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    #await message.reply("Привет✌️🌱! Чтобы получить курсы криптовалют, нажми на кнопку 'Получить курсы'", reply_markup=markup)
    await send_rates(message)

#@dp.callback_query_handler(lambda c: c.data == 'get_rates')
#async def process_callback_get_rates(callback_query: types.CallbackQuery):
#    await send_rates(callback_query.message)
#    await bot.answer_callback_query(callback_query.id)

# Функция для отправки сообщений
async def send_message():
    message = get_rates()
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')

async def send_rates(message: types.Message):
    await message.answer(get_rates(), parse_mode='HTML')

# Создаем задачу для отправки сообщений
async def send_messages():
    while True:
        # Получаем текущее время
        now = time.localtime()

        if now.tm_hour in [9, 14, 17]:
            await send_message()
        await asyncio.sleep(3600)


# Запускаем задачу для отправки сообщений
async def on_startup(dp):
    asyncio.create_task(send_messages())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
