import unittest
from app.persistence.repository import InMemoryRepository
from app.models.user import User

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryRepository()

        self.user = User(
            "Jana",
            "Alhazmi",
            "jana@test.com"
        )

    def test_add(self):
        self.repo.add(self.user)
        self.assertEqual(
            self.repo.get(self.user.id),
            self.user
        )

    def test_get_all(self):
        self.repo.add(self.user)
        self.assertEqual(len(self.repo.get_all()), 1)

    def test_update(self):
        self.repo.add(self.user)

        self.repo.update(
            self.user.id,
            {"first_name": "Sara"}
        )

        self.assertEqual(
            self.repo.get(self.user.id).first_name,
            "Sara"
        )

    def test_delete(self):
        self.repo.add(self.user)
        self.repo.delete(self.user.id)

        self.assertIsNone(
            self.repo.get(self.user.id)
        )

if __name__ == "__main__":
    unittest.main()
