import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

# GENERATES AN IMPORTANT JSON WITH THE URLS OF THE BOOKS BY CATEGORY, 
# TO FACILITATE TESTING AND FUTURE ANALYSIS


BASE_CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/"
OUTPUT_JSON_PATH = Path("data/books_by_category.json")

CATEGORIES = [
    "travel_2", "mystery_3", "historical-fiction_4", "sequential-art_5",
    "classics_6", "philosophy_7", "romance_8", "womens-fiction_9",
    "fiction_10", "childrens_11", "religion_12", "nonfiction_13",
    "music_14", "default_15", "science-fiction_16", "sports-and-games_17",
    "add-a-comment_18", "fantasy_19", "new-adult_20", "young-adult_21",
    "science_22", "poetry_23", "paranormal_24", "art_25", "psychology_26",
    "autobiography_27", "parenting_28", "adult-fiction_29", "humor_30",
    "horror_31", "history_32", "food-and-drink_33", "christian-fiction_34",
    "business_35", "biography_36", "thriller_37", "contemporary_38",
    "spirituality_39", "academic_40", "self-help_41", "historical_42",
    "christian_43", "suspense_44", "short-stories_45", "novels_46",
    "health_47", "politics_48", "cultural_49", "erotica_50", "crime_51"
]

def scrape_categories_urls():
    result = {}

    for cat_slug in CATEGORIES:
        category_name = cat_slug.split("_")[0].replace("-", " ").title()
        page = 1
        urls = []

        while True:
            page_url = urljoin(BASE_CATEGORY_URL, f"{cat_slug}/index.html") if page == 1 else \
                       urljoin(BASE_CATEGORY_URL, f"{cat_slug}/page-{page}.html")
            try:
                resp = requests.get(page_url)
                if resp.status_code != 200:
                    break
            except requests.RequestException:
                break

            soup = BeautifulSoup(resp.text, "html.parser")
            links = soup.select("article.product_pod h3 a")
            if not links:
                break

            for a in links:
                href = a["href"]
                full_url = urljoin(page_url, href)
                urls.append(full_url)

            next_page = soup.select_one("li.next a")
            if next_page:
                page += 1
            else:
                break

        result[category_name] = urls
        print(f"✅ {category_name}: {len(urls)} URLs")

    # save to JSON
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Saved JSON to {OUTPUT_JSON_PATH}")

if __name__ == "__main__":
    scrape_categories_urls()