# HBnB — Part 4: Simple Web Client

A front-end for the HBnB API built with **HTML5, CSS3 and JavaScript ES6**.
It lets a visitor browse places, log in, view a place's details and reviews,
and post a review — all without page reloads, using the Fetch API.

---

## Contents

- [Project structure](#project-structure)
- [Running the project](#running-the-project)
- [Test accounts](#test-accounts)
- [How to test the login functionality](#how-to-test-the-login-functionality)
- [How to test the list of places and filtering](#how-to-test-the-list-of-places-and-filtering)
- [How to test the place details page](#how-to-test-the-place-details-page)
- [How to test the add review functionality](#how-to-test-the-add-review-functionality)
- [Design notes](#design-notes)
- [Notes on CORS](#notes-on-cors)

---

## Project structure

```
part4_shouq/
├── index.html          # List of places + price filter
├── login.html          # Login form
├── place.html          # Place details + reviews + add review form
├── add_review.html     # Standalone add review page
├── styles.css          # All styling (navy theme)
├── scripts.js          # All client logic (tasks 1–4)
├── images/             # Logo, favicon, amenity icons, photography
│
├── app/                # The API (from Part 3)
│   ├── api/v1/         # Endpoints
│   ├── models/         # SQLAlchemy models
│   ├── services/       # Facade
│   └── persistence/    # Repositories
├── config.py           # Development / Testing / Production configs
├── run.py              # API entry point
├── create_admin.py     # Creates the first admin account
├── seed_data.py        # Fills the database with demo data
└── requirements.txt
```

**Where each task lives in `scripts.js`:**

| Task | Functions |
|---|---|
| 1 — Login | `initLogin`, `setCookie`, `getCookie` |
| 2 — List of places | `fetchPlaces`, `buildPlaceCard`, `renderPlaces`, `applyPriceFilter`, `checkAuthentication` |
| 3 — Place details | `initPlaceDetails`, `renderPlaceDetails`, `renderReviews`, `getPlaceIdFromURL`, `showPlaceError` |
| 4 — Add review | `initReviewForm`, `submitReview` |

---

## Running the project

You need **two terminals open at the same time**, both inside `part4_shouq/`.

**1. Install the dependencies (once):**

```bash
python -m pip install -r requirements.txt
```

**2. Terminal one — start the API:**

```bash
python seed_data.py     # fills the database with demo data
python run.py           # starts the API on http://127.0.0.1:5000
```

**3. Terminal two — serve the web client:**

```bash
python -m http.server 8000
```

**4. Open the site:**

```
http://localhost:8000/index.html
```

> The pages must be served over `http://`, not opened as a `file://` path —
> browsers block API requests coming from local files.
> Swagger documentation for the API is available at `http://127.0.0.1:5000/api/v1/`.

---

## Test accounts

`seed_data.py` creates these:

| Email | Password | Role |
|---|---|---|
| `admin@test.com` | `123456` | Administrator |
| `sara@test.com` | `pass1234` | Owns all the demo places |
| `omar@test.com` | `pass1234` | Owns nothing — use this one to post reviews |

> A user cannot review their own place, so log in as **omar** when testing reviews.

---

## How to test the login functionality

**Successful login**

1. Open `http://localhost:8000/login.html`
2. Enter `omar@test.com` / `pass1234` and press **Login**.
3. You are redirected to `index.html`.
4. Confirm the token was stored: press <kbd>F12</kbd> → **Application** → **Cookies** →
   `http://localhost:8000`. You should see a cookie named **`token`** holding the JWT.
5. On the main page the **Login** button is now hidden and a **Logout** button appears
   in its place — this is the behaviour the spec requires.

**Failed login**

1. Go back to `login.html` and enter a wrong password.
2. An error message appears under the form: *"Invalid email or password. Please try again."*
3. No cookie is created and you stay on the page.

**API offline**

1. Stop the API (<kbd>Ctrl</kbd>+<kbd>C</kbd> in terminal one) and try to log in.
2. The form shows *"Could not reach the API. Is the server running?"* instead of failing silently.

**Logout**

- Click **Logout** — the cookie is deleted and the **Login** button comes back.

---

## How to test the list of places and filtering

1. Open `http://localhost:8000/index.html`.
2. Six place cards are loaded **from the API** — each with an image, name, price and a
   **View Details** button.
3. Use the **Max price per night** dropdown:
   - `10` → no places match, the counter reads *"No places match this price."*
   - `50` → only places priced up to $50
   - `100` → places priced up to $100
   - `All` → all six come back
4. Notice the page never reloads — filtering is done in the browser by toggling
   `style.display` on each card.
5. If the API is not running, the page falls back to sample cards and shows a yellow
   notice explaining why, instead of appearing broken.

---

## How to test the place details page

1. From the main page click **View Details** on any card.
2. The URL becomes `place.html?place_id=<id>` and the page shows that place's
   title, host, price, description, amenities and its reviews.
3. **Invalid id:** open `place.html?place_id=does-not-exist` — the page shows
   *"Place not found"* with a link back to the list, rather than stale content.
4. **Not logged in:** the *Add your review* form is hidden.
5. **Logged in:** the form is visible.

---

## How to test the add review functionality

**Posting a review (happy path)**

1. Log in as `omar@test.com` / `pass1234`.
2. Open a place owned by Sara, for example **Seaside Calm Apartment**.
3. Scroll to *Add your review*, or open the standalone page from the
   *"Open the review form"* link.
4. Write a comment, pick a rating, press **Submit review**.
5. A green message appears: *"Thank you! Your review has been added."* and the form clears.
6. Reload the place page — your review is listed. You can also confirm it was stored by
   opening `http://127.0.0.1:5000/api/v1/reviews/` in a browser tab.

**Error cases**

| What you do | What should happen |
|---|---|
| Submit with an empty comment or no rating | *"Please write a review and choose a rating."* |
| Review the **same place twice** | `400` — *"You have already reviewed this place"* |
| Review a place **you own** (log in as `sara@test.com`) | `400` — *"You cannot review your own place"* |
| Open `add_review.html` while logged out | You are redirected to `index.html` |
| Stop the API and submit | *"Could not reach the API. Is the server running?"* |

---

## Design notes

The layout follows the required structure while using a custom palette, which the
task explicitly allows.

**Fixed values required by the specification** — applied to both `.place-card` and
`.review-card`:

```css
margin: 20px;
padding: 10px;
border: 1px solid #ddd;
border-radius: 10px;
```

**Required classes and ids used:**
`logo` · `login-button` · `login-link` · `places-list` · `price-filter` ·
`place-card` · `details-button` · `place-details` · `place-info` · `review-card` ·
`add-review` · `form`

**Free choices made here:** a calm navy palette, the **Poppins** font, hotel
photography for the places, and the official `logo.png`, `icon.png` and the
`icon_wifi` / `icon_bed` / `icon_bath` amenity icons from the provided base files.

All four pages pass the [W3C validator](https://validator.w3.org/) with no errors.

---

## Notes on CORS

The browser blocks requests from `localhost:8000` to `127.0.0.1:5000` unless the API
allows it. This is already handled in `app/__init__.py`:

```python
from flask_cors import CORS

CORS(app, resources={r"/api/*": {"origins": "*"}})
```

If you ever see a `CORS policy` error in the browser console, it means the API is
running without this configuration.
