/* ============================================================
   HBnB — Simple Web Client
   Task 1: Login (JWT stored in a cookie)
   Task 2: List of Places + client-side price filter
   Task 3: Place details
   Task 4: Add review (authenticated users only)
   ============================================================ */

'use strict';

const API_BASE = 'http://127.0.0.1:5000/api/v1';

/* Fallback images so cards always look right, whatever the API returns. */
const PLACE_IMAGES = [
  'images/place1.png', 'images/place2.png', 'images/place3.png',
  'images/place4.png', 'images/place5.png', 'images/place6.png'
];
const GUEST_IMAGES = [
  'images/guest1.png', 'images/guest2.png', 'images/guest3.png',
  'images/guest4.png', 'images/guest5.png', 'images/guest6.png'
];

/* ------------------------------------------------------------
   Cookies
   ------------------------------------------------------------ */

function setCookie (name, value, days = 1) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

function getCookie (name) {
  const found = document.cookie
    .split('; ')
    .find((row) => row.startsWith(`${name}=`));
  return found ? decodeURIComponent(found.split('=').slice(1).join('=')) : null;
}

function deleteCookie (name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
}

const getToken = () => getCookie('token');
const isLoggedIn = () => Boolean(getToken());

/* ------------------------------------------------------------
   Helpers
   ------------------------------------------------------------ */

function pick (list, key) {
  let sum = 0;
  const str = String(key || '');
  for (let i = 0; i < str.length; i++) sum += str.charCodeAt(i);
  return list[sum % list.length];
}

function escapeHtml (value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function getPlaceIdFromURL () {
  return new URLSearchParams(window.location.search).get('place_id');
}

function showMessage (form, text, isError = true) {
  if (!form) return;
  let box = form.querySelector('.form-message');
  if (!box) {
    box = document.createElement('p');
    box.className = 'form-message';
    form.appendChild(box);
  }
  box.textContent = text;
  box.style.color = isError ? '#C0483F' : '#2E7D62';
  box.style.fontSize = '14px';
  box.style.marginTop = '14px';
  box.style.textAlign = 'center';
}

/* Swap the header button between Login and Logout. */
function updateAuthLink () {
  const link = document.getElementById('login-link');
  if (!link) return;

  if (isLoggedIn()) {
    link.textContent = 'Logout';
    link.href = '#';
    link.addEventListener('click', (event) => {
      event.preventDefault();
      deleteCookie('token');
      window.location.href = 'index.html';
    });
  } else {
    link.textContent = 'Login';
    link.href = 'login.html';
  }
}

/* ------------------------------------------------------------
   Task 1 — Login
   ------------------------------------------------------------ */

function initLogin () {
  const form = document.getElementById('login-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        setCookie('token', data.access_token);
        window.location.href = 'index.html';
      } else {
        showMessage(form, 'Invalid email or password. Please try again.');
      }
    } catch (error) {
      showMessage(form, 'Could not reach the API. Is the server running?');
    }
  });
}

/* ------------------------------------------------------------
   Task 2 — List of Places (+ price filter)
   ------------------------------------------------------------ */

let allPlaces = [];

function buildPlaceCard (place, index) {
  const image = pick(PLACE_IMAGES, place.id || index);
  const price = Number(place.price) || 0;
  const title = escapeHtml(place.title || 'Unnamed place');

  const article = document.createElement('article');
  article.className = 'place-card';
  article.dataset.price = String(price);

  article.innerHTML = `
    <div class="place-media">
      <img src="${image}" alt="${title}" class="place-image">
      <span class="badge">Calm stay</span>
      <span class="fav" aria-hidden="true">&hearts;</span>
    </div>
    <div class="place-card-body">
      <div class="place-top">
        <h3 class="place-name">${title}</h3>
        <span class="rating">&#9733; 4.8</span>
      </div>
      <p class="place-location">${escapeHtml(place.description || 'A quiet place to stay')}</p>
      <ul class="place-tags">
        <li>WiFi</li>
        <li>Quiet</li>
      </ul>
      <div class="place-foot">
        <p class="place-price"><span class="amount">$${price}</span> per night</p>
        <a href="place.html?place_id=${encodeURIComponent(place.id)}" class="details-button">View Details</a>
      </div>
    </div>
  `;
  return article;
}

function renderPlaces (places) {
  const list = document.getElementById('places-list');
  if (!list) return;

  list.textContent = '';

  if (!places.length) {
    const empty = document.createElement('p');
    empty.className = 'filter-hint';
    empty.textContent = 'No places match this price yet.';
    list.appendChild(empty);
  } else {
    places.forEach((place, i) => list.appendChild(buildPlaceCard(place, i)));
  }

  const hint = document.querySelector('.filter-hint');
  if (hint) hint.innerHTML = `Showing <strong>${places.length}</strong> places`;
}

function applyPriceFilter () {
  const select = document.getElementById('price-filter');
  if (!select) return;

  const value = select.value;
  const filtered = value === 'all'
    ? allPlaces
    : allPlaces.filter((place) => Number(place.price) <= Number(value));

  renderPlaces(filtered);
}

async function fetchPlaces () {
  const list = document.getElementById('places-list');
  if (!list) return;

  try {
    const response = await fetch(`${API_BASE}/places/`);
    if (!response.ok) throw new Error('Request failed');

    allPlaces = await response.json();
    applyPriceFilter();
  } catch (error) {
    // Keep the static demo cards already in the HTML when the API is offline.
    console.warn('Could not load places from the API — showing sample content.');
  }
}

function initIndex () {
  if (!document.getElementById('places-list')) return;

  const select = document.getElementById('price-filter');
  if (select) select.addEventListener('change', applyPriceFilter);

  fetchPlaces();
}

/* ------------------------------------------------------------
   Task 3 — Place details
   ------------------------------------------------------------ */

function renderPlaceDetails (place) {
  const banner = document.querySelector('.page-banner h1');
  if (banner) banner.textContent = place.title || 'Place details';

  const info = document.querySelector('.place-info');
  if (!info) return;

  const owner = place.owner || {};
  const host = `${owner.first_name || ''} ${owner.last_name || ''}`.trim() || 'Unknown host';

  const nameEl = info.querySelector('h2');
  if (nameEl) nameEl.textContent = place.title || '';

  const values = info.querySelectorAll('.info-item .v');
  if (values[0]) values[0].textContent = host;
  if (values[1]) values[1].textContent = `$${Number(place.price) || 0} / night`;

  const desc = info.querySelector('.desc');
  if (desc) desc.textContent = place.description || 'No description provided.';

  const amenities = info.querySelector('.amenities');
  if (amenities && Array.isArray(place.amenities)) {
    amenities.textContent = '';
    if (!place.amenities.length) {
      const li = document.createElement('li');
      li.textContent = 'No amenities listed';
      amenities.appendChild(li);
    } else {
      place.amenities.forEach((amenity) => {
        const li = document.createElement('li');
        li.textContent = amenity.name || String(amenity);
        amenities.appendChild(li);
      });
    }
  }

  const hero = document.querySelector('.place-hero-img');
  if (hero) {
    hero.src = pick(PLACE_IMAGES, place.id);
    hero.alt = place.title || 'Place image';
  }
}

function renderReviews (reviews) {
  const list = document.getElementById('reviews-list');
  if (!list) return;

  list.textContent = '';

  if (!reviews.length) {
    const empty = document.createElement('p');
    empty.className = 'filter-hint';
    empty.textContent = 'No reviews yet — be the first to write one.';
    list.appendChild(empty);
    return;
  }

  reviews.forEach((review) => {
    const article = document.createElement('article');
    article.className = 'review-card';
    article.innerHTML = `
      <div class="review-inner">
        <div class="review-head">
          <img src="${pick(GUEST_IMAGES, review.user_id)}" alt="Guest" class="avatar">
          <span class="review-who">
            <span class="review-user">Guest</span>
            <span class="review-date">Verified stay</span>
          </span>
          <span class="review-rating">&#9733; ${escapeHtml(review.rating)}</span>
        </div>
        <p class="review-text">${escapeHtml(review.text)}</p>
      </div>
    `;
    list.appendChild(article);
  });

  const hint = document.querySelector('.reviews-head .filter-hint');
  if (hint) hint.textContent = `${reviews.length} review${reviews.length === 1 ? '' : 's'}`;
}

async function initPlaceDetails () {
  const details = document.getElementById('place-details');
  if (!details) return;

  // Only logged-in users may add a review.
  const addReview = document.getElementById('add-review');
  if (addReview && !isLoggedIn()) addReview.style.display = 'none';

  const placeId = getPlaceIdFromURL();
  if (!placeId) return;                       // keep the sample content

  const reviewLink = document.querySelector('.form-note a[href="add_review.html"]');
  if (reviewLink) reviewLink.href = `add_review.html?place_id=${encodeURIComponent(placeId)}`;

  try {
    const response = await fetch(`${API_BASE}/places/${placeId}`);
    if (!response.ok) throw new Error('Request failed');
    renderPlaceDetails(await response.json());
  } catch (error) {
    console.warn('Could not load place details — showing sample content.');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/reviews/`);
    if (!response.ok) throw new Error('Request failed');
    const reviews = await response.json();
    renderReviews(reviews.filter((review) => review.place_id === placeId));
  } catch (error) {
    console.warn('Could not load reviews.');
  }
}

/* ------------------------------------------------------------
   Task 4 — Add review
   ------------------------------------------------------------ */

async function submitReview (form, placeId, text, rating) {
  try {
    const response = await fetch(`${API_BASE}/reviews/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({ text, rating: Number(rating), place_id: placeId })
    });

    if (response.ok) {
      showMessage(form, 'Thank you! Your review has been added.', false);
      form.reset();
      return true;
    }

    const data = await response.json().catch(() => ({}));
    showMessage(form, data.error || 'Could not submit your review.');
    return false;
  } catch (error) {
    showMessage(form, 'Could not reach the API. Is the server running?');
    return false;
  }
}

function initReviewForm () {
  const form = document.getElementById('review-form');
  if (!form) return;

  const onAddReviewPage = Boolean(document.querySelector('.review-page'));

  // The dedicated page is for authenticated users only.
  if (onAddReviewPage && !isLoggedIn()) {
    window.location.href = 'index.html';
    return;
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    if (!isLoggedIn()) {
      window.location.href = 'login.html';
      return;
    }

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
      showMessage(form, 'No place selected — open a place first.');
      return;
    }

    const text = document.getElementById('review-text').value.trim();
    const ratingField = form.querySelector('[name="rating"]:checked') ||
                        document.getElementById('rating');
    const rating = ratingField ? ratingField.value : '';

    if (!text || !rating) {
      showMessage(form, 'Please write a review and choose a rating.');
      return;
    }

    const ok = await submitReview(form, placeId, text, rating);
    if (ok && onAddReviewPage) {
      setTimeout(() => {
        window.location.href = `place.html?place_id=${encodeURIComponent(placeId)}`;
      }, 1200);
    }
  });
}

/* ------------------------------------------------------------
   Boot
   ------------------------------------------------------------ */

document.addEventListener('DOMContentLoaded', () => {
  updateAuthLink();
  initLogin();
  initIndex();
  initPlaceDetails();
  initReviewForm();
});
