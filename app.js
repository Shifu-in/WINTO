let balance = 0;

function startApp() {
    loadBalanceFromServer();
}

function clickHandler() {
    balance += 10;
    updateBalanceDisplay();
    saveBalanceToServer();
}

function saveAndGoBack() {
    saveBalanceToServer();
    // Redirect to main page or perform the necessary action
    window.location.href = 'index.html'; // Update this if necessary
}

function loadBalanceFromServer() {
    fetch('/get_balance')
        .then(response => response.json())
        .then(data => {
            balance = data.balance;
            updateBalanceDisplay();
        })
        .catch(error => console.error('Error loading balance:', error));
}

function saveBalanceToServer() {
    fetch('/update_balance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ balance: balance })
    })
    .then(response => response.json())
    .then(data => console.log('Balance saved:', data))
    .catch(error => console.error('Error saving balance:', error));
}

function updateBalanceDisplay() {
    document.getElementById('balanceAmount').textContent = balance;
}
