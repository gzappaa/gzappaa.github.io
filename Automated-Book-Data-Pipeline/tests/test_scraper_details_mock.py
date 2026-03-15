import unittest
from unittest.mock import patch, Mock
from src.scraper import get_book_details

BOOK_DETAIL_HTML_PATH = "tests/data/book_detail.html"

class TestBookDetailsMock(unittest.TestCase):

    def setUp(self):
        # Patch requests.get inside setUp
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            with open(BOOK_DETAIL_HTML_PATH, "r", encoding="utf-8") as f:
                mock_response.text = f.read()
            mock_get.return_value = mock_response

            # Call get_book_details with any fake URL (mocked)
            self.details = get_book_details("fake_url")
            self.table = self.details["table_data"]

    def test_table_fields_exist(self):
        # Ensure all expected table fields are present
        self.assertIn("UPC", self.table)
        self.assertIn("Product Type", self.table)
        self.assertIn("Price (excl. tax)", self.table)
        self.assertIn("Price (incl. tax)", self.table)
        self.assertIn("Tax", self.table)
        self.assertIn("Availability", self.table)
        self.assertIn("Number of reviews", self.table)

    def test_types(self):
        # Ensure all table fields have correct types
        self.assertIsInstance(self.table["UPC"], str)
        self.assertIsInstance(self.table["Product Type"], str)
        self.assertIsInstance(self.table["Price (excl. tax)"], float)
        self.assertIsInstance(self.table["Price (incl. tax)"], float)
        self.assertIsInstance(self.table["Tax"], float)
        self.assertIsInstance(self.table["Availability"], str)
        self.assertIsInstance(self.table["Number of reviews"], int)


if __name__ == "__main__":
    unittest.main()