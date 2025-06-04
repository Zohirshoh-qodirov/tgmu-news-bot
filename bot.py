from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем .env

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Получаем токен из переменной окружения

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который публикует новости!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
