import re
from urllib.parse import urljoin

# Base URL of the site
BASE_URL = "https://books.toscrape.com/"

# ------------------------------
# Book parsing class
# ------------------------------
class BookParser:
    # Mapping of star-rating words to numbers
    RATING_DICT = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}

    # ------------------------------
    # Parse price string to float
    # ------------------------------
    @staticmethod
    def parse_price(value: str) -> float:
        # Match numeric part in a string like 'A£51.77'
        match = re.search(r"\d+\.\d+", value)
        # Return float or 0.0 if not found
        return float(match.group()) if match else 0.0

    # ------------------------------
    # Parse rating from HTML class list
    # ------------------------------
    @classmethod
    def parse_rating(cls, rating_class_list):
        # Convert rating string to integer using RATING_DICT
        return cls.RATING_DICT.get(rating_class_list[1], 0)

    # ------------------------------
    # Parse book details table
    # ------------------------------
    @staticmethod
    def parse_table(table):
        # Initialize table data dictionary
        table_data = {}

        # Map fields to parsers
        PARSERS = {
            "Price (excl. tax)": BookParser.parse_price,
            "Price (incl. tax)": BookParser.parse_price,
            "Tax": BookParser.parse_price,
            "Number of reviews": int
        }

        # Extract table rows
        if table:
            for row in table.find_all("tr"):
                # Get field name and value
                key = row.find("th").text
                value = row.find("td").text.strip()

                # Apply parser if available
                if key in PARSERS:
                    value = PARSERS[key](value)
                table_data[key] = value

        # Return dictionary of parsed data
        return table_data

    # ------------------------------
    # Parse book description
    # ------------------------------
    @staticmethod
    def parse_description(soup):
        desc_tag = soup.find("meta", attrs={"name": "description"})
        if not desc_tag:
            return ""
        
        text = desc_tag["content"].strip()
        
        # Cleaning common encoding issues
        text = text.replace("â", "\"").replace("â", "\"")  # aspas
        text = text.replace("â", "-")  # en-dash
        text = text.replace("â", "'")  # apóstrofe
        text = text.replace("â¦", "...")  # reticências
        
        # Remove spaces and extra line breaks
        text = re.sub(r"\s+", " ", text).strip()
        
        return text
    
    # Parse availability text
    @staticmethod
    def parse_availability(soup):
        # Get the <p> tag with class "instock availability"
        avail_tag = soup.find("p", class_="instock availability")
        # Return the text stripped of whitespace, or empty string if not found
        return avail_tag.text.strip() if avail_tag else ""
    

    # ------------------------------
    # Parse a book from catalog HTML
    # ------------------------------
    @classmethod
    def parse_book(cls, book_html, base_url=BASE_URL):
        # Get book title
        title = book_html.h3.a["title"]

        # Get book price
        price_text = book_html.find("p", class_="price_color").text
        price = cls.parse_price(price_text)

        # Get book rating
        rating_class = book_html.find("p", class_="star-rating")["class"]
        rating = cls.parse_rating(rating_class)

        # Get book image URL
        image_url = urljoin(base_url, book_html.img["src"])

        # Get book detail URL
        relative_url = book_html.h3.a["href"]
        if not relative_url.startswith("catalogue/"):
            relative_url = f"catalogue/{relative_url}"
        book_url = urljoin(BASE_URL, relative_url)

        # Return dictionary with parsed book info
        return {
            "title": title,
            "price": price,
            "rating": rating,
            "image_url": image_url,
            "book_url": book_url
        }