# KittyBot

Telegram-бот, который присылает случайные фотографии котиков.
Картинки берутся из [The Cat API](https://thecatapi.com/), 
а если он недоступен - бот не теряется и присылает собачку из [The Dog API](https://thedogapi.com/).

## Возможности

| Команда / кнопка | Что делает |
| --- | --- |
| `/start` | Приветствует по имени, показывает клавиатуру и присылает первого котика |
| `/newcat` | Присылает нового случайного котика |
| `/random_digit` | Присылает случайную цифру от 0 до 9 |
| «Который час?» | Сообщает текущее время сервера |
| любой другой текст | Бот здоровается и подсказывает, что делать |


## Стек

- Python 3.9+
- pyTelegramBotAPI
- requests
- python-dotenv

## Быстрый старт

### 1. Получите токен бота

Напишите [@BotFather](https://t.me/BotFather) в Telegram, создайте бота командой `/newbot`
и скопируйте токен.

### 2. Клонируйте репозиторий и установите зависимости

```bash
git clone https://github.com/<ваш-логин>/kittybot.git
cd kittybot
python -m venv venv
```

Активируйте окружение.

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### 3. Настройте переменные окружения

Скопируйте `.env.example` в `.env` и впишите свой токен:

```env
TOKEN=123456789:AAAA-your-bot-token
CHAT_ID=123456789
```

### 4. Запустите бота

```bash
python kittybot.py
```

Откройте бота в Telegram и отправьте `/start`. Остановить бота — `Ctrl+C`.
