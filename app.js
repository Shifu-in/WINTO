let balance = 0;const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get('user_id');
function startApp() {    document.getElementById('start-app').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');}
function clickHandler() {
    balance += 1;    document.getElementById('balance').innerText = balance;
    saveBalanceToServer(balance);}
async function saveBalanceToServer(newBalance) {
    try {        const response = await fetch(`/update_balance?user_id=${userId}`, {
            method: 'POST',            headers: {
                'Content-Type': 'application/json'            },
            body: JSON.stringify({ balance: newBalance })        });
        const data = await response.json();        console.log('Balance saved:', data);
    } catch (error) {        console.error('Error saving balance:', error);
    }}
document.addEventListener('DOMContentLoaded', (event) => {
    if (userId) {        startApp();
    }});
