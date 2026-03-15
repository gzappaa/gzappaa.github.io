import json
from collections import defaultdict
from pathlib import Path

def calculate_complete_analytics(filepath="data/books_processed.json"):
    """
    Reads books JSON and returns a complete analytics dictionary.
    
    Output dictionary contains:
    - total_books
    - total_availability
    - average_price
    - average_rating
    - max_price (dict with title, price, category)
    - min_price (dict with title, price, category)
    - categories: dict of category stats
    - books: list of all books (with defaults for missing fields)
    """

    # Ensure file exists
    if not Path(filepath).exists():
        raise FileNotFoundError(f"{filepath} not found")

    with open(filepath, "r", encoding="utf-8") as f:
        raw_books = json.load(f)

    if not raw_books:
        raise ValueError("No books found in JSON")

    books = []
    for book in raw_books:
        # Ensure every field exists
        books.append({
            "title": book.get("title", "Untitled"),
            "category": book.get("category", "Miscellaneous"),
            "price": float(book.get("price", 0)),
            "rating": int(book.get("rating", 0)),
            "availability": int(book.get("availability", 0)),
            "image_url": book.get("image_url", ""),
            "book_url": book.get("book_url", ""),
            "description": book.get("description", ""),
            "upc": book.get("upc", book.get("table_data", {}).get("UPC", ""))
        })

    # Basic stats
    total_books = len(books)
    total_availability = sum(b["availability"] for b in books)
    average_price = round(sum(b["price"] for b in books) / total_books, 2)
    average_rating = round(sum(b["rating"] for b in books) / total_books, 2)

    max_price_book = max(books, key=lambda x: x["price"])
    min_price_book = min(books, key=lambda x: x["price"])

    # Category-level stats
    categories = defaultdict(lambda: {
        "num_books": 0,
        "total_availability": 0,
        "average_price": 0,
        "max_price": 0,
        "min_price": float("inf")
    })

    for b in books:
        cat = b["category"]
        cat_data = categories[cat]
        cat_data["num_books"] += 1
        cat_data["total_availability"] += b["availability"]
        cat_data["average_price"] += b["price"]
        if b["price"] > cat_data["max_price"]:
            cat_data["max_price"] = b["price"]
        if b["price"] < cat_data["min_price"]:
            cat_data["min_price"] = b["price"]

    # Finalize average_price per category
    for cat, data in categories.items():
        if data["num_books"] > 0:
            data["average_price"] = round(data["average_price"] / data["num_books"], 2)
        if data["min_price"] == float("inf"):
            data["min_price"] = 0

    analytics = {
        "total_books": total_books,
        "total_availability": total_availability,
        "average_price": average_price,
        "average_rating": average_rating,
        "max_price": {
            "title": max_price_book["title"],
            "price": max_price_book["price"],
            "category": max_price_book["category"]
        },
        "min_price": {
            "title": min_price_book["title"],
            "price": min_price_book["price"],
            "category": min_price_book["category"]
        },
        "categories": dict(categories),
        "books": books
    }

    return analytics


if __name__ == "__main__":
    analytics = calculate_complete_analytics("data/books_processed.json")
    print(f"Analytics computed for {analytics['total_books']} books")