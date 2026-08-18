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
  'images/place1.jpg', 'images/place2.jpg', 'images/place3.jpg',
  'images/place4.jpg', 'images/place5.jpg', 'images/place6.jpg'
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

/* Includes the JWT in requests when the user is logged in. */
function authHeaders () {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

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

/* Spec: show the login link only when the user is NOT authenticated.
   When authenticated the link is hidden and a separate Logout link
   takes its place. */
function checkAuthentication () {
  const loginLink = document.getElementById('login-link');
  if (!loginLink) return getToken();

  if (!isLoggedIn()) {
    loginLink.style.display = 'block';
    const old = document.getElementById('logout-link');
    if (old) old.remove();
  } else {
    loginLink.style.display = 'none';

    if (!document.getElementById('logout-link')) {
      const logout = document.createElement('a');
      logout.id = 'logout-link';
      logout.className = 'login-button';
      logout.href = '#';
      logout.textContent = 'Logout';
      logout.addEventListener('click', (event) => {
        event.preventDefault();
        deleteCookie('token');
        window.location.href = 'index.html';
      });
      loginLink.insertAdjacentElement('afterend', logout);
    }
  }

  return getToken();
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
  places.forEach((place, i) => list.appendChild(buildPlaceCard(place, i)));
}

/* Filters whatever cards are on the page, so it works with API data
   and with the built-in sample cards alike. */
function applyPriceFilter () {
  const select = document.getElementById('price-filter');
  if (!select) return;

  const max = select.value;
  const cards = document.querySelectorAll('#places-list .place-card');
  let shown = 0;

  cards.forEach((card) => {
    const price = Number(card.dataset.price || 0);
    const visible = max === 'all' || price <= Number(max);
    card.style.display = visible ? '' : 'none';
    if (visible) shown += 1;
  });

  const hint = document.querySelector('.filter-hint');
  if (hint) {
    hint.innerHTML = shown
      ? `Showing <strong>${shown}</strong> of ${cards.length} places`
      : 'No places match this price.';
  }
}

/* Tells the user the API is not running instead of failing silently. */
function showApiNotice () {
  if (document.getElementById('api-notice')) return;

  const notice = document.createElement('p');
  notice.id = 'api-notice';
  notice.className = 'api-notice';
  notice.innerHTML =
    'Showing sample places — the API is not running. ' +
    'Start it with <code>python run.py</code> to load real data.';

  const filter = document.getElementById('filter');
  if (filter) filter.insertAdjacentElement('afterend', notice);
}

async function fetchPlaces () {
  const list = document.getElementById('places-list');
  if (!list) return;

  try {
    const response = await fetch(`${API_BASE}/places/`, { headers: authHeaders() });
    if (!response.ok) throw new Error('Request failed');

    allPlaces = await response.json();
    if (allPlaces.length) renderPlaces(allPlaces);
    else showApiNotice();
  } catch (error) {
    // Keep the sample cards already in the HTML and say why.
    showApiNotice();
  }

  applyPriceFilter();
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

/* Sample places used when the API is not running (index.html links
   here with ?demo=N so each card opens its own place, not always the first). */
const DEMO_PLACES = {
  '1': ['Seaside Calm Apartment', 'Jeddah, Saudi Arabia', 200, 'images/place1.jpg'],
  '2': ['Blue Hour Studio',       'Riyadh, Saudi Arabia', 120, 'images/place2.jpg'],
  '3': ['Golden Hills Retreat',   'Abha, Saudi Arabia',    85, 'images/place3.jpg'],
  '4': ['Dusk House',             'Taif, Saudi Arabia',   150, 'images/place4.jpg'],
  '5': ['Still Water Lodge',      'Al Ula, Saudi Arabia', 240, 'images/place5.jpg'],
  '6': ['Morning Mist Cottage',   'Al Baha, Saudi Arabia', 70, 'images/place6.jpg']
};

function renderDemoPlace (key) {
  const demo = DEMO_PLACES[key];
  if (!demo) return;
  const [title, location, price, image] = demo;

  const banner = document.querySelector('.page-banner h1');
  if (banner) banner.textContent = title;

  const bannerSub = document.querySelector('.page-banner > p:last-of-type');
  if (bannerSub) bannerSub.textContent = location;

  const crumb = document.querySelector('.crumbs');
  if (crumb) crumb.innerHTML = `<a href="index.html">Places</a> &rsaquo; ${title}`;

  const info = document.querySelector('.place-info');
  if (info) {
    const h2 = info.querySelector('h2');
    if (h2) h2.textContent = title;
    const loc = info.querySelector('.place-location');
    if (loc) loc.textContent = location;
    const values = info.querySelectorAll('.info-item .v');
    if (values[1]) values[1].textContent = `$${price} / night`;
  }

  const hero = document.querySelector('.place-hero-img');
  if (hero) { hero.src = image; hero.alt = title; }

  document.title = `HBnB — ${title}`;
}

/* Replaces the details card with a clear message when the place id in the
   URL is invalid, instead of silently leaving stale sample content. */
function showPlaceError (text) {
  const details = document.getElementById('place-details');
  if (!details) return;

  details.innerHTML = `
    <div class="place-info">
      <h2>Place not found</h2>
      <p class="desc">${escapeHtml(text)}</p>
      <p style="margin-top:18px">
        <a href="index.html" class="details-button">Back to all places</a>
      </p>
    </div>
  `;

  const reviews = document.querySelector('.reviews-section');
  if (reviews) reviews.style.display = 'none';

  const addReview = document.getElementById('add-review');
  if (addReview) addReview.style.display = 'none';

  const banner = document.querySelector('.page-banner h1');
  if (banner) banner.textContent = 'Place not found';
}

async function initPlaceDetails () {
  const details = document.getElementById('place-details');
  if (!details) return;

  // Only logged-in users may add a review.
  const addReview = document.getElementById('add-review');
  if (addReview) addReview.style.display = isLoggedIn() ? 'block' : 'none';

  const demoKey = new URLSearchParams(window.location.search).get('demo');
  if (demoKey) { renderDemoPlace(demoKey); return; }

  const placeId = getPlaceIdFromURL();
  if (!placeId) return;                       // keep the sample content

  const reviewLink = document.querySelector('.form-note a[href="add_review.html"]');
  if (reviewLink) reviewLink.href = `add_review.html?place_id=${encodeURIComponent(placeId)}`;

  try {
    const response = await fetch(`${API_BASE}/places/${placeId}`, { headers: authHeaders() });

    // The place id in the URL does not exist in the database.
    if (response.status === 404) {
      showPlaceError('This place does not exist. It may have been removed.');
      return;
    }
    if (!response.ok) throw new Error('Request failed');

    renderPlaceDetails(await response.json());
  } catch (error) {
    showPlaceError('Could not load this place. Is the API running?');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/reviews/`, { headers: authHeaders() });
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
  checkAuthentication();
  initLogin();
  initIndex();
  initPlaceDetails();
  initReviewForm();
});
