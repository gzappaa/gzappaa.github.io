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

    /* project card separator */
    .project { 
      background: #fff; 
      border: 1px solid #ddd; 
      border-radius: 8px; 
      padding: 2rem; 
      margin-bottom: 2.5rem;
    }
    .project h1 { margin-top: 0; }
    .badge {
      display: inline-block;
      font-size: 0.75rem;
      background: #eaf4fb;
      color: #2980b9;
      border: 1px solid #aed6f1;
      border-radius: 4px;
      padding: 2px 8px;
      margin-right: 4px;
      margin-bottom: 6px;
    }
  </style>
</head>
<body>

<!-- ─────────────────────────────────────────────
     PROJECT 1 — Hebrew Vocab Hub
───────────────────────────────────────────── -->
<div class="project">
  <h1>hebrew_vocab_hub</h1>
  <div class="section">
    <span class="badge">Scrapy</span>
    <span class="badge">Playwright</span>
    <span class="badge">MongoDB</span>
    <span class="badge">MySQL</span>
    <span class="badge">PostgreSQL JSONB</span>
    <span class="badge">Python</span>
    <span class="badge">pandas</span>
    <span class="badge">GitHub Actions</span>
  </div>
  <div class="section">
    <p>A data pipeline that builds a structured Hebrew vocabulary dataset from multiple real-world Israeli sources — dictionary entries, song lyrics, news articles, and YouTube comments — and outputs a single unified JSON ready for use in language learning APIs, apps, or databases.</p>
    <p>The core challenge is Hebrew's <strong>niqqudot</strong> (vowel points): modern Hebrew text is written without them, so the same string like <code>חברה</code> can mean <em>company</em>, <em>girlfriend</em>, or <em>she connected</em> depending on context. The pipeline handles this by matching words across all inflected forms in conjugation tables using Unicode NFD decomposition, and flags entries with <code>multiple_meanings: true</code> when ambiguity exists.</p>
  </div>
  <div class="section">
    <h2>GitHub Repository</h2>
    <p>Full code and instructions are available at:
       <a href="https://github.com/gzappaa/hebrew_vocab_hub" target="_blank">
       https://github.com/gzappaa/hebrew_vocab_hub</a>
    </p>
  </div>
  <div class="section">
    <h2>What it produces</h2>
    <p>~13,000 Hebrew words, each entry containing meanings with niqqudot, transcription, root, part of speech, full conjugation/declension tables, bilingual example sentences, and real-world frequency across songs, news, and YouTube.</p>
    <div class="data-sample">
      <pre style="margin:0; font-size: 0.85rem; overflow-x: auto;">{
  "word": "חברה",
  "multiple_meanings": true,
  "meanings": [
    { "hebrew": "חֶבְרָה", "transcription": "chevra", "meaning": "company, society", ... },
    { "hebrew": "חֲבֵרָה", "transcription": "chavera", "meaning": "girlfriend; female friend", ... }
  ],
  "sentences": [
    { "sentence": "החברה הזו גדולה.", "translation": "This company is big.", "source": "reverso" }
  ],
  "sources": { "songs": 12, "news": 45, "youtube": 8, "total": 65 }
}</pre>
    </div>
    <p>The dataset is <strong>PostgreSQL JSONB-ready</strong> — insert the whole document into a <code>jsonb</code> column and index on <code>word</code>.</p>
  </div>
  <div class="section">
    <h2>Pipeline</h2>
    <div class="data-sample">
      pealim.com → spider_dict + spider_words → dict-complete.json<br>
      Spotify Israel charts → lyrics (Genius API + spider_lyrics) → all_lyrics.txt<br>
      hadshon.co.il → news articles → hadshon_articles.json<br>
      YouTube Data API → trending comments → word_sources.json<br>
      Tatoeba API + Reverso (Playwright) → example sentences<br>
      ↓<br>
      final_dataset.py → <strong>vocab_dataset.json</strong>
    </div>
  </div>
  <div class="section">
    <h2>Data sources</h2>
    <ul>
      <li><a href="https://www.pealim.com" target="_blank">pealim.com</a> — dictionary entries with niqqudot, transcription, conjugation tables</li>
      <li><a href="https://www.hadshon.co.il" target="_blank">hadshon.co.il</a> — Israeli government Hebrew learning site; news articles used for word frequency</li>
      <li>Spotify Israel top charts — top ~2,000 songs since 2018, filtered for Hebrew titles</li>
      <li><a href="https://genius.com" target="_blank">Genius</a> — song lyrics scraped for each Hebrew track</li>
      <li><a href="https://tatoeba.org" target="_blank">Tatoeba</a> — bilingual example sentences (public API)</li>
      <li><a href="https://context.reverso.net" target="_blank">Reverso Context</a> — bilingual sentences for words missing from Tatoeba, via Playwright</li>
      <li>YouTube Data API v3 — daily trending video comments from Israel</li>
    </ul>
  </div>
  <div class="section">
    <h2>Getting Started</h2>
    <ul>
      <li>Clone: <code>git clone https://github.com/gzappaa/hebrew_vocab_hub</code></li>
      <li>Install: <code>pip install -r requirements.txt && playwright install chromium</code></li>
      <li>Full bootstrap: <code>make bootstrap</code></li>
      <li>Daily refresh: <code>make daily</code></li>
      <li>Tests: <code>make test</code></li>
    </ul>
  </div>
</div>

<!-- ─────────────────────────────────────────────
     PROJECT 2 — Book Pipeline
───────────────────────────────────────────── -->
<div class="project">
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
</div>


</body>
</html>
