import os
from telegram import Bot, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
import threading
import asyncio

# Задайте переменные окружения на Render:
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # Например: -1001234567890

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

# === Команда /post для публикации в канал ===
async def post_to_channel(update, context):
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text="📝 Новый пост в канале!")
        await context.bot.send_photo(chat_id=CHANNEL_ID, photo="https://example.com/image.jpg", caption="Картинка и ссылка ниже 👇")
        await context.bot.send_message(chat_id=CHANNEL_ID, text="🔗 https://example.com")
        await update.message.reply_text("✅ Отправлено в канал.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

# === Поддержка Render через Flask ===
@app.route('/')
def home():
    return "Бот работает!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# === Основной запуск ===
async def run_bot():
    app_builder = ApplicationBuilder().token(BOT_TOKEN).build()
    app_builder.add_handler(CommandHandler("post", post_to_channel))
    await app_builder.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(run_bot())
