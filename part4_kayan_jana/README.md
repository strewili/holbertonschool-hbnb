# HBnB - Simple Web Client

## Project Overview

This project is the front-end web client for the HBnB application.

The application provides a simple interface for users to browse available places, view place details, log in, and add reviews.

The front-end communicates with the HBnB REST API developed in the previous project parts.

---

## Features

### Home Page

- Displays available places.
- Shows the place title and price per night.
- Allows users to filter places based on price.
- Provides a button to view place details.

### Login

- Users can log in using their email and password.
- Authentication is handled using JWT tokens.
- The token is stored in a browser cookie.

### Place Details

Each place page displays:

- Host name
- Price per night
- Description
- Amenities
- Reviews
- Add Review button

### Reviews

Authenticated users can:

- View reviews for a place.
- Add a review.
- Select a rating from 1 to 5.
- Submit a review for a place.

Administrators cannot create reviews.

Users cannot submit more than one review for the same place.

---

## Technologies Used

- HTML5
- CSS3
- JavaScript
- Python
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- SQLite
- Git & GitHub

---

## Project Structure

```text
part4_kayan_jana/
│
├── index.html
├── index.js
├── place.html
├── place.js
├── login.html
├── add_review.html
├── add_review.js
├── scripts.js
├── styles.css
├── styles2.css
│
├── images/
│   ├── hotel1.jpg
│   ├── hotel2.jpg
│   ├── hotel3.jpg
│   ├── icon.png
│   ├── icon_bath.png
│   ├── icon_bed.png
│   ├── icon_wifi.png
│   └── logo.png
│
└── app/
    ├── api/
    ├── models/
    ├── persistence/
    ├── services/
    ├── config.py
    ├── extensions.py
    └── run.py

API Endpoints Used
Places
GET /api/v1/places/
GET /api/v1/places/<place_id>
Authentication
POST /api/v1/auth/login
Reviews
GET /api/v1/reviews/
POST /api/v1/reviews/
GET /api/v1/reviews/<review_id>
PUT /api/v1/reviews/<review_id>
DELETE /api/v1/reviews/<review_id>



Demo Accounts
Role	Email	Password
Test User	test@test.com	testpass123
Regular User	regular@test.com	userpass123
Admin	admin@test.com	adminpass123

Note: Administrators are not allowed to create reviews.


Running the Application
1. Start the Flask API

Open a terminal and run:

cd ~/holbertonschool-hbnb/part4_kayan_jana
python3 -m app.run

The API will run on:

http://127.0.0.1:5000
2. Start the Web Client

Open another terminal:

cd ~/holbertonschool-hbnb/part4_kayan_jana
python3 -m http.server 8001

Then open:

http://127.0.0.1:8001/index.html

Testing

The application was tested using:

Browser developer tools
JavaScript Fetch API
Flask API endpoints
SQLite database
Different user roles
Review Testing

Regular users can create reviews:

POST /api/v1/reviews/

Administrators receive:

403 Forbidden

when attempting to create a review.

Users also receive an error if they attempt to review the same place more than once.

Authentication

JWT authentication is used to protect authenticated actions.

The JWT token is stored in a browser cookie and sent with API requests using:

Authorization: Bearer <token>
Authors

HBnB Project - Part 4

Student: Kayan-Jana
