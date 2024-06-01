import loggingimport json
from aiogram import Bot, Dispatcher, typesfrom aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButtonfrom aiohttp import web
import asyncioimport aiosqlite
API_TOKEN = '7098707163:AAFDsdeAL4fR9P_o2uEuChpi-KWmpz1vcFM'
WEBHOOK_URL = 'https://win-umber.vercel.app/webhook'WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 3000
logging.basicConfig(level=logging.INFO)logger = logging.getLogger(__name__)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
async def create_db():    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users                            (user_id INTEGER PRIMARY KEY, balance INTEGER)''')
        await db.commit()
@dp.message_handler(Command('start'))async def send_welcome(message: Message):
    user_id = message.from_user.id    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Запустить приложение", url=f"https://win-umber.vercel.app/?user_id={user_id}")]    ])
    await message.answer("Добро пожаловать в Clicker Bot! Нажмите 'Запустить приложение', чтобы начать.", reply_markup=keyboard)    logger.info(f"User {message.from_user.id} started the bot.")
async def update_balance(request):
    data = await request.json()    user_id = int(request.query['user_id'])
    new_balance = data['balance']
    async with aiosqlite.connect('bot_database.db') as db:        await db.execute('INSERT OR REPLACE INTO users (user_id, balance) VALUES (?, ?)', (user_id, new_balance))
        await db.commit()    
    return web.json_response({'status': 'success', 'balance': new_balance})
async def on_startup(app):    await bot.set_webhook(WEBHOOK_URL)
    await create_db()
app = web.Application()app.router.add_post('/update_balance', update_balance)
if name == '__main__':
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)    asyncio.run(dp.start_polling(bot))
