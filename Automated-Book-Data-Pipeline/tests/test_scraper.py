import unittest
from src.scraper import get_all_books, get_soup, BASE_URL

class TestGetAllBooksReal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Fetch all 50 pages of the catalog (real scraping)
        cls.book_list = get_all_books()  # ~50 requests, only basic book info

    def test_books_not_empty(self):
        # Ensure the scraper collected books
        self.assertTrue(len(self.book_list) > 0, "Book list is empty")

    def test_catalogue_size(self):
        # There should be roughly 1000 books (50 pages × 20 books per page)
        self.assertEqual(len(self.book_list), 50 * 20, "Total book count mismatch")

    def test_book_fields_exist(self):
        # Each book should have the required fields
        for book in self.book_list:
            self.assertIn("title", book)
            self.assertIn("price", book)
            self.assertIn("rating", book)
            self.assertIn("image_url", book)
            self.assertIn("book_url", book)

    def test_fields_types(self):
        # Check that each field has the correct type
        for book in self.book_list:
            self.assertIsInstance(book["title"], str)
            self.assertIsInstance(book["price"], float)
            self.assertIsInstance(book["rating"], int)
            self.assertIsInstance(book["image_url"], str)
            self.assertIsInstance(book["book_url"], str)

    def test_book_urls_format(self):
        # Each book URL should start with http(s)
        for book in self.book_list:
            self.assertTrue(book["book_url"].startswith("http"), f"Invalid URL: {book['book_url']}")

    def test_get_soup(self):
        # Check that get_soup returns a BeautifulSoup object
        soup = get_soup(BASE_URL)
        self.assertEqual(soup.__class__.__name__, "BeautifulSoup")


if __name__ == "__main__":
    unittest.main()