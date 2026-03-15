import unittest
from unittest.mock import patch
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.scraper import get_all_books, BASE_URL

# Path to the catalogue HTML used for testing
CATALOGUE_HTML_PATH = "tests/data/catalogue.html"

class TestBookScraperMock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the test catalogue HTML once for all tests
        with open(CATALOGUE_HTML_PATH, "r", encoding="utf-8") as f:
            cls.catalogue_html = f.read()

    @patch("src.scraper.get_soup")
    def test_books_list_not_empty(self, mock_get_soup):
        """Test that get_all_books returns a non-empty list"""
        mock_get_soup.return_value = BeautifulSoup(self.catalogue_html, "html.parser")
        book_list = get_all_books()
        self.assertTrue(len(book_list) > 0, "Book list should not be empty")

    @patch("src.scraper.get_soup")
    def test_books_fields_exist(self, mock_get_soup):
        """Test that each book has all required fields"""
        mock_get_soup.return_value = BeautifulSoup(self.catalogue_html, "html.parser")
        book_list = get_all_books()
        for book in book_list:
            self.assertIn("title", book)
            self.assertIn("price", book)
            self.assertIn("rating", book)
            self.assertIn("image_url", book)

    @patch("src.scraper.get_soup")
    def test_books_field_types(self, mock_get_soup):
        """Test that each book field has the correct data type"""
        mock_get_soup.return_value = BeautifulSoup(self.catalogue_html, "html.parser")
        book_list = get_all_books()
        for book in book_list:
            self.assertIsInstance(book["title"], str)
            self.assertIsInstance(book["price"], float)
            self.assertIsInstance(book["rating"], int)
            self.assertIsInstance(book["image_url"], str)

    @patch("src.scraper.get_soup")
    def test_books_urls(self, mock_get_soup):
        """Test that each book has a valid book_url"""
        mock_get_soup.return_value = BeautifulSoup(self.catalogue_html, "html.parser")
        book_list = get_all_books()

        # Build book URLs from HTML
        soup = mock_get_soup.return_value
        book_articles = soup.find_all("article", class_="product_pod")
        for book, article in zip(book_list, book_articles):
            relative_url = article.h3.a["href"]
            book["book_url"] = urljoin(BASE_URL + "catalogue/", relative_url)

        # Check URLs
        for book in book_list:
            self.assertIn("book_url", book)
            self.assertTrue(book["book_url"].startswith("http"), f"Invalid URL: {book['book_url']}")

if __name__ == "__main__":
    unittest.main()