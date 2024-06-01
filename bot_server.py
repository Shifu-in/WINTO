import logging
import json
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import aiosqlite
from pathlib import Path

API_TOKEN = '7098707163:AAFDsdeAL4fR9P_o2uEuChpi-KWmpz1vcFM'
DATA_FILE = Path("user_data.json")
EXCEL_FILE = Path("user_data.xlsx")
TXT_FILE = Path("user_data.txt")
CHANNEL_ID = '@shifucrypto'
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

def save_to_excel(data):
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index.name = 'user_id'
    df.to_excel(EXCEL_FILE)

def save_to_txt(data):
    with open(TXT_FILE, 'w', encoding='utf-8') as f:
        for user_id, info in data.items():
            f.write(f"user_id: {user_id}, balance: {info['balance']}\n")

async def create_db():
    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users
                            (user_id INTEGER PRIMARY KEY, balance INTEGER, subscribed INTEGER DEFAULT 0)''')
        await db.commit()

        cursor = await db.execute('PRAGMA table_info(users)')
        columns = [info[1] for info in await cursor.fetchall()]
        if 'subscribed' not in columns:
            await db.execute('ALTER TABLE users ADD COLUMN subscribed INTEGER DEFAULT 0')
            await db.commit()

def get_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📲 Подписаться", url=f"https://t.me/{CHANNEL_ID.strip('@')}")],
        [InlineKeyboardButton(text="🔍 Проверить подписку", callback_data="check_subscription")]
    ])
    return keyboard

async def send_welcome(message: Message):
    welcome_message = (
        "👋 Привет! Добро пожаловать в наш кликер-бот!\n\n"
        "Для начала, пожалуйста, подпишитесь на наш канал и получите бонус 🎁."
    )
    await message.answer(welcome_message, reply_markup=get_subscription_keyboard())
    logger.info(f"User {message.from_user.id} started the bot.")

async def check_subscription_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

    user_data = load_data()
    async with aiosqlite.connect('bot_database.db') as db:
        async with db.execute('SELECT balance, subscribed FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()

        if result is None:
            balance = 0
            subscribed = 0
            await db.execute('INSERT INTO users (user_id, balance, subscribed) VALUES (?, ?, ?)', (user_id, balance, subscribed))
            await db.commit()
        else:
            balance, subscribed = result

        if chat_member.status in ['member', 'administrator', 'creator']:
            if not subscribed:
                new_balance = balance + BONUS_AMOUNT
                await db.execute('UPDATE users SET balance = ?, subscribed = ? WHERE user_id = ?', (new_balance, 1, user_id))
                await db.commit()

                user_data[str(user_id)] = {"balance": new_balance}
                save_data(user_data)
                save_to_excel(user_data)
                save_to_txt(user_data)

                await bot.send_message(user_id, f"🎉 Спасибо за подписку! Вам начислено {BONUS_AMOUNT} монет. Ваш новый баланс: {new_balance}")
                logger.info(f"User {callback_query.from_user.id} subscribed. New balance: {new_balance}")

                # Добавляем кнопку для запуска приложения
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Запустить приложение", url=f"https://win-umber.vercel.app/?user_id={user_id}")]
                ])
                await bot.send_message(user_id, "🎮 Нажмите 'Запустить приложение', чтобы начать играть!", reply_markup=keyboard)
            else:
                await bot.send_message(user_id, f"💡 Вы уже получили бонус за подписку. Ваш текущий баланс: {balance}")
        else:
            await bot.send_message(user_id, "❌ Вы еще не подписаны на наш канал. Пожалуйста, подпишитесь и попробуйте снова.")

    await bot.answer_callback_query(callback_query.id)

async def main():
    await create_db()

    dp.message.register(send_welcome, Command("start"))
    dp.callback_query.register(check_subscription_handler, lambda c: c.data == 'check_subscription')

    logger.info("Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
