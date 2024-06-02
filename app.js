let balance = 0;
let clicks = 0;
const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get('user_id');

if (!userId) {
    console.error('User ID not provided!');
} else {
    console.log("Starting app for user_id:", userId);
    startApp();
}

function startApp() {
    document.getElementById('start-app').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    loadUserData();
}

function clickHandler() {
    clicks += 1;
    balance += 1; // Увеличиваем баланс на 1 за каждый клик
    document.getElementById('clicks').innerText = clicks;
    document.getElementById('balance').innerText = balance;
    saveUserData();
}

async function saveAndGoBack() {
    try {
        console.log("Saving data and going back for user_id:", userId, "Balance:", balance, "Clicks:", clicks);
        await saveUserData();
        window.history.back(); // Возвращаемся назад
    } catch (error) {
        console.error('Error saving data:', error);
    }
}

async function loadUserData() {
    try {
        console.log("Loading data for user_id:", userId);
        const response = await fetch(`https://win-umber.vercel.app/api/get_user_data?user_id=${userId}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        balance = data.balance || 0;
        clicks = data.clicks || 0;
        document.getElementById('balance').innerText = balance;
        document.getElementById('clicks').innerText = clicks;
        console.log("Data loaded:", data);
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

async function saveUserData() {
    try {
        console.log("Saving data for user_id:", userId, "Balance:", balance, "Clicks:", clicks);
        const response = await fetch('https://win-umber.vercel.app/api/update_user_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId, balance: balance, clicks: clicks })
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Data saved:', data);
    } catch (error) {
        console.error('Error saving data:', error);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    if (userId) {
        startApp();
    }
});
