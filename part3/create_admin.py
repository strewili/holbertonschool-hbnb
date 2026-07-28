from app import create_app
from app.services import facade

app = create_app()

with app.app_context():
    admin = facade.create_user({
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@test.com",
        "password": "123456"
    })

    admin.is_admin = True

    print("Admin created")
    print(admin.email)
    print(admin.is_admin)


