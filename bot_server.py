import logging
import json
import pandas as pd
from aiohttp import web
from pathlib import Path

# Настройка логирования
logging.basicConfig(level=logging.INFO)

DATA_FILE = Path("user_data.json")
EXCEL_FILE = Path("user_data.xlsx")
TXT_FILE = Path("user_data.txt")

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
            f.write(f"user_id: {user_id}, balance: {info['balance']}, clicks: {info.get('clicks', 0)}\n")

async def get_user_data(request):
    user_id = request.query.get('user_id')
    logging.info(f"Fetching data for user_id: {user_id}")
    data = load_data()
    balance = data.get(user_id, {}).get("balance", 0)
    clicks = data.get(user_id, {}).get("clicks", 0)
    logging.info(f"User data: {user_id}, Balance: {balance}, Clicks: {clicks}")
    return web.json_response({'user_id': user_id, 'balance': balance, 'clicks': clicks})

async def update_user_data(request):
    data = await request.json()
    user_id = data.get('user_id')
    balance = data.get('balance')
    clicks = data.get('clicks')
    logging.info(f"Updating data for user_id: {user_id}, Balance: {balance}, Clicks: {clicks}")
    
    user_data = load_data()
    user_data[user_id] = {"balance": balance, "clicks": clicks}
    save_data(user_data)
    save_to_excel(user_data)
    save_to_txt(user_data)
    
    logging.info(f"User data updated: {user_id}, Balance: {balance}, Clicks: {clicks}")
    return web.json_response({'status': 'success'})

app = web.Application()
app.router.add_get('/get_user_data', get_user_data)
app.router.add_post('/update_user_data', update_user_data)

if __name__ == '__main__':
    logging.info("Starting server...")
    web.run_app(app)
