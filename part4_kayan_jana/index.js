document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');

  checkAuthentication();
  fetchPlaces(token);

  const priceFilter = document.getElementById('price-filter');

  if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
      filterPlacesByPrice(event.target.value);
    });
  }
});

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (loginLink) {
    if (token) {
      loginLink.style.display = 'none';
    } else {
      loginLink.style.display = 'block';
    }
  }
}

async function fetchPlaces(token) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(
      'http://127.0.0.1:5000/api/v1/places/',
      {
        method: 'GET',
        headers: headers
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const places = await response.json();

    displayPlaces(places);
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');

  if (!placesList) return;

  placesList.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');

    card.className = 'place-card';

    const image = place.title === 'Test Place'
      ? 'images/hotel1.jpg'
      : 'images/hotel2.jpg';

    const title = place.title === 'Test Place'
      ? 'Royal Garden Suite'
      : 'Golden Pearl Residence';

    card.innerHTML = `
      <img src="${image}" alt="${title}" class="place-image">

      <div class="place-card-content">
        <h3>${title}</h3>
        <p><strong>Price:</strong> $${place.price} per night</p>
        <p>${place.title === 'Test Place'
  ? 'A luxurious and comfortable suite designed for a relaxing stay.'
  : 'An elegant private residence with a warm and luxurious atmosphere.'
}</p>

        <a href="place.html?id=${place.id}" class="details-button">
          View Details
        </a>
      </div>
    `;

    placesList.appendChild(card);
  });
}

function filterPlacesByPrice(selectedPrice) {
  const cards = document.querySelectorAll('.place-card');

  cards.forEach(card => {
    const priceText = card.querySelector('p strong')
      .parentElement.textContent;

    const price = parseFloat(
      priceText.replace(/[^0-9.]/g, '')
    );

    if (selectedPrice === 'All' || price <= Number(selectedPrice)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}
