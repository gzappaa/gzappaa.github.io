# Automated Book Data Pipeline

## Overview
This project is a modular, reproducible, and testable pipeline for scraping, processing, and analyzing book data from [Books to Scrape](https://books.toscrape.com/). It collects book information, cleans and analyzes the data, downloads cover images, and generates detailed PDF and Excel reports.

---

## Pipeline Modules

1. **Scraper (`scraper.py`)**  
   - Scrapes all books from the website, collecting basic info from paginated pages.  
   - Fetches detailed info for each book (description, availability, table data, category) using multithreading and retries.  
   - Uses `parser.py` for HTML parsing logic.  
   - Saves results to JSON files for further processing.

2. **Parser (`parser.py`)**  
   - Contains reusable parsing logic for catalog and book pages.  
   - Used internally by `scraper.py` to extract structured book data.

3. **Data Cleaning (`clean.py`)**  
   - Cleans raw JSON data (`books_raw.json`).  
   - Normalizes categories, extracts availability numbers, and fills missing fields.  
   - Saves the cleaned dataset as `books_processed.json`.

4. **Categorization (`categorized.py`)**  
   - Collects book URLs by category and saves them in a JSON file (`books_by_category.json`).  
   - Helps testing and analyzing books by category.

5. **Cover Downloader (`cover_downloader.py`)**  
   - Downloads book cover images into a local folder.  
   - Ensures safe filenames and avoids duplicates using UPC codes.  
   - Uses multithreading and retry logic for speed and reliability.

6. **Analytics (`analytics.py`)**  
   - Computes full analytics from `books_processed.json`.  
   - Calculates totals, averages, min/max prices, and per-category stats.  
   - Returns a structured dictionary with all results.

7. **Reporting (`report.py`)**  
   - Generates PDF and Excel reports from analytics.  
   - PDF includes summary stats, most expensive and cheapest books, and a complete book list.  
   - Excel contains multiple sheets: All Books, Category Summary, Top 20 Expensive, Top 5 per Category.

---

## Workflow Summary

The full pipeline orchestrated by `main.py`:

   scrape books (basic info) -> fetch detailed book info -> clean data -> download covers -> generate reports

### Info
Note: Prices are numeric values only (no € symbol), but all amounts are in euros.

## Features

- Scraper
- Parser
- Analytics
- Concurrency
- Reports
- Unit tests
- CI/CD
- Image downloader
- Docker
- Mocks


## Project Structure
``` 
Automated-Book-Data-Pipeline/
│
│
├── .github/
│   └── workflows/
│       └── python-tests.yml
│
├── data/                           # Output: JSON, PDF, Excel
│
├── src/                            # Main
│   ├── __init__.py
│   ├── analytics.py               # Computes stats and analytics from scraped book data
│   ├── categorized.py             # Groups books by category, builds JSON mapping categories
│   ├── clean.py                   # Normalizes and cleans raw book data 
│   ├── cover_downloader.py        # Downloads book cover images
│   ├── data_consistency.py        # Internal check script, validates data
│   ├── main.py                    # Main pipeline orchestrator
│   ├── parser.py                  # Parses HTML catalog and book pages
│   ├── report.py                  # Generates Excel and PDF reports
│   └── scraper.py                 # Scrapes catalog and book pages
│
├── tests/                              # Unit tests
│   ├── __init__.py
│   ├── test_cover_downloader.py        # Cover image download tests
│   ├── test_dataset.py                 # Dataset checks after full pipeline (skip on CI)
│   ├── test_scraper.py                 # Real get_all_books tests
│   ├── test_scraper_mock.py            # Mocked lightweight get_all_books tests
│   ├── test_scraper_details_mock.py    # Mocked detailed book parsing tests
│   └── test_scraper_details.py         # Real detailed book parsing tests
│
│
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

## Getting Started

1. **Clone the repo**
```
git clone https://github.com/gzappaa/Automated-Book-Data-Pipeline
cd Automated-Book-Data-Pipeline
```

2. **Install dependencies**

```
pip install -r requirements.txt
```

3. **Run the scraper**

```
python -m src.scraper
```
## Run with Docker

```
docker build -t book-pipeline .
```

# Run the container (maps local data/ folder for PDF/Excel output):

```
docker run --rm -v ${PWD}/data:/app/data book-pipeline
```
**Note:** On Windows, replace `${PWD}` with `%cd%`.

---

## Running Tests
```
python -m unittest discover -s tests
```
This will run all unit tests, including mocks and real scraping tests.
