from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # например '@my_channel'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def post_news():
    url = 'https://example.com/news'  # <- Поставь URL сайта с новостями
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('article')  # или другой тег, который подходит для сайта
        for article in articles[:5]:  # последние 5 новостей
            title = article.find('h2').text.strip()  # пример
            link = article.find('a')['href']
            message = f"{title}\nПодробнее: {link}"

            await bot.send_message(CHANNEL_ID, message)

    except Exception as e:
        print(f"Ошибка при парсинге или отправке: {e}")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который публикует новости с сайта в канал!")

@dp.message_handler(commands=['post'])
async def manual_post(message: types.Message):
    await message.reply("Начинаю публикацию новостей...")
    await post_news()
    await message.reply("Публикация завершена!")

if __name__ == '__main__':
    # Запускаем бота и параллельно можно запускать периодическую публикацию
    async def scheduler():
        while True:
            await post_news()
            await asyncio.sleep(60 * 60)  # раз в час

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dp, skip_updates=True)
