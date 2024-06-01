from aiohttp import web
import aiosqlite
import json

async def get_user_data(request):
    user_id = request.query.get('user_id')
    async with aiosqlite.connect('bot_database.db') as db:
        async with db.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                balance = result[0]
            else:
                balance = 0
    return web.json_response({'user_id': user_id, 'balance': balance})

async def update_user_data(request):
    data = await request.json()
    user_id = data.get('user_id')
    balance = data.get('balance')
    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute('INSERT OR REPLACE INTO users (user_id, balance) VALUES (?, ?)', (user_id, balance))
        await db.commit()
    return web.json_response({'status': 'success'})

app = web.Application()
app.router.add_get('/get_user_data', get_user_data)
app.router.add_post('/update_user_data', update_user_data)

if __name__ == '__main__':
    web.run_app(app)
