import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


## I thought that some of the data was redundant, and this script confirmed to me that:
## All books have Product Type = 'Books'.
## All books have consistent availability.
## All books have Tax = 0.0.
## All books have Number of reviews = 0.
## Therefore, they will be removed in the cleaning step

# Load the books JSON
with open("data/books_raw.json", "r", encoding="utf-8") as f:
    books = json.load(f)

# 1️⃣ Check if all Product Types are "Books"
product_type_issues = [b["title"] for b in books if b["table_data"]["Product Type"] != "Books"]

if product_type_issues:
    print("Books with Product Type not equal to 'Books':")
    for t in product_type_issues:
        print("-", t)
else:
    print("All books have Product Type = 'Books'.")

# 2️⃣ Check if availability matches between main field and table_data
availability_issues = [b["title"] for b in books if b["availability"] != b["table_data"]["Availability"]]

if availability_issues:
    print("Books with inconsistent availability:")
    for t in availability_issues:
        print("-", t)
else:
    print("All books have consistent availability.")

# 3️⃣ Check if any book has Tax different from 0.0
books_with_tax = [b["title"] for b in books if b["table_data"]["Tax"] != 0.0]

if books_with_tax:
    print("Books with Tax not equal to 0.0:")
    for t in books_with_tax:
        print("-", t)
else:
    print("All books have Tax = 0.0.")

# 4️⃣ Check if any book has Number of reviews different from 0
books_with_reviews = [b["title"] for b in books if b["table_data"]["Number of reviews"] != 0]

if books_with_reviews:
    print("Books with Number of reviews not equal to 0:")
    for t in books_with_reviews:
        print("-", t)
else:
    print("All books have Number of reviews = 0.")

