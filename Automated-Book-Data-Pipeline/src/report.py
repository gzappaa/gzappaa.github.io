from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import pandas as pd
from pathlib import Path
from .analytics import calculate_complete_analytics

def generate_reports(stats, pdf_path="data/book_report.pdf", excel_path="data/book_report.xlsx"):
    """
    Generate both PDF and Excel reports from book stats.

    PDF contains:
    - Summary statistics
    - Most expensive book
    - Cheapest book
    - Complete list of books

    Excel contains multiple sheets:
    - All Books
    - Category Summary
    - Top 20 Expensive
    - Top 5 per Category
    """
    Path("data").mkdir(exist_ok=True)
    books = stats["books"]

    # ===== PDF =====
    doc = SimpleDocTemplate(pdf_path)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>Book Data Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.5*inch))

    # Summary
    elements.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Total Books: {stats['total_books']}", styles["Normal"]))
    elements.append(Paragraph(f"Total Availability: {stats['total_availability']}", styles["Normal"]))
    elements.append(Paragraph(f"Average Price: £{stats['average_price']}", styles["Normal"]))
    elements.append(Paragraph(f"Average Rating: {stats['average_rating']} stars", styles["Normal"]))
    elements.append(Spacer(1, 0.3*inch))

    # Most expensive
    me = stats["max_price"]
    elements.append(Paragraph("<b>Most Expensive Book</b>", styles["Heading3"]))
    elements.append(Paragraph(f"{me['title']} - £{me['price']} ({me['category']})", styles["Normal"]))
    elements.append(Spacer(1, 0.3*inch))

    # Cheapest
    ch = stats["min_price"]
    elements.append(Paragraph("<b>Cheapest Book</b>", styles["Heading3"]))
    elements.append(Paragraph(f"{ch['title']} - £{ch['price']} ({ch['category']})", styles["Normal"]))
    elements.append(Spacer(1, 0.3*inch))

    # Complete book list
    elements.append(Paragraph("<b>Complete Book List</b>", styles["Heading2"]))
    book_items = [
        ListItem(Paragraph(f"{b['title']} | £{b['price']} | {b['rating']} stars | {b['category']}", styles["Normal"]))
        for b in books
    ]
    elements.append(ListFlowable(book_items, bulletType="bullet"))

    doc.build(elements)
    print(f"PDF report saved to {pdf_path}")

    # ===== Excel =====
    df_books = pd.DataFrame(books)

    # Category Summary
    category_summary = pd.DataFrame([
        {
            "category": cat,
            "num_books": data["num_books"],
            "total_availability": data["total_availability"],
            "average_price": data["average_price"],
            "max_price": data["max_price"],
            "min_price": data["min_price"]
        }
        for cat, data in stats["categories"].items()
    ]).sort_values("num_books", ascending=False)

    # Top 20 most expensive
    top_expensive = df_books.sort_values("price", ascending=False).head(20)

    # Top 5 per category
    top_per_category = (
        df_books.sort_values(["category", "price"], ascending=[True, False])
        .groupby("category")
        .head(5)
        .reset_index(drop=True)
    )

    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        df_books.to_excel(writer, sheet_name="All Books", index=False)
        category_summary.to_excel(writer, sheet_name="Category Summary", index=False)
        top_expensive.to_excel(writer, sheet_name="Top 20 Expensive", index=False)
        top_per_category.to_excel(writer, sheet_name="Top 5 per Category", index=False)

    print(f"Excel report saved to {excel_path}")


if __name__ == "__main__":
    stats = calculate_complete_analytics("data/books_processed.json")
    generate_reports(stats)