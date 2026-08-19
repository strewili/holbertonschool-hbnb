#!/usr/bin/python3
"""
One-off script: create a test user directly in the database.

Run this from your project root (part4_kayan_jana/), e.g.:

    python3 -m app.create_test_user

or, if you place it inside app/, adjust the import path accordingly.
"""
from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    email = "test@test.com"
    password = "testpass123"

    existing = User.query.filter_by(email=email).first()
    if existing:
        print(f"User already exists: {email}")
    else:
        user = User(
            first_name="Test",
            last_name="User",
            email=email,
            password=password,
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        print(f"Created user: {email} / {password}")