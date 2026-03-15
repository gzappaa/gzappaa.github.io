import json
import re

# Categories that are considered invalid and should be renamed
BAD_CATEGORIES = {"default", "add a comment"}

def clean_books_data(input_file="data/books_raw.json", output_file="data/books_processed.json"):
    """
    Read the raw JSON, normalize categories and fields, and save a cleaned JSON.

    Args:
        input_file (str): Path to the raw JSON file.
        output_file (str): Path to save the cleaned JSON file.

    Returns:
        list: List of cleaned books.
    """

    # Load the raw books JSON
    with open(input_file, "r", encoding="utf-8") as f:
        books = json.load(f)

    clean_books = []

    for book in books:
        # Get the book category
        category = book.get("category", "")

        # Rename invalid categories to 'Miscellaneous'
        if category.lower() in BAD_CATEGORIES:
            category = "Miscellaneous"

        # Extract availability number from string
        availability_text = book.get("availability", "")
        match = re.search(r"\((\d+)\s+available\)", availability_text)
        availability = int(match.group(1)) if match else 0  # default 0 if not found

        # Build the cleaned book dictionary
        clean_books.append({
            "title": book.get("title"),                     # Book title
            "category": category,                           # Cleaned category
            "price": book.get("price"),                     # Price as float
            "rating": book.get("rating"),                   # Star rating
            "image_url": book.get("image_url"),             # Cover image URL
            "book_url": book.get("book_url"),               # Link to book page
            "description": book.get("description"),         # Book description
            "upc": book.get("table_data", {}).get("UPC"),   # Unique product code
            "availability": availability                    # Available units as int
        })

    # Save the cleaned books to a new JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(clean_books, f, indent=4, ensure_ascii=False)

    # Print summary
    print(f"{len(clean_books)} books cleaned and saved to {output_file}")

    return clean_books

if __name__ == "__main__":
    clean_books_data()