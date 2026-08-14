from app import create_app
from app.services import facade

app = create_app()

with app.app_context():
    admin = facade.get_user_by_email("admin@test.com")

    if not admin:
        admin = facade.create_user({
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@test.com",
            "password": "123456"
        })

    admin.is_admin = True

    facade.update_user(
        admin.id,
        {"is_admin": True}
    )

    print("Admin created")
    print(admin.email)
    print(admin.is_admin)
