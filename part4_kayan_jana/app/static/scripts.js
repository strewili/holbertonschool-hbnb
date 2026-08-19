document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }
});

async function loginUser(email, password) {
    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Store JWT in a cookie for session management
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            showLoginError(data.error || 'Invalid credentials');
        }
    } catch (err) {
        showLoginError('Network error, please try again.');
    }
}

function showLoginError(message) {
    let errorEl = document.getElementById('login-error');

    // Create the error element once, reuse it on subsequent attempts
    if (!errorEl) {
        errorEl = document.createElement('p');
        errorEl.id = 'login-error';
        errorEl.style.color = 'red';
        document.getElementById('login-form').appendChild(errorEl);
    }

    errorEl.textContent = message;
}