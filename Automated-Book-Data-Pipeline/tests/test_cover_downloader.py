import unittest
from pathlib import Path
from shutil import rmtree
from urllib.parse import urljoin
from src.scraper import get_soup, get_book_details
from src.cover_downloader import download_images, safe_filename

class TestCoverDownloaderReal(unittest.TestCase):

    def setUp(self):
        # Folder for test images
        self.test_folder = Path("data/test_images_real")
        # Remove it if it exists (cleanup from previous runs)
        if self.test_folder.exists():
            rmtree(self.test_folder)
        self.test_folder.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        # Cleanup after test
        if self.test_folder.exists():
            rmtree(self.test_folder)

    def test_download_two_real_images(self):
        # Step 1: Get first page books only
        soup = get_soup("https://books.toscrape.com/")
        articles = soup.find_all("article", class_="product_pod")

        test_books = []
        for article in articles:
            book_url = article.h3.a["href"]
            if not book_url.startswith("http"):
                book_url = urljoin("https://books.toscrape.com/", book_url)

            details = get_book_details(book_url)
            if details.get("table_data", {}).get("UPC"):
                book_data = {
                    "title": article.h3.a.text.strip(),
                    "image_url": urljoin("https://books.toscrape.com/", article.find("img")["src"]),
                    "table_data": details["table_data"]
                }
                test_books.append(book_data)

            if len(test_books) == 2:  # Stop after 2 books
                break

        # Step 2: Download the images
        download_images(test_books, folder=self.test_folder, max_workers=2)

        # Step 3: Assert files exist
        for book in test_books:
            upc = book["table_data"]["UPC"]
            safe_title = safe_filename(book["title"])
            filepath = self.test_folder / f"{upc}_{safe_title}.jpg"
            self.assertTrue(filepath.exists(), f"File not found: {filepath}")

if __name__ == "__main__":
    unittest.main()