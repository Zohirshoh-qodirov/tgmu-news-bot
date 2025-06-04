import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

URL = "https://tajmedun.tj/ru/novosti/"
SEEN_FILE = "seen_news.txt"


def load_seen_links():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())


def save_seen_link(link):
    with open(SEEN_FILE, "a") as f:
        f.write(link + "\n")


async def fetch_news():
    seen_links = load_seen_links()

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    news_items = soup.select(".news-item")  # селектор может отличаться

    for item in news_items:
        title_tag = item.select_one(".news-title")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = "https://tajmedun.tj" + title_tag.get("href")
        if link in seen_links:
            continue

        description_tag = item.select_one(".news-text")
        description = description_tag.get_text(strip=True) if description_tag else ""

        img_tag = item.select_one("img")
        image_url = "https://tajmedun.tj" + img_tag.get("src") if img_tag else None

        message = f"<b>{title}</b>\n\n{description}\n\n📎 <a href='{link}'>Источник</a>"

        try:
            if image_url:
                await bot.send_photo(CHANNEL_ID, photo=image_url, caption=message)
            else:
                await bot.send_message(CHANNEL_ID, message)
        except Exception as e:
            print(f"Ошибка при отправке: {e}")

        save_seen_link(link)


async def scheduler():
    while True:
        try:
            await fetch_news()
        except Exception as e:
            print(f"Ошибка в fetch_news: {e}")
        await asyncio.sleep(60)  # проверять каждый час


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("✅ Бот работает и отслеживает новости Tajmedun.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dp, skip_updates=True)
