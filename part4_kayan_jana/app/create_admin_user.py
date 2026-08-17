#!/usr/bin/python3
"""
One-off script: create an admin user directly in the database,
bypassing the admin-protected POST /api/v1/users/ endpoint.

Run this from your project root (part4_kayan_jana/), e.g.:

    python3 -m app.create_admin_user

(place this file inside app/ first)
"""
from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    email = "admin@test.com"
    password = "adminpass123"

    existing = User.query.filter_by(email=email).first()
    if existing:
        print(f"User already exists: {email}")
    else:
        user = User(
            first_name="Admin",
            last_name="User",
            email=email,
            password=password,
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        print(f"Created admin user: {email} / {password}")