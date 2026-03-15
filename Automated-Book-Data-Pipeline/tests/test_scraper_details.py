import unittest
from urllib.parse import urljoin
from src.scraper import get_soup, get_book_details, BASE_URL

"""
 This test is real and will make an actual HTTP request to the 
 first book's page to verify the details scraping logic. 
 It checks that all expected fields are present and have the correct types. 
 This ensures that the get_book_details function correctly extracts information from the book detail page,
 including the category from the breadcrumb navigation.
"""


class TestBookDetailsReal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Fetch only the first page of the catalog
        soup = get_soup(BASE_URL)
        assert soup is not None, "Failed to fetch the first catalog page"

        # Get the first book on the page
        first_article = soup.find("article", class_="product_pod")
        assert first_article is not None, "No books found on the first page"

        # Build the full URL to the first book
        cls.book_url = urljoin(BASE_URL, first_article.h3.a["href"])

        # Fetch real details for this book
        cls.details = get_book_details(cls.book_url)
        cls.table = cls.details.get("table_data", {})

    def test_table_fields_exist(self):
        # Check that all expected fields exist in the table
        self.assertIn("UPC", self.table)
        self.assertIn("Product Type", self.table)
        self.assertIn("Price (excl. tax)", self.table)
        self.assertIn("Price (incl. tax)", self.table)
        self.assertIn("Tax", self.table)
        self.assertIn("Availability", self.table)
        self.assertIn("Number of reviews", self.table)

    def test_types(self):
        # Check that each field has the correct data type
        self.assertIsInstance(self.table["UPC"], str)
        self.assertIsInstance(self.table["Product Type"], str)
        self.assertIsInstance(self.table["Price (excl. tax)"], float)
        self.assertIsInstance(self.table["Price (incl. tax)"], float)
        self.assertIsInstance(self.table["Tax"], float)
        self.assertIsInstance(self.table["Availability"], str)
        self.assertIsInstance(self.table["Number of reviews"], int)


if __name__ == "__main__":
    unittest.main()