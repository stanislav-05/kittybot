import logging
import os
import random
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv(override=True)

TOKEN = os.getenv('TOKEN')

CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'
# Запасной API: если котики недоступны, пришлем собачку.
DOG_API_URL = 'https://api.thedogapi.com/v1/images/search'
REQUEST_TIMEOUT = 10

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

if not TOKEN:
    logger.critical(
        'Не найден TOKEN. Создайте файл .env по образцу .env.example.'
    )
    sys.exit(1)

bot = TeleBot(token=TOKEN)


def fetch_image_url(api_url):
    """Запрашивает API и возвращает ссылку на случайную картинку."""

    response = requests.get(api_url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()[0]['url']


def get_new_image():
    """Возвращает ссылку на котика, а при сбое - на собачку."""

    try:
        return fetch_image_url(CAT_API_URL)
    except (requests.RequestException, ValueError, LookupError) as error:
        logger.error(f'Ошибка при запросе к основному API: {error}')
        return fetch_image_url(DOG_API_URL)


def send_image(chat_id):
    """Отправляет картинку в чат или сообщает об ошибке."""

    try:
        bot.send_photo(chat_id, get_new_image())
    except Exception as error:
        logger.error(f'Не удалось отправить картинку: {error}')
        bot.send_message(chat_id, 'Котики сейчас спят 😿 Попробуйте позже.')


def build_keyboard():
    """Создаёт клавиатуру с кнопками бота."""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton('/newcat'),
        types.KeyboardButton('/random_digit'),
    )
    keyboard.row(types.KeyboardButton('Который час?'))
    return keyboard


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = chat.first_name or 'друг'
    bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что вы включили меня, {name}!',
        reply_markup=build_keyboard(),
    )
    send_image(chat.id)


@bot.message_handler(commands=['newcat'])
def new_cat(message):
    send_image(message.chat.id)


@bot.message_handler(commands=['random_digit'])
def random_digit(message):
    bot.send_message(message.chat.id, f'Ваша цифра: {random.randint(0, 9)}')


@bot.message_handler(func=lambda message: message.text == 'Который час?')
def what_time(message):
    now = datetime.now().strftime('%H:%M')
    bot.send_message(message.chat.id, f'Сейчас {now} (по времени сервера).')


@bot.message_handler(content_types=['text'])
def say_hi(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Привет, я KittyBot! Нажмите /newcat, чтобы получить котика.',
    )


def main():
    logger.info('KittyBot запущен')
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
