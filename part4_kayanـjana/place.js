document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();
  const token = getCookie('token');

  checkAuthentication(token);

  if (placeId) {
    fetchPlaceDetails(token, placeId);
  } else {
    console.error('Place ID not found in URL');
  }
});

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function checkAuthentication(token) {
  const addReviewSection = document.getElementById('add-review');

  if (!addReviewSection) return;

  if (token) {
    addReviewSection.style.display = 'block';
  } else {
    addReviewSection.style.display = 'none';
  }
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(
      `http://127.0.0.1:5000/api/v1/places/${placeId}`,
      {
        method: 'GET',
        headers: headers
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const place = await response.json();

    displayPlaceDetails(place);
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');

  if (!placeDetails) return;

  const ownerName = place.owner
    ? `${place.owner.first_name} ${place.owner.last_name}`
    : 'Unknown';

  placeDetails.innerHTML = `
    <h1>${place.title}</h1>

    <div class="place-info">
      <p><strong>Host:</strong> ${ownerName}</p>

      <p><strong>Price:</strong> $${place.price} per night</p>

      <h2>Description</h2>
      <p>${place.description || 'No description available.'}</p>

      <h2>Amenities</h2>

      <div class="amenities">
        ${
          place.amenities && place.amenities.length > 0
            ? place.amenities.map(amenity => `
                <div class="amenity">
                  <p>${amenity.name || amenity}</p>
                </div>
              `).join('')
            : '<p>No amenities available.</p>'
        }
      </div>
    </div>
  `;
}
