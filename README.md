# FinBERT sentiment app

## Overview
JLT Terminal is a Tkinter-based desktop application for scraping, loading, and analyzing financial news and documents (including PDFs) with advanced sentiment analysis. It uses Hugging Face's FinBERT transformer model for finance-specific sentiment, and provides in-depth mathematical/statistical metrics for each analysis.

## Features
- **Load and display text** from TXT, CSV, and PDF files
- **Automatic sentiment analysis** using FinBERT (finance-specific transformer)
- **Math/statistical metrics**: overall score, weighted sentiment, volatility, momentum
- **Highlight/Unhighlight words** in the displayed text
- **Clear screen** to remove all displayed text
- **Visualize sentiment**: see sentiment distribution and statistics in a chart
- **Thread-safe GUI**: all updates run in the main thread
- **Robust file reading**: handles encoding and PDF extraction

## How to Use
1. **Install dependencies** (see below)
2. Run `python webscraper.py`
3. Use the sidebar to:
   - Select and load a file (TXT, CSV, PDF)
   - Highlight or unhighlight words
   - Clear the screen
   - Run sentiment analysis (auto-runs on file load)
   - Visualize sentiment results

## Sentiment Analysis Details
- Uses Hugging Face's `ProsusAI/finbert` model
- Analyzes each sentence for sentiment (positive, negative, neutral)
- Calculates:
  - **Overall Score** (mean sentiment)
  - **Weighted Sentiment** (confidence-weighted)
  - **Volatility** (standard deviation)
  - **Momentum** (trend from first to second half)
- Results are shown in a popup and can be visualized as a chart

## Requirements
- Python 3.8+
- Install dependencies:
  ```bash
  pip install tkinter pandas requests beautifulsoup4 matplotlib seaborn PyPDF2 transformers torch
  ```

## Notes
- For best results, use with financial news, earnings reports, or similar documents.
- All processing is local; no data is sent to external servers (except for model download on first run).
- The app is designed for single-file analysis, but can be extended for batch or time-series analysis.

## License
MIT License

---

**Created by [Narasimha Cittarusu]**
