// app.js
let balance = 0;
let clicks = 0;
const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get('user_id');

function startApp() {
    console.log("Starting app for user_id:", userId);
    document.getElementById('start-app').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    loadUserData();
}

function clickHandler() {
    clicks += 1;
    balance += 1;  // Увеличиваем баланс на 1 за каждый клик
    document.getElementById('clicks').innerText = clicks;
    document.getElementById('balance').innerText = balance;
    saveUserData();
}

async function saveAndGoBack() {
    try {
        console.log("Saving data and going back for user_id:", userId, "Balance:", balance, "Clicks:", clicks);
        await saveUserData();
        window.history.back();
    } catch (error) {
        console.error('Error saving data:', error);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    if (userId) {
        startApp();
    }
});

// Запрещаем двойной тап и масштабирование
document.addEventListener('gesturestart', function (e) {
    e.preventDefault();
});
document.addEventListener('dblclick', function (e) {
    e.preventDefault();
});
