document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');
    
    if (userId) {
        const response = await fetch(`/get_user_data?user_id=${userId}`);
        const data = await response.json();
        const balance = data.balance;

        document.getElementById('balance').innerText = balance;
    }

    document.getElementById('click-button').addEventListener('click', async () => {
        let balance = parseInt(document.getElementById('balance').innerText, 10);
        balance += 1;
        document.getElementById('balance').innerText = balance;

        await fetch('/update_user_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId, balance: balance }),
        });
    });
});
