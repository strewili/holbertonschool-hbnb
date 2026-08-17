document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(
                    '/api/v1/auth/login',
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            email: email,
                            password: password
                        })
                    }
                );

                if (response.ok) {
                    const data = await response.json();

                    document.cookie =
                        `token=${data.access_token}; path=/`;

                    window.location.href = '/index.html';
                } else {
                    let errorMessage =
                        loginForm.querySelector('.error-message');

                    if (!errorMessage) {
                        errorMessage = document.createElement('p');
                        errorMessage.className = 'error-message';
                        loginForm.appendChild(errorMessage);
                    }

                    errorMessage.textContent =
                        'Login failed. Please check your email and password.';
                }
            } catch (error) {
                let errorMessage =
                    loginForm.querySelector('.error-message');

                if (!errorMessage) {
                    errorMessage = document.createElement('p');
                    errorMessage.className = 'error-message';
                    loginForm.appendChild(errorMessage);
                }

                errorMessage.textContent =
                    'Unable to connect to the server.';
            }
        });
    }
});