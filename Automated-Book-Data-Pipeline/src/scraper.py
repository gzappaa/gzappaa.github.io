import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from urllib.parse import urljoin
import time
import concurrent.futures
from threading import Lock
from .parser import BookParser

BASE_URL = "https://books.toscrape.com/"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds between retries

# Lock for thread-safe progress printing
progress_lock = Lock()

# Return BeautifulSoup object from URL with retries and UTF-8 encoding.
def get_soup(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            res = requests.get(url, timeout=30)
            res.raise_for_status()
            res.encoding = 'utf-8'
            return BeautifulSoup(res.text, "html.parser")
        except (requests.Timeout, requests.ConnectionError) as e:
            print(f"Attempt {attempt}/{MAX_RETRIES} failed for {url}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                print(f"Failed to fetch {url} after {MAX_RETRIES} attempts.")
                return None
        except requests.HTTPError as e:
            print(f"HTTP error for {url}: {e}")
            return None

# Scrape book details including description, availability, table data, and category from breadcrumb.
def get_book_details(book_url):
    soup = get_soup(book_url)
    if soup is None:
        print(f"Skipping {book_url}")
        return {}

    description = BookParser.parse_description(soup)
    availability_text = BookParser.parse_availability(soup)
    table = soup.find("table", class_="table table-striped")
    table_data = BookParser.parse_table(table)

    breadcrumb_links = soup.select("ul.breadcrumb li a")
    category = breadcrumb_links[2].text.strip() if len(breadcrumb_links) > 2 else "Unknown"

    return {
        "description": description,
        "availability": availability_text,
        "table_data": table_data,
        "category": category
    }

# Scrape all books from paginated pages with thread-safe progress prints
def get_all_books():
    all_books = []
    total_pages = 50
    milestones = {0.25, 0.5, 0.75}

    milestones_lock = Lock()

    def process_page(page_num):
        url = BASE_URL if page_num == 1 else urljoin(BASE_URL, f"catalogue/page-{page_num}.html")
        soup = get_soup(url)
        if soup is None:
            print(f"Page {page_num} failed to load.")
            return []

        books_html = soup.find_all("article", class_="product_pod")
        page_books = [BookParser.parse_book(b) for b in books_html]

        # Thread-safe progress printing
        progress = page_num / total_pages
        with milestones_lock:
            for m in sorted(milestones):
                if progress >= m:
                    print(f"Progress: {int(m*100)}%")
                    milestones.remove(m)
                    break

        return page_books

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(process_page, range(1, total_pages + 1))

    for page_books in results:
        all_books.extend(page_books)

    print(f"Total books collected: {len(all_books)}")
    return all_books

# Fetch detailed info for each book using multithreading with progress tracking
def get_book_list_with_details(books):
    total_books = len(books)
    book_counter = 0
    counter_lock = Lock()

    def fetch_details(book):
        nonlocal book_counter
        details = get_book_details(book["book_url"])
        book.update(details)
        with counter_lock:
            book_counter += 1
            if book_counter % 50 == 0:
                print(f"Book {book_counter}/{total_books} processed")
        return book

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        books_with_details = list(executor.map(fetch_details, books))

    print(f"All {total_books} books with details processed.")
    return books_with_details


if __name__ == "__main__":
    # Step 1: Scrape all books
    books = get_all_books()
    Path("data").mkdir(exist_ok=True)
    with open("data/books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)
    print(f"{len(books)} books saved to data/books.json")

    # Step 2: Fetch detailed info
    books_with_details = get_book_list_with_details(books)
    with open("data/books_raw.json", "w", encoding="utf-8") as f:
        json.dump(books_with_details, f, ensure_ascii=False, indent=4)
    print(f"{len(books_with_details)} books with details saved to data/books_raw.json")