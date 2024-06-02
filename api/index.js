const { json, send } = require('micro');
const { router, get, post } = require('microrouter');
const fs = require('fs');
const path = require('path');

const DATA_FILE = path.resolve(__dirname, '../user_data.txt');

function loadData() {
    if (fs.exists(DATA_FILE)) {
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        const lines = data.split('\n');
        const result = {};
        lines.forEach(line => {
            const [user_id, balance, clicks] = line.split(',');
            if (user_id && balance && clicks) {
                result[user_id] = { balance: parseInt(balance, 10), clicks: parseInt(clicks, 10) };
            }
        });
        return result;
    }
    return {};
}

function saveData(data) {
    const lines = Object.keys(data).map(user_id => `${user_id},${data[user_id].balance},${data[user_id].clicks}`);
    fs.writeFileSync(DATA_FILE, lines.join('\n'), 'utf8');
}

async function getUserData(req, res) {
    const { user_id } = req.query;
    const data = loadData();
    const user = data[user_id] || { balance: 0, clicks: 0 };
    res.setHeader('Content-Type', 'application/json');
    send(res, 200, user);
}

async function updateUserData(req, res) {
    const newUser = await json(req);
    const data = loadData();
    data[newUser.user_id] = { balance: newUser.balance, clicks: newUser.clicks };
    saveData(data);
    res.setHeader('Content-Type', 'application/json');
    send(res, 200, { status: 'success' });
}

module.exports = router(
    get('/api/get_user_data', getUserData),
    post('/api/update_user_data', updateUserData)
);
