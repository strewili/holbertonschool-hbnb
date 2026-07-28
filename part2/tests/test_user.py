import unittest
from app.models.user import User


class TestUser(unittest.TestCase):

    def test_create_user(self):
        user = User(
            first_name="Jana",
            last_name="Alhazmi",
            email="jana@test.com"
        )

        self.assertEqual(user.first_name, "Jana")
        self.assertEqual(user.last_name, "Alhazmi")
        self.assertEqual(user.email, "jana@test.com")


if __name__ == "__main__":
    unittest.main()
