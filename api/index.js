const { json, send } = require('micro');
const { router, get, post } = require('microrouter');
const fs = require('fs');
const path = require('path');

const DATA_FILE = path.resolve(__dirname, 'user_data.json');

function loadData() {
    if (fs.existsSync(DATA_FILE)) {
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        return JSON.parse(data);
    }
    return {};
}

function saveData(data) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
}

async function getUserData(req, res) {
    const { user_id } = req.query;
    const data = loadData();
    const user = data[user_id] || { balance: 0, clicks: 0 };
    res.setHeader('Content-Type', 'application/json');  // Установка заголовка Content-Type
    send(res, 200, user);
}

async function updateUserData(req, res) {
    const newUser = await json(req);
    const data = loadData();
    data[newUser.user_id] = { balance: newUser.balance, clicks: newUser.clicks };
    saveData(data);
    res.setHeader('Content-Type', 'application/json');  // Установка заголовка Content-Type
    send(res, 200, { status: 'success' });
}

module.exports = router(
    get('/get_user_data', getUserData),
    post('/update_user_data', updateUserData)
);
