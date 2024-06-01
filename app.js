document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');

    async function getUserData() {
        const response = await fetch(`/get_user_data?user_id=${userId}`);
        const data = await response.json();
        return data.balance;
    }

    async function updateUserData(balance) {
        await fetch('/update_user_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId, balance: balance }),
        });
    }

    window.startApp = async function() {
        if (userId) {
            const balance = await getUserData();
            document.getElementById('balance').innerText = balance;
            document.getElementById('balance-container').style.display = 'block';
        } else {
            alert('User ID not found');
        }
    }

    document.getElementById('click-button').addEventListener('click', async () => {
        let balance = parseInt(document.getElementById('balance').innerText, 10);
        balance += 1;
        document.getElementById('balance').innerText = balance;

        await updateUserData(balance);
    });
});
