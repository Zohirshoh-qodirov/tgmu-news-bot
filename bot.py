import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Хранилище уже опубликованных новостей
posted_links = set()

async def fetch_news():
    url = 'https://tajmedun.tj/ru/novosti/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            page_content = await response.text()
            soup = BeautifulSoup(page_content, 'html.parser')
            news_items = soup.find_all('div', class_='news-item')  # Замените на актуальный класс

            new_posts = []

            for item in news_items:
                title_tag = item.find('h3')
                link_tag = item.find('a')
                img_tag = item.find('img')
                desc_tag = item.find('p')

                if not (title_tag and link_tag):
                    continue

                title = title_tag.get_text(strip=True)
                link = link_tag['href']
                if not link.startswith('http'):
                    link = 'https://tajmedun.tj' + link

                if link in posted_links:
                    continue  # Уже опубликовано

                image_url = ''
                if img_tag and img_tag.get('src'):
                    image_url = img_tag['src']
                    if not image_url.startswith('http'):
                        image_url = 'https://tajmedun.tj' + image_url

                description = desc_tag.get_text(strip=True) if desc_tag else ''

                new_posts.append({
                    'title': title,
                    'link': link,
                    'image_url': image_url,
                    'description': description
                })

                posted_links.add(link)

            return new_posts

async def post_news():
    news = await fetch_news()
    for item in news:
        message = f"<b>{item['title']}</b>\n\n{item['description']}\n\n<a href='{item['link']}'>Читать полностью</a>"
        try:
            if item['image_url']:
                await bot.send_photo(CHANNEL_ID, photo=item['image_url'], caption=message, parse_mode='HTML')
            else:
                await bot.send_message(CHANNEL_ID, message, parse_mode='HTML')
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот, который публикует новости с сайта ТГМУ в канал.")

@dp.message_handler(commands=['post'])
async def manual_post(message: types.Message):
    await message.reply("Начинаю публикацию новых новостей...")
    await post_news()
    await message.reply("Публикация завершена!")

async def scheduler():
    while True:
        await post_news()
        await asyncio.sleep(3600)  # Проверять каждые 60 минут

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dp, skip_updates=True)
