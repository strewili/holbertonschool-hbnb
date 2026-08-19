document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');

  // Redirect unauthenticated users
  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  const placeId = getPlaceIdFromURL();
  const reviewForm = document.getElementById('review-form');

  if (!placeId) {
    alert('Place ID not found.');
    return;
  }

  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const reviewText = document.getElementById('review').value.trim();
      const rating = document.getElementById('rating').value;

      if (!reviewText || !rating) {
        alert('Please enter a review and select a rating.');
        return;
      }

      await submitReview(token, placeId, reviewText, rating);
    });
  }
});

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

async function submitReview(token, placeId, reviewText, rating) {
  try {
    const response = await fetch(
      'http://127.0.0.1:5000/api/v1/reviews/',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text: reviewText,
          rating: Number(rating),
          place_id: placeId
        })
      }
    );

    const data = await response.json();

    if (response.ok) {
      alert('Review submitted successfully!');

      document.getElementById('review-form').reset();
    } else {
      alert(data.error || 'Failed to submit review.');
    }
  } catch (error) {
    console.error('Error submitting review:', error);
    alert('An error occurred while submitting the review.');
  }
}
