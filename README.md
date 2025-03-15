

# Stock Web Scraper Sentiment Analysis

`JLT Terminal` is a Python application with a graphical user interface (GUI) built using Tkinter. It serves as a financial data scraper and sentiment analysis tool, allowing users to fetch web content, analyze sentiment, visualize data, and automate searches for financial news related to specific companies. The application integrates libraries like `pandas`, `requests`, `BeautifulSoup`, `nltk`, `googlesearch`, and `matplotlib` to process and visualize data.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [How It Works](#how-it-works)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Web Content Loading**: Fetch content from URLs or load text from files (including CSV).
- **Batch Processing**: Process multiple URLs from a text or CSV file.
- **Text Manipulation**: Find and replace text, highlight specific words, and unhighlight them.
- **HTML Parsing**: Extract specific HTML elements (e.g., paragraphs) or auto-detect tables.
- **Sentiment Analysis**: Analyze text sentiment using NLTK’s VADER sentiment analyzer, identifying positive, negative, and neutral sentiments.
- **Word Display**: Extract and display words from loaded content.
- **History Tracking**: Maintain a history of loaded URLs and sentiment analysis results, exportable to CSV.
- **Automated Search**: Continuously scrape Google for financial news based on company name, NASDAQ code, and SEO keywords.
- **Data Visualization**: Generate histograms to visualize the distribution of positive and negative words using Matplotlib and Seaborn.
- **GUI Interface**: User-friendly interface with buttons for various functionalities and a scrolled text area for output.

## Prerequisites
Before running this application, ensure you have the following installed on your system:
- **Python**: Version 3.6 or higher.
- **Required Libraries**:
  - `tkinter` (usually included with Python).
  - `pandas`: `pip install pandas`
  - `requests`: `pip install requests`
  - `beautifulsoup4`: `pip install beautifulsoup4`
  - `nltk`: `pip install nltk` (includes VADER lexicon, downloaded automatically on first run).
  - `googlesearch-python`: `pip install googlesearch-python`
  - `matplotlib`: `pip install matplotlib`
  - `seaborn`: `pip install seaborn`

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd jlt-terminal
   ```

2. **Install Dependencies**:
   Run the following command to install all required Python packages:
   ```bash
   pip install pandas requests beautifulsoup4 nltk googlesearch-python matplotlib seaborn
   ```
   - Note: The first run of the application will automatically download the `vader_lexicon` for NLTK.

3. **Run the Application**:
   ```bash
   python main.py
   ```
   - Replace `main.py` with the name of your source file if different.

## Usage
1. **Launch the Application**:
   Run the script to open the `JLT Terminal` window.

2. **Load Content**:
   - **Load URL**: Enter a URL in the entry field and click "Load URL" to fetch and display its content.
   - **Select File**: Click "Select File" to load text or CSV content from a file.
   - **Batch Process URLs**: Select a `.txt` or `.csv` file containing URLs to process them sequentially.

3. **Text Manipulation**:
   - **Find and Replace**: Enter a word to find and its replacement, then apply the change.
   - **Highlight Text**: Enter a word to highlight it in yellow in the text area.
   - **Unhighlight Text**: Remove all highlights.

4. **HTML Parsing**:
   - **Select HTML Elements**: Enter an HTML tag (e.g., `p`) to extract and display its content.
   - **Auto-Detect Tables**: Extract and display all `<table>` elements from the loaded HTML.

5. **Sentiment Analysis**:
   - Click "Sentiment Analysis" to analyze the loaded text, displaying positive and negative words and overall sentiment in a new window.

6. **Word Display**:
   - Click "Display Words" to show all words extracted from the loaded content in a new window.

7. **History Management**:
   - Click "Show History" to view a table of all loaded URLs and sentiment analyses.
   - Click "Export to CSV" in the history window to save the data to a file.

8. **Automated Search**:
   - Click "Start Auto Search" to open a configuration window.
   - Enter the company name, NASDAQ code, SEO keywords (comma-separated), interval (seconds), and duration (minutes).
   - Click "Start" to begin scraping financial news every `interval` seconds for `duration` minutes.
   - Click "Stop Auto Search" to halt the process.

9. **Visualize Sentiment**:
   - Click "Visualize Sentiment" to open a window.
   - Click "Import CSV" to load a history CSV file and display a histogram of positive and negative word counts.

10. **Exit**:
    - Close the main window to terminate the application.

## Code Structure
- **Main Class: `StockScraperApp`**:
  - Manages the Tkinter GUI, including frames, buttons, text display, and event handling.
- **Helper Class: `FinanceScraper`**:
  - Handles web scraping, sentiment analysis, and automated search logic.
- **Key Methods**:
  - `setup_frames`, `setup_buttons`, `setup_text_display`: Initialize the GUI layout.
  - `load_from_url`, `load_from_file`: Fetch content from URLs or files.
  - `find_replace`, `highlight_text`, `unhighlight_text`: Manipulate displayed text.
  - `select_html_elements`, `auto_detect_tables`: Parse HTML content.
  - `perform_sentiment_analysis`: Analyze sentiment and display results.
  - `display_words`: Extract and show words.
  - `show_history`, `export_history`: Manage and export history.
  - `start_auto_search`, `stop_auto_search`: Control automated scraping.
  - `visualize_sentiment`, `import_csv`: Visualize sentiment data.

## How It Works
1. **Content Loading**:
   - URLs are fetched using `requests`, and files are read with `pandas` or standard file I/O.
   - Content is displayed in chunks of 5000 characters in a scrolled text area.
2. **Text Manipulation**:
   - Text replacement and highlighting are performed using Tkinter’s text widget tags.
3. **HTML Parsing**:
   - `BeautifulSoup` extracts specified elements or tables from HTML content.
4. **Sentiment Analysis**:
   - NLTK’s VADER analyzes text sentiment, categorizing words as positive, negative, or neutral based on compound scores.
5. **Automated Search**:
   - `googlesearch-python` queries Google, and `FinanceScraper` fetches article summaries, analyzes sentiment, and updates the display every 5 seconds per result.
6. **Visualization**:
   - `matplotlib` and `seaborn` create histograms of word counts from imported CSV data, displayed in a Tkinter canvas.

## Limitations
- **Internet Dependency**: Requires an active internet connection for URL loading and Google searches.
- **Rate Limiting**: Google search API may impose limits, causing errors during automated searches.
- **Sentiment Accuracy**: VADER’s sentiment analysis may not fully capture context or industry-specific terms.
- **Performance**: Large files or frequent automated searches may slow down the application.
- **Error Handling**: Limited validation for invalid URLs or file formats.
- **Visualization**: Relies on user-provided CSV; no real-time visualization of current session data.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request with a description of your changes.

Please ensure your code follows Python best practices, includes comments, and maintains compatibility with the existing structure.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or support, please contact [Your Name] at [your.email@example.com] or open an issue on the repository.

---


