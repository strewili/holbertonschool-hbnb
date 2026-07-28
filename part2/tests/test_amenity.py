import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):

    def test_create_amenity(self):
        amenity = Amenity("WiFi")
        self.assertEqual(amenity.name, "WiFi")

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Amenity("")

    def test_long_name(self):
        with self.assertRaises(ValueError):
            Amenity("A" * 51)

if __name__ == "__main__":
    unittest.main()
