from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.extensions import db


class UserRepository(SQLAlchemyRepository):
    """Repository for User-specific database operations."""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        return self.get_by_attribute("email", email)

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        data = data.copy()

        if "password" in data:
            obj.hash_password(data.pop("password"))

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        db.session.commit()
        return obj
