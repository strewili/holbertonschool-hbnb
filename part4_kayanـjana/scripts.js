// ---------- دوال مشتركة ----------
function getCookie(name) {
  const cookies = document.cookie.split('; ');
  for (const cookie of cookies) {
    const [key, value] = cookie.split('=');
    if (key === name) return decodeURIComponent(value);
  }
  return null;
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    if (loginLink) loginLink.style.display = 'inline-block';
  } else {
    if (loginLink) loginLink.style.display = 'none';
  }
  return token;
}

// ---------- تشغيل عند تحميل أي صفحة ----------
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();

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

// ---------- تسجيل الدخول ----------
async function loginUser(email, password) {
  const errorMessage = document.getElementById('error-message');

  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = 'index.html';
    } else {
      const errorData = await response.json().catch(() => ({}));
      const message = errorData.message || 'Invalid email or password.';
      if (errorMessage) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
      } else {
        alert(message);
      }
    }
  } catch (error) {
    console.error('Error during login:', error);
    if (errorMessage) {
      errorMessage.textContent = 'Server error. Please try again later.';
      errorMessage.style.display = 'block';
    } else {
      alert('Server error. Please try again later.');
    }
  }
}