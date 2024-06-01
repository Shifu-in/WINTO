let balance = 0;
const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get('user_id');

function startApp() {
    console.log("Starting app for user_id:", userId);
    document.getElementById('start-app').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    loadBalanceFromServer();
}

function clickHandler() {
    balance += 1;
    document.getElementById('balance').innerText = balance;
    saveBalanceToServer(balance);
}

async function loadBalanceFromServer() {
    try {
        console.log("Loading balance for user_id:", userId);
        const response = await fetch(`/get_user_data?user_id=${userId}`);
        const data = await response.json();
        balance = data.balance || 0;
        document.getElementById('balance').innerText = balance;
        console.log("Balance loaded:", balance);
    } catch (error) {
        console.error('Error loading balance:', error);
    }
}

async function saveBalanceToServer(newBalance) {
    try {
        console.log("Saving balance for user_id:", userId, "Balance:", newBalance);
        const response = await fetch('/update_user_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId, balance: newBalance })
        });
        const data = await response.json();
        console.log('Balance saved:', data);
    } catch (error) {
        console.error('Error saving balance:', error);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    if (userId) {
        startApp();
    }
});

// Запрет двойного тапа и масштабирования
document.addEventListener('gesturestart', function (e) {
    e.preventDefault();
});
document.addEventListener('dblclick', function (e) {
    e.preventDefault();
});
