from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User


class UserRepository(SQLAlchemyRepository):
    """Repository for User-specific database operations."""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        return self.get_by_attribute("email", email)
