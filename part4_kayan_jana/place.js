document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();
  const token = getCookie('token');

  const addReviewLink = document.getElementById('add-review-link');

  if (addReviewLink && placeId) {
    addReviewLink.href = `add_review.html?id=${placeId}`;
  }

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
    await fetchReviews(token, placeId);

  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

async function fetchReviews(token, placeId) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(
      'http://127.0.0.1:5000/api/v1/reviews/',
      {
        method: 'GET',
        headers: headers
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const reviews = await response.json();

    const placeReviews = reviews.filter(
      review => review.place_id === placeId
    );

    displayReviews(placeReviews);

  } catch (error) {
    console.error('Error fetching reviews:', error);
  }
}

function displayReviews(reviews) {
  const reviewsSection = document.getElementById('reviews');

  if (!reviewsSection) return;

  reviewsSection.innerHTML = '<h2>Reviews</h2>';

  if (reviews.length === 0) {
    reviewsSection.innerHTML += '<p>No reviews yet.</p>';
  } else {
    reviews.forEach(review => {
      const article = document.createElement('article');
      article.className = 'review-card';

      article.innerHTML = `
        <p>${review.text}</p>
        <p>Rating: ${review.rating}/5</p>
      `;

      reviewsSection.appendChild(article);
    });
  }

  const addReviewLink = document.createElement('a');
  addReviewLink.href = `add_review.html?id=${getPlaceIdFromURL()}`;
  addReviewLink.id = 'add-review-link';
  addReviewLink.className = 'details-button';
  addReviewLink.textContent = 'Add Review';

  reviewsSection.appendChild(addReviewLink);
}

function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');

  if (!placeDetails) return;

  const ownerName = place.owner
    ? `${place.owner.first_name} ${place.owner.last_name}`
    : 'Unknown';

  placeDetails.innerHTML = `
    <h1>Luxury Hotel Suite</h1>

    <div class="place-info">
      <p><strong>Host:</strong> ${ownerName}</p>

      <p><strong>Price:</strong> $${place.price} per night</p>

      <h2>Description</h2>
      <p>
        A luxurious and elegant hotel suite designed for a relaxing
        and comfortable stay, with beautiful interiors and everything
        you need for a memorable experience.
      </p>

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
