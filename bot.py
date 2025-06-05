import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Получаем токен из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Обработка команды /start
@dp.message(Command(commands=["start", "hello"]))
async def start_handler(message: Message):
    await message.answer("👋 Привет! Я бот TGMU. Жду твоих команд!")

# Обработка команды /help
@dp.message(Command(commands=["help"]))
async def help_handler(message: Message):
    await message.answer("🛠 Доступные команды:\n/start - начать\n/help - помощь")

# Эхо-обработчик всех остальных сообщений
@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"Вы сказали: {message.text}")

# Основная функция запуска бота
async def run_bot():
    await dp.start_polling(bot)
