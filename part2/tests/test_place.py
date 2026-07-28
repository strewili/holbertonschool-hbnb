import unittest
from app.models.user import User
from app.models.place import Place

class TestPlace(unittest.TestCase):

    def setUp(self):
        self.user = User(
            "Jana",
            "Alhazmi",
            "jana@test.com"
        )

    def test_create_place(self):
        place = Place(
            "House",
            "Nice house",
            500,
            24.7,
            46.7,
            self.user
        )

        self.assertEqual(place.title, "House")

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            Place(
                "House",
                "",
                -5,
                24.7,
                46.7,
                self.user
            )

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Place(
                "House",
                "",
                100,
                100,
                46.7,
                self.user
            )

    def test_invalid_owner(self):
        with self.assertRaises(ValueError):
            Place(
                "House",
                "",
                100,
                24.7,
                46.7,
                "jana"
            )

if __name__ == "__main__":
    unittest.main()
