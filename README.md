<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Giovanni Zappa Portfolio</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem;
      background-color: #f5f5f5;
      color: #333;
      line-height: 1.6;
    }
    h1, h2 { color: #2c3e50; }
    a { color: #2980b9; text-decoration: none; }
    a:hover { text-decoration: underline; }
    code { background-color: #ecf0f1; padding: 2px 4px; border-radius: 4px; }
    .section { margin-bottom: 2rem; }
    ul { padding-left: 1.5rem; }
    .data-sample { background-color: #fff; border: 1px solid #ddd; padding: 1rem; border-radius: 6px; margin: 1rem 0; }
  </style>
</head>
<body>

<h1>Automated Book Data Pipeline</h1>

<div class="section">
  <p>This project is a modular, reproducible, and testable pipeline for scraping, processing, and analyzing book data from <strong>Books to Scrape</strong>. It collects book information, cleans and analyzes the data, downloads cover images, and generates PDF and Excel reports.</p>
</div>

<div class="section">
  <h2>GitHub Repository</h2>
  <p>Full code and instructions are available at: 
     <a href="https://github.com/gzappaa/Automated-Book-Data-Pipeline" target="_blank">
     https://github.com/gzappaa/Automated-Book-Data-Pipeline</a>
  </p>
</div>

<div class="section">
  <h2>Pipeline Modules</h2>
  <ul>
    <li><strong>Scraper:</strong> Collects book data using BeautifulSoup + multithreading.</li>
    <li><strong>Parser:</strong> Extracts structured info from HTML catalog and book pages.</li>
    <li><strong>Data Cleaning:</strong> Normalizes categories, converts prices, extracts availability.</li>
    <li><strong>Cover Downloader:</strong> Saves book images as <code>UPC_title.jpg</code>.</li>
    <li><strong>Analytics:</strong> Computes totals, averages, min/max prices, per-category stats.</li>
    <li><strong>Reporting:</strong> Generates PDF and Excel reports.</li>
    <li><strong>Testing:</strong> Unit tests with mocks and CI-ready configuration.</li>
    <li><strong>Docker:</strong> Containerized pipeline for easy reproducibility.</li>
  </ul>
</div>

<div class="section">
  <h2>Workflow</h2>
  <div class="data-sample">
    scrape books (basic info) → fetch detailed info → clean data → download covers → generate reports
  </div>
</div>

<div class="section">
  <h2>Getting Started</h2>
  <ul>
    <li>Clone the repo: <code>git clone https://github.com/gzappaa/Automated-Book-Data-Pipeline</code></li>
    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
    <li>Run scraper: <code>python -m src.scraper</code></li>
    <li>Run with Docker: <code>docker build -t book-pipeline .</code> and <code>docker run --rm -v ${PWD}/data:/app/data book-pipeline</code></li>
  </ul>
</div>

<div class="section">
  <h2>Notes</h2>
  <p>All prices are numeric only (no € symbol), but amounts are in euros. All data outputs (JSON, PDFs, Excel, images) are saved in the <code>data/</code> folder.</p>
</div>

<div class="section">
  <h2>Screenshots / Reports (Optional)</h2>
  <p>You can include some screenshots of PDFs, Excel sheets, or cover images here to make it more visual.</p>
</div>

</body>
</html>
