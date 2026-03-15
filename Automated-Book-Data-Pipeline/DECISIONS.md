# Decisions

1. **Scraping Approach**  
Decision: Use BeautifulSoup with requests and multithreading.  
Rationale: BS4 is lightweight, easy to parse HTML.  
Alternatives Considered: I’m familiar with neither Scrapy nor Selenium.  
Impact: Easy to maintain, can fetch all pages quickly.  

2. **Retries & Error Handling**  
Decision: Retry failed requests up to 3 times with a delay.  
Rationale: Network failures can happen; retry increases robustness.  
Impact: Ensures scraping completes reliably; minor delay on repeated failures.  

3. **Data Cleaning**  
Decision: Normalize categories, convert prices to floats, extract availability numbers.  
Rationale: Raw data (`books_raw.json`) is inconsistent. For example: availability listed twice, all products labeled as "Books", tax always 0. `data_consistency.py` verifies this and remains in the project to ensure data integrity.  

Additional Decisions:  
- One book appeared twice with different URLs (`_764` and `_642`) with different UPCs and cover images; treated as separate entries.  
- Two categories, "Add a comment" (67 books) and "default" (152 books), appeared to be entry errors; merged into "Miscellaneous".  
- Save all book cover images using `UPC_title.jpg` to ensure uniqueness and readability.  

Impact: `books_processed.json` is reliable for all downstream processing.  

4. **Parallelism / Concurrency**  
Decision: Use ThreadPoolExecutor for both page scraping and image downloading.  
Rationale: I/O-bound tasks benefit from threads.  
Impact: Faster execution; thread-safety handled with Lock objects.  

5. **File Structure & Modularization**  
Decision: Separate scripts into modules: scraper, parser, clean, analytics, report, cover_downloader.  
Rationale: Improves maintainability and testability; each module has a clear responsibility.  
Impact: Easier unit testing and potential reuse of modules.  

6. **Reports**  
Decision: Generate both PDF and Excel reports.  
Rationale: PDF for human-readable summary; Excel for further analysis.  
Impact: Multiple output formats satisfy different use cases.  

7. **Testing**  
Decision: Use unittest with mocks for network calls and real tests for small subsets.  
Rationale: Avoids slow tests hitting the real website every time.  
Impact: Fast CI, reliable testing of pipeline logic.  

8. **Docker**  
Decision: Containerize the pipeline for reproducibility.  
Rationale: Ensures dependencies and Python versions are consistent across machines.  
Impact: Easy to run on any host; maps `data/` folder to preserve outputs.  

9. **Data Storage**  
Decision: Store JSONs in `data/` and images in `data/images/`.  
Rationale: Keeps outputs organized; easy to reference in analytics and reports.  
Impact: Clear separation of raw, processed, and auxiliary data.  

10. **Future Considerations**  
- Use a database for scalability if the dataset grows.  
- Potential migration to Scrapy for more complex sites.  
- Consider async I/O (aiohttp + asyncio) for even faster scraping.