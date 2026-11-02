import os

import requests
from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv(override=True)

bot = TeleBot(token=os.getenv('TOKEN'))
chat_id = os.getenv('CHAT_ID')

# Адрес API сохраним в константе:
URL = 'https://api.thecatapi.com/v1/images/search'

response = requests.get(URL, timeout=10).json()
random_cat_url = response[0].get('url')
bot.send_photo(chat_id, random_cat_url)
