# main.py
"""
Main pipeline for 'books.toscrape.com' project.
This script orchestrates the entire workflow:
1. Scrape categories URLs
2. Scrape all books
3. Scrape detailed info for each book
4. Save raw JSON data
5. Clean and normalize data
6. Download book cover images
7. Calculate analytics
8. Generate PDF and Excel reports
"""

from pathlib import Path
import json

# Relative imports from project modules
from .categorized import scrape_categories_urls
from .scraper import get_all_books, get_book_list_with_details
from .clean import clean_books_data
from .cover_downloader import download_images
from .analytics import calculate_complete_analytics
from .report import generate_reports

def main():
    # Step 1: Scrape categories URLs (for testing & future analysis)
    print("Scraping categories URLs...")
    scrape_categories_urls()
    
    # Step 2: Scrape all books (basic info)
    print("\nScraping all books...")
    books = get_all_books()
    
    Path("data").mkdir(exist_ok=True)
    basic_json_path = Path("data/books.json")
    with open(basic_json_path, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)
    print(f"{len(books)} books saved to {basic_json_path}")
    
    # Step 3: Scrape detailed info for each book
    print("\nFetching detailed book information...")
    books_with_details = get_book_list_with_details(books)
    
    raw_json_path = Path("data/books_raw.json")
    with open(raw_json_path, "w", encoding="utf-8") as f:
        json.dump(books_with_details, f, ensure_ascii=False, indent=4)
    print(f"{len(books_with_details)} books with details saved to {raw_json_path}")
    
    # Step 4: Clean and normalize the books JSON
    print("\nCleaning and normalizing data...")
    clean_json_path = Path("data/books_processed.json")
    clean_books_data(input_file=raw_json_path, output_file=clean_json_path)
    
    # Step 5: Calculate analytics
    print("\nCalculating analytics...")
    stats = calculate_complete_analytics(filepath=clean_json_path)
    
    # Step 6: Generate PDF and Excel reports
    print("\nGenerating reports...")
    generate_reports(stats, pdf_path="data/book_report.pdf", excel_path="data/book_report.xlsx")

    # Step 7: Download book cover images
    print("\nDownloading book cover images...")
    download_images(books_with_details, folder="data/images", max_workers=8)
    
    print("\nPipeline completed successfully!")

if __name__ == "__main__":
    main()