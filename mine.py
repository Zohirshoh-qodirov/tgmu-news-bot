import asyncio
from bot import run_bot
from web import app
from threading import Thread

def start_web():
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    Thread(target=start_web).start()
    asyncio.run(run_bot())
