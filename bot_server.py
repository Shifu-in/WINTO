import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web
import asyncio
from pathlib import Path

API_TOKEN = 'YOUR_API_TOKEN'
DATA_FILE = Path("user_data.json")
CHANNEL_ID = '@yourchannel'
BONUS_AMOUNT = 20000

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def handle_get_balance(request):
    user_id = request.query.get('user_id')
    data = load_data()
    balance = data.get(user_id, {}).get('balance', 0)
    return web.json_response({'balance': balance})

async def handle_update_balance(request):
    try:
        data = await request.json()
        user_id = data['user_id']
        balance = data['balance']
        user_data = load_data()
        user_data[user_id] = {"balance": balance}
        save_data(user_data)
        return web.json_response({'status': 'success'})
    except Exception as e:
        logger.error(f"Error updating balance: {e}")
        return web.json_response({'status': 'error'}, status=500)

app = web.Application()
app.router.add_get('/get_balance', handle_get_balance)
app.router.add_post('/update_balance', handle_update_balance)

async def main():
    dp.message.register(send_welcome, Command("start"))

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    logger.info("Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
