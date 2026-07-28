import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

class TestReview(unittest.TestCase):

    def setUp(self):
        self.user = User(
            "Jana",
            "Alhazmi",
            "jana@test.com"
        )

        self.place = Place(
            "House",
            "",
            100,
            24.7,
            46.7,
            self.user
        )

    def test_create_review(self):
        review = Review(
            "Excellent",
            5,
            self.place,
            self.user
        )

        self.assertEqual(review.rating, 5)

    def test_invalid_rating(self):
        with self.assertRaises(ValueError):
            Review(
                "Bad",
                6,
                self.place,
                self.user
            )

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            Review(
                "",
                5,
                self.place,
                self.user
            )

if __name__ == "__main__":
    unittest.main()
