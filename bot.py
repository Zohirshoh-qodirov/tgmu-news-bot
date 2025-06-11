import asyncio
import logging
import os
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

sent_news = set()

async def fetch_news():
    url = "https://tajmedun.tj/"
    async with ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            news_items = soup.select(".entry-title a")
            new_posts = []
            for item in news_items[:5]:
                title = item.text.strip()
                link = item['href']
                if link not in sent_news:
                    sent_news.add(link)
                    new_posts.append(f"<b>{title}</b>\n{link}")
            return new_posts

async def news_job():
    while True:
        try:
            news = await fetch_news()
            for post in news:
                await bot.send_message(CHANNEL_ID, post)
        except Exception as e:
            logging.error(f"Ошибка при получении новостей: {e}")
        await asyncio.sleep(600)

async def run_bot():
    logging.basicConfig(level=logging.INFO)
    asyncio.create_task(news_job())
    await dp.start_polling(bot)
