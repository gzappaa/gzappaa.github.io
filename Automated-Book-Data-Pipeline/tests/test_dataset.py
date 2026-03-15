import unittest
import json
from pathlib import Path
from urllib.parse import urlparse
from re import sub
import os

# --------------------------------------------------------------------------------------------------
# THIS TEST DEPENDS ON LOCALLY GENERATED FILES
# --------------------------------------------------------------------------------------------------
# This test checks the final books JSON, images, and categories.
# It should NOT run in CI/GitHub Actions because it depends on data that only exists after local generation.
# Therefore, we use @unittest.skipIf(os.getenv("CI") == "true"):
# - Locally: the test runs normally
# - CI/GitHub Actions: the test is skipped
# --------------------------------------------------------------------------------------------------



def normalize_category(name):
    return name.strip().lower()

@unittest.skipIf(os.getenv("CI") == "true", "Skip dataset test on CI")
class TestBooksJSON(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load detailed books JSON
        json_path = Path("data/books_raw.json")
        with json_path.open("r", encoding="utf-8") as f:
            cls.books = json.load(f)

        # Load category JSON
        with Path("data/books_by_category.json").open("r", encoding="utf-8") as f:
            cls.books_by_category = json.load(f)

        # Images folder
        cls.images_folder = Path("data/images")
    
    def test_all_books_have_required_fields(self):
        # All books should have title, table_data with UPC, and a non-empty UPC
        for book in self.books:
            with self.subTest(book=book.get("title", "No title")):
                self.assertIn("title", book)
                self.assertIn("table_data", book)
                self.assertIn("UPC", book["table_data"])
                self.assertTrue(book["table_data"]["UPC"], "UPC cannot be empty")

    def test_no_duplicate_upc(self):
        # All UPCs should be unique
        upcs = [b["table_data"]["UPC"] for b in self.books if "table_data" in b and "UPC" in b["table_data"]]
        self.assertEqual(len(upcs), len(set(upcs)), "Duplicate UPCs found")

    def test_image_url_valid(self):
        # All books should have a valid image URL
        for book in self.books:
            with self.subTest(book=book.get("title", "No title")):
                self.assertIn("image_url", book)
                url = book["image_url"]
                parsed = urlparse(url)
                self.assertTrue(parsed.scheme in ("http", "https"), f"Invalid URL: {url}")

    def test_images_folder_has_all_files(self):
        # Count all .jpg files in images folder
        jpg_files = list(self.images_folder.glob("*.jpg"))
        expected_count = len(self.books)
        self.assertEqual(len(jpg_files), expected_count,
                        f"Expected {expected_count} images, found {len(jpg_files)}")

    def test_image_file_exists(self):
        # All books should have an image file saved with the correct filename pattern
        for book in self.books:
            with self.subTest(book=book.get("title", "No title")):
                upc = book["table_data"]["UPC"]
                # Filename pattern: UPC + safe title
                safe_title = sub(r'[<>:"/\\|?*]', '_', book['title']).strip().lower()
                safe_title = sub(r'[\s_]+', '_', safe_title)
                filename = f"{upc}_{safe_title}.jpg"
                filepath = self.images_folder / filename
                self.assertTrue(filepath.exists(), f"Image file missing: {filename}")

    def test_price_positive(self):
        # All books should have a non-negative price
        for book in self.books:
            with self.subTest(book=book.get("title", "No title")):
                price = book.get("price")
                self.assertIsInstance(price, (int, float), "Price must be a number")
                self.assertGreaterEqual(price, 0, "Negative price found")

    def test_all_books_have_category(self):
        # All books should have a non-empty category field
        for book in self.books:
            with self.subTest(book=book.get("title", "No title")):
                self.assertIn("category", book, "Category field missing")
                self.assertTrue(book["category"], "Category cannot be empty")

    def test_category_counts_match(self):
        # group counts from detailed JSON by normalized category
        counts_detailed = {}
        for book in self.books:
            cat = book.get("category")
            if cat:
                cat_norm = normalize_category(cat)
                counts_detailed[cat_norm] = counts_detailed.get(cat_norm, 0) + 1

        # compare counts with simple JSON (also normalize key)
        for category, urls in self.books_by_category.items():
            with self.subTest(category=category):
                cat_norm = normalize_category(category)
                count_detailed = counts_detailed.get(cat_norm, 0)
                self.assertEqual(len(urls), count_detailed,
                                 f"Mismatch in count for category '{category}': "
                                 f"{len(urls)} in simple JSON vs {count_detailed} in detailed JSON")

    def test_category_urls_match(self):
        # group URLs from detailed JSON by normalized category
        urls_detailed = {}
        for book in self.books:
            cat = book.get("category")
            url = book.get("book_url")
            if cat and url:
                cat_norm = normalize_category(cat)
                urls_detailed.setdefault(cat_norm, []).append(url)

        # compare URLs for each category
        for category, urls_simple in self.books_by_category.items():
            with self.subTest(category=category):
                cat_norm = normalize_category(category)
                detailed_urls = urls_detailed.get(cat_norm, [])
                missing_urls = [url for url in detailed_urls if url not in urls_simple]
                self.assertFalse(missing_urls,
                                 f"Missing URLs in simple JSON for category '{category}': {missing_urls}")
    
    
    def test_book_report_pdf_exists(self):
        """Check that the book_report.pdf exists in the data folder"""
        pdf_path = Path("data/book_report.pdf")
        self.assertTrue(pdf_path.exists(), f"book_report.pdf not found at {pdf_path}")


    def test_book_report_excel_exists(self):
        """Check that the book_report.xlsx exists in the data folder"""
        excel_path = Path("data/book_report.xlsx")
        self.assertTrue(excel_path.exists(), f"book_report.xlsx not found at {excel_path}")





if __name__ == "__main__":
    unittest.main()