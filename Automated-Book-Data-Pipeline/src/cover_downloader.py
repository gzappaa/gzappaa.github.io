from pathlib import Path
import requests
import re
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import json
import time

# ------------------------------
# Safe filename generator
# ------------------------------
def safe_filename(title: str) -> str:
    filename = re.sub(r'[<>:"/\\|?*]', '_', title)
    filename = re.sub(r'[\s_]+', '_', filename.strip().lower())
    return filename

# ------------------------------
# Download a single image
# ------------------------------
def download_image(book, folder, downloaded_upcs, lock, max_retries=3):
    upc = book.get("table_data", {}).get("UPC")
    url = book.get("image_url")

    if not upc:
        return f"Missing UPC for: {book.get('title', 'No title')}"
    if not url:
        return f"No image URL for: {book.get('title', 'No title')}"

    filename = f"{upc}_{safe_filename(book['title'])}.jpg"
    filepath = folder / filename

    # Thread-safe check for already downloaded UPC
    with lock:
        if upc in downloaded_upcs:
            return f"Skipped duplicate UPC: {book['title']}"
        downloaded_upcs.add(upc)

    if filepath.exists():
        return f"Already exists: {filename}"

    # Retry mechanism
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            filepath.write_bytes(resp.content)
            return f"Downloaded: {filename}"
        except requests.RequestException as e:
            if attempt < max_retries:
                time.sleep(1)  # brief pause before retry
                continue
            return f"Error downloading {filename} after {max_retries} attempts: {e}"

# ------------------------------
# Download all images
# ------------------------------
def download_images(books, folder="data/images", max_workers=30):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    downloaded_upcs = set()
    lock = Lock()

    downloaded, skipped, errors = 0, 0, 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(lambda b: download_image(b, folder, downloaded_upcs, lock), books)
        for r in results:
            print(r)
            if r.startswith("Downloaded"):
                downloaded += 1
            elif r.startswith("Skipped") or r.startswith("Already exists"):
                skipped += 1
            else:
                errors += 1

    print("\n=== Download Summary ===")
    print(f"Downloaded: {downloaded}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print("========================\n")

# ------------------------------
# Run as script
# ------------------------------
if __name__ == "__main__":
    books_json_path = Path("data/books_raw.json")
    if not books_json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {books_json_path}")

    with books_json_path.open("r", encoding="utf-8") as f:
        books = json.load(f)

    download_images(books, folder="data/images", max_workers=8)