import requests
from pathlib import Path

# file to save the HTML content for testing
Path("tests/data").mkdir(exist_ok=True)

# urls to fetch for testing
urls = {
    "catalogue": "https://books.toscrape.com/",
    "book_detail": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}

for name, url in urls.items():
    response = requests.get(url)
    if response.ok:
        filepath = Path(f"tests/data/{name}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Saved {name} to {filepath}")
    else:
        print(f"Failed to fetch {url}")