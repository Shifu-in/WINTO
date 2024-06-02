import logging
import json
from aiohttp import web
from pathlib import Path

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TXT_FILE = Path("../user_data.txt")

def load_data():
    if TXT_FILE.exists():
        data = {}
        with open(TXT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                user_id, balance, clicks = line.strip().split(',')
                data[user_id] = {'balance': int(balance), 'clicks': int(clicks)}
        return data
    return {}

def save_data(data):
    with open(TXT_FILE, 'w', encoding='utf-8') as f):
        for user_id, info in data.items():
            f.write(f"{user_id},{info['balance']},{info.get('clicks', 0)}\n")

async def get_user_data(request):
    user_id = request.query.get('user_id')
    logger.info(f"Fetching data for user_id: {user_id}")
    data = load_data()
    balance = data.get(user_id, {}).get("balance", 0)
    clicks = data.get(user_id, {}).get("clicks", 0)
    logger.info(f"User data: {user_id}, Balance: {balance}, Clicks: {clicks}")
    return web.json_response({'user_id': user_id, 'balance': balance, 'clicks': clicks})

async def update_user_data(request):
    data = await request.json()
    user_id = data.get('user_id')
    balance = data.get('balance')
    clicks = data.get('clicks')
    logger.info(f"Updating data for user_id: {user_id}, Balance: {balance}, Clicks: {clicks}")
    
    user_data = load_data()
    user_data[user_id] = {"balance": balance, "clicks": clicks}
    save_data(user_data)
    
    logger.info(f"User data updated: {user_id}, Balance: {balance}, Clicks: {clicks}")
    return web.json_response({'status': 'success'})

async def cors_middleware(app, handler):
    async def middleware_handler(request):
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    return middleware_handler

app = web.Application(middlewares=[cors_middleware])
app.router.add_get('/api/get_user_data', get_user_data)
app.router.add_post('/api/update_user_data', update_user_data)

if __name__ == '__main__':
    logger.info("Starting server...")
    web.run_app(app)
