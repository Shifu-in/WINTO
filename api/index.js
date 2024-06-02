const { json, send } = require('micro');
const { router, get, post } = require('microrouter');
const fs = require('fs');
const path = require('path');

const DATA_FILE = path.resolve(__dirname, '../user_data.txt');

// Функция для логирования
function log(message) {
    console.log(`[LOG] ${message}`);
}

function loadData() {
    log('Loading data');
    if (fs.existsSync(DATA_FILE)) {
        log(`Data file ${DATA_FILE} exists`);
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        const lines = data.split('\n');
        const result = {};
        lines.forEach(line => {
            const [user_id, balance, clicks] = line.split(',');
            if (user_id && balance && clicks) {
                result[user_id] = { balance: parseInt(balance, 10), clicks: parseInt(clicks, 10) };
            }
        });
        log('Data loaded successfully');
        return result;
    }
    log('Data file does not exist');
    return {};
}

function saveData(data) {
    log('Saving data');
    const lines = Object.keys(data).map(user_id => `${user_id},${data[user_id].balance},${data[user_id].clicks}`);
    fs.writeFileSync(DATA_FILE, lines.join('\n'), 'utf8');
    log('Data saved successfully');
}

async function getUserData(req, res) {
    log(`getUserData called with user_id: ${req.query.user_id}`);
    const { user_id } = req.query;
    const data = loadData();
    const user = data[user_id] || { balance: 0, clicks: 0 };
    res.setHeader('Content-Type', 'application/json');
    send(res, 200, user);
}

async function updateUserData(req, res) {
    log('updateUserData called');
    const newUser = await json(req);
    log(`Received user data: ${JSON.stringify(newUser)}`);
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
