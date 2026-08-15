#!/usr/bin/python3
"""Populate the development database with demo data.

Creates an admin, two regular users, six places, amenities and a few
reviews so the web client has something to show.

Usage (from the part4_shouq folder):
    python seed_data.py
"""

from app import create_app
from app.extensions import db
from app.services import facade

app = create_app("config.DevelopmentConfig")

USERS = [
    ("Admin", "User", "admin@test.com", "123456", True),
    ("Sara", "Alqahtani", "sara@test.com", "pass1234", False),
    ("Omar", "Alharbi", "omar@test.com", "pass1234", False),
]

AMENITIES = ["WiFi", "Air Conditioning", "Swimming Pool",
             "Kitchen", "Free parking", "Sea view"]

PLACES = [
    ("Seaside Calm Apartment", "Quiet apartment steps from the shore, with wide windows facing the water.", 200, 21.4858, 39.1925),
    ("Blue Hour Studio", "Bright studio with a proper desk for slow mornings and remote work.", 120, 24.7136, 46.6753),
    ("Golden Hills Retreat", "Mountain retreat with a fireplace and a small garden.", 85, 18.2164, 42.5053),
    ("Dusk House", "Peaceful house with a terrace that catches the evening light.", 150, 21.2703, 40.4158),
    ("Still Water Lodge", "Lakeside lodge with a private pool and long quiet evenings.", 240, 26.6084, 37.9216),
    ("Morning Mist Cottage", "Small cottage with a balcony over the valley.", 70, 20.0129, 41.4677),
]

REVIEWS = [
    (0, "Exactly as described — calm, clean, and the sea view in the morning is unreal.", 5),
    (1, "Worked remotely for a week from here. The desk and the quiet made it easy.", 5),
    (2, "Lovely place and a great location. The lift was slow, but the balcony made up for it.", 4),
]


with app.app_context():
    db.create_all()

    # ---- users ----
    users = {}
    for first, last, email, password, is_admin in USERS:
        user = facade.get_user_by_email(email)
        if not user:
            user = facade.create_user({
                "first_name": first, "last_name": last,
                "email": email, "password": password
            })
            if is_admin:
                facade.update_user(user.id, {"is_admin": True})
        users[email] = user
    print(f"users     : {len(users)}")

    # ---- amenities ----
    existing = {a.name for a in facade.get_all_amenities()}
    for name in AMENITIES:
        if name not in existing:
            facade.create_amenity({"name": name})
    amenity_ids = [a.id for a in facade.get_all_amenities()]
    print(f"amenities : {len(amenity_ids)}")

    # ---- places (owned by Sara) ----
    owner = users["sara@test.com"]
    have = {p.title for p in facade.get_all_places()}
    created = []
    for title, desc, price, lat, lon in PLACES:
        if title in have:
            continue
        place = facade.create_place({
            "title": title, "description": desc, "price": price,
            "latitude": lat, "longitude": lon,
            "owner_id": owner.id,
            "amenities": amenity_ids[:3],
        })
        created.append(place)
    print(f"places    : {len(facade.get_all_places())}")

    # ---- reviews (written by Omar, who owns nothing) ----
    reviewer = users["omar@test.com"]
    places = facade.get_all_places()
    added = 0
    for index, text, rating in REVIEWS:
        if index >= len(places):
            continue
        try:
            facade.create_review({
                "text": text, "rating": rating,
                "place_id": places[index].id,
                "user_id": reviewer.id,
            })
            added += 1
        except ValueError:
            pass          # already reviewed / owner of the place
    print(f"reviews   : {len(facade.get_all_reviews())}")

    print("\nDone. Log in with:")
    print("  admin@test.com / 123456   (admin)")
    print("  sara@test.com  / pass1234 (owns the places)")
    print("  omar@test.com  / pass1234 (can post reviews)")
