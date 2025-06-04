import requests
from bs4 import BeautifulSoup
import telegram
import time

BOT_TOKEN = 'BOT_TOKEN'
CHANNEL_NAME = '@TGMUNEWS'
bot = telegram.Bot(token=BOT_TOKEN)

sent_links = set()

def get_news():
    url = "https://tajmedun.tj/ru/novosti/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select(".blog-item")

    news = []
    for article in articles:
        title = article.select_one(".blog-title").get_text(strip=True)
        link = "https://tajmedun.tj" + article.select_one("a")["href"]
        image = "https://tajmedun.tj" + article.select_one("img")["src"]
        date = article.select_one(".blog-date").get_text(strip=True)

        if link not in sent_links:
            sent_links.add(link)
            news.append((title, link, image, date))
    return news

def send_news():
    for title, link, image, date in get_news():
        message = f"<b>{title}</b>\n🗓 {date}\n<a href='{image}'>⠀</a>\n<a href='{link}'>Читать подробнее</a>"
        bot.send_message(chat_id=CHANNEL_NAME, text=message, parse_mode=telegram.ParseMode.HTML)

if __name__ == '__main__':
    while True:
        try:
            send_news()
            time.sleep(60)  # каждые 10 минут
        except Exception as e:
            print("Ошибка:", e)
            time.sleep(30)
