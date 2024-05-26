import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, scrolledtext, Canvas, ttk
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import threading
import nltk
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googlesearch import search
import matplotlib.pyplot as plt

nltk.download('vader_lexicon')

class FinanceScraper:
    def __init__(self, company, nasdaq_code, seo_words, display_callback):
        self.company = company
        self.nasdaq_code = nasdaq_code
        self.seo_words = seo_words
        self.display_callback = display_callback
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.history = []
  
    def analyze_sentiment(self, text):
        return self.sentiment_analyzer.polarity_scores(text)

    def fetch_article_summary(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        summary = ' '.join([para.get_text() for para in paragraphs])
        return summary

    def scrape_google_search(self):
        query = f"{self.company} {self.nasdaq_code} {' '.join(self.seo_words)} finance news"
        for url in search(query, num_results=10):
            try:
                summary = self.fetch_article_summary(url)
                sentiment = self.analyze_sentiment(summary)

                self.display_callback(self.company, url, summary, sentiment)
                self.history.append({"Title": self.company, "URL": url, "Summary": summary, **sentiment})
                time.sleep(5)  # Display each result for 5 seconds
            except Exception as e:
                print(f"Error processing {url}: {e}")

    def start_scraping(self, interval, duration):
        end_time = time.time() + duration * 60
        while time.time() < end_time:
            self.scrape_google_search()
            time.sleep(interval)

    def export_history(self, file_path):
        history_df = pd.DataFrame(self.history)
        history_df.to_csv(file_path, index=False)
        print(f"History exported to {file_path}")


class StockScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text Manipulation Tool")
        self.text_content = ""  # Variable to store all text
        self.chunk_size = 5000  # Display 5000 characters at a time
        self.current_position = 0  # Current starting index of text to display
        self.history = []  # List to store history of URL loads and sentiment analysis
        self.scraper_thread = None
        self.scraper = None

        self.setup_frames()
        self.setup_buttons()
        self.setup_text_display()
        self.setup_icon()

    def setup_frames(self):
        self.left_frame = tk.Frame(self.root, width=200, relief=tk.RAISED, borderwidth=2, bg='white')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.right_frame = tk.Frame(self.root, bg='white')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def setup_buttons(self):
        tk.Label(self.left_frame, text="Enter URL or Select File:", bg='white').pack(fill=tk.X, padx=5)
        self.url_entry = tk.Entry(self.left_frame, width=20)
        self.url_entry.pack(fill=tk.X, padx=5)
        self.add_buttons()

    def add_buttons(self):
        commands = [("Load URL", self.load_from_url), ("Select File", self.load_from_file),
                    ("Batch Process URLs", self.process_url_list), ("Find and Replace", self.find_replace),
                    ("Highlight Text", self.highlight_text), ("Unhighlight Text", self.unhighlight_text),
                    ("Select HTML Elements", self.select_html_elements),
                    ("Auto-Detect Tables", self.auto_detect_tables),
                    ("Sentiment Analysis", self.perform_sentiment_analysis), ("Display Words", self.display_words),
                    ("Show History", self.show_history), ("Start Auto Search", self.start_auto_search),
                    ("Stop Auto Search", self.stop_auto_search), ("Visualize Sentiment", self.visualize_sentiment)]
        for (text, command) in commands:
            tk.Button(self.left_frame, text=text, command=command, bg='red', fg='white').pack(fill=tk.X, padx=5, pady=5)

    def setup_text_display(self):
        self.text = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, bg='black', fg='white')
        self.text.pack(fill=tk.BOTH, expand=True)

    def setup_icon(self):
        canvas = Canvas(self.left_frame, width=20, height=20, bg='white', highlightthickness=0)
        canvas.pack(side=tk.BOTTOM, pady=10, expand=True)

    def load_from_url(self):
        url = self.url_entry.get()
        threading.Thread(target=self.fetch_and_display_url, args=(url,)).start()

    def load_from_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            threading.Thread(target=self.read_file, args=(file_path,)).start()

    def fetch_and_display_url(self, url):
        try:
            response = requests.get(url)
            self.text_content = response.text
            self.current_position = 0
            self.update_text_display()
            self.perform_sentiment_analysis()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to load URL: {e}")

    def read_file(self, file_path):
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                self.text_content = df.to_string()
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text_content = file.read()
            self.current_position = 0
            self.update_text_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

    def update_text_display(self):
        if self.text_content:
            self.text.config(state=tk.NORMAL)
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, self.text_content[self.current_position:self.current_position + self.chunk_size])
            self.text.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "No content to display.")

    def find_replace(self):
        word_to_find = simpledialog.askstring("Find and Replace", "Enter word to find:")
        word_to_replace = simpledialog.askstring("Find and Replace", "Enter word to replace with:")

        if word_to_find and word_to_replace:
            self.text_content = self.text_content.replace(word_to_find, word_to_replace)
            self.update_text_display()

    def highlight_text(self):
        word_to_highlight = simpledialog.askstring("Highlight Text", "Enter word to highlight:")
        if word_to_highlight:
            self.text.tag_remove("highlight", "1.0", tk.END)
            start_pos = "1.0"
            while True:
                start_pos = self.text.search(word_to_highlight, start_pos, tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word_to_highlight)}c"
                self.text.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
            self.text.tag_config("highlight", background="yellow")

    def unhighlight_text(self):
        self.text.tag_remove("highlight", "1.0", tk.END)

    def select_html_elements(self):
        element = simpledialog.askstring("Select HTML Elements", "Enter HTML element (e.g., 'p' for paragraphs):")
        if element:
            try:
                soup = BeautifulSoup(self.text_content, 'html.parser')
                elements = soup.find_all(element)
                element_text = "\n\n".join([el.get_text() for el in elements])
                self.text_content = element_text
                self.update_text_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to select HTML elements: {e}")

    def auto_detect_tables(self):
        try:
            soup = BeautifulSoup(self.text_content, 'html.parser')
            tables = soup.find_all('table')
            tables_text = "\n\n".join([str(table) for table in tables])
            self.text_content = tables_text
            self.update_text_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to auto-detect tables: {e}")

    def process_url_list(self):
        url_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if url_file:
            try:
                urls = []
                if url_file.endswith('.csv'):
                    df = pd.read_csv(url_file)
                    urls = df.iloc[:, 0].tolist()
                else:
                    with open(url_file, 'r') as file:
                        urls = file.readlines()

                for url in urls:
                    self.fetch_and_display_url(url.strip())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process URL list: {e}")

    def perform_sentiment_analysis(self):
        if not self.text_content:
            messagebox.showerror("Error", "No content loaded. Please load a URL or file first.")
            return

        if not hasattr(self, 'word_list') or not self.word_list:
            self.display_words()

        sid = SentimentIntensityAnalyzer()
        positive_words = []
        negative_words = []

        for word in self.word_list:
            sentiment = sid.polarity_scores(word)
            if sentiment['compound'] >= 0.05:
                positive_words.append(word)
            elif sentiment['compound'] <= -0.05:
                negative_words.append(word)

        positive_df = pd.DataFrame(positive_words, columns=['Word'])
        negative_df = pd.DataFrame(negative_words, columns=['Word'])

        positive_df['Frequency'] = positive_df['Word'].map(positive_df['Word'].value_counts())
        negative_df['Frequency'] = negative_df['Word'].map(negative_df['Word'].value_counts())

        positive_output = "Positive Words:\n" + positive_df.to_string(index=False)
        negative_output = "\nNegative Words:\n" + negative_df.to_string(index=False)

        # Determine overall sentiment
        if len(positive_words) > len(negative_words):
            overall_sentiment = "Good"
        elif len(positive_words) < len(negative_words):
            overall_sentiment = "Bad"
        else:
            overall_sentiment = "Moderate"

        # Store results in history
        self.history.append({
            'Title': self.url_entry.get(),
            'URL': self.url_entry.get(),
            'Summary': self.text_content[:200],  # Summary is the first 200 characters
            'Sentiment': overall_sentiment
        })

        # Create a new window
        sentiment_window = tk.Toplevel()
        sentiment_window.title("Sentiment Analysis Results")

        # Create text widget to display results
        results_text = tk.Text(sentiment_window)
        results_text.insert(tk.END, positive_output + "\n" + negative_output)
        results_text.pack()

        sentiment_window.mainloop()

    def display_words(self):
        try:
            if self.text_content:
                # Get the webpage text content
                soup = BeautifulSoup(self.text_content, 'html.parser')
                webpage_text = soup.get_text()

                # Split the text into words
                self.word_list = re.findall(r'\w+', webpage_text)

                # Create a new window to display the words
                display_window = tk.Toplevel(self.root)
                display_window.title("Words from URL")
                text_box = scrolledtext.ScrolledText(display_window, wrap=tk.WORD)

                # Insert the words into the text box
                word_list_str = '\n'.join(self.word_list)
                text_box.insert(tk.END, word_list_str)
                text_box.pack(fill=tk.BOTH, expand=True)
            else:
                messagebox.showerror("Error", "No content loaded. Please load a URL first.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_history(self):
        history_window = tk.Toplevel()
        history_window.title("History of Loaded URLs and Sentiment Analysis")

        columns = ("Title", "URL", "Summary", "Sentiment")
        tree = ttk.Treeview(history_window, columns=columns, show="headings")
        tree.heading("Title", text="Title")
        tree.heading("URL", text="URL")
        tree.heading("Summary", text="Summary")
        tree.heading("Sentiment", text="Sentiment")

        for entry in self.history:
            tree.insert("", tk.END, values=(
                entry['Title'],
                entry['URL'],
                entry['Summary'],
                entry['Sentiment']
            ))

        tree.pack(fill=tk.BOTH, expand=True)

        export_button = tk.Button(history_window, text="Export to CSV", command=self.export_history)
        export_button.pack(pady=10)

    def export_history(self):
        if not self.history:
            messagebox.showerror("Error", "No history to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save history as CSV")
        if file_path:
            history_df = pd.DataFrame(self.history)
            history_df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"History exported to {file_path}")

    def start_auto_search(self):
        auto_search_window = tk.Toplevel(self.root)
        auto_search_window.title("Start Automatic Search")

        tk.Label(auto_search_window, text="Company Name:").pack(fill=tk.X, padx=5, pady=5)
        company_name_entry = tk.Entry(auto_search_window)
        company_name_entry.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(auto_search_window, text="NASDAQ Code:").pack(fill=tk.X, padx=5, pady=5)
        nasdaq_code_entry = tk.Entry(auto_search_window)
        nasdaq_code_entry.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(auto_search_window, text="SEO Words (comma separated):").pack(fill=tk.X, padx=5, pady=5)
        seo_words_entry = tk.Entry(auto_search_window)
        seo_words_entry.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(auto_search_window, text="Interval (seconds):").pack(fill=tk.X, padx=5, pady=5)
        interval_entry = tk.Entry(auto_search_window)
        interval_entry.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(auto_search_window, text="Duration (minutes):").pack(fill=tk.X, padx=5, pady=5)
        duration_entry = tk.Entry(auto_search_window)
        duration_entry.pack(fill=tk.X, padx=5, pady=5)

        def start_search():
            company = company_name_entry.get()
            nasdaq_code = nasdaq_code_entry.get()
            seo_words = seo_words_entry.get().split(',')
            interval = int(interval_entry.get())
            duration = int(duration_entry.get())

            self.scraper = FinanceScraper(company, nasdaq_code, seo_words, self.display_article)
            self.scraper_thread = threading.Thread(target=self.scraper.start_scraping, args=(interval, duration))
            self.scraper_thread.start()
            auto_search_window.destroy()

        tk.Button(auto_search_window, text="Start", command=start_search).pack(pady=10)

    def visualize_sentiment(self):
        #if self.scraper:
            sentiment_window = tk.Toplevel()
            sentiment_window.title("Visualize Sentiment")

            import_button = tk.Button(sentiment_window, text="Import CSV", command=self.import_csv)
            import_button.pack(pady=10)

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                if 'pos' in df.columns and 'neg' in df.columns:
                    plt.figure(figsize=(10, 6))
                    plt.scatter(df['pos'], range(len(df)), color='green', label='Positive Sentiment')
                    plt.scatter(df['neg'], range(len(df)), color='red', label='Negative Sentiment')
                    plt.xlabel('Sentiment Score')
                    plt.ylabel('Article Index')
                    plt.title('Sentiment Analysis Results')
                    plt.xticks([0, 0.5, 1], ['Neg', 'Neutral', 'Pos'])
                    plt.legend()
                    plt.grid(True)
                    plt.show()
                else:
                    messagebox.showerror("Error", "CSV file does not contain required columns 'pos' and 'neg'.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import CSV: {e}")
    
    def display_article(self, title, link, summary, sentiment):
        sentiment_str = f"Pos: {sentiment['pos']} | Neu: {sentiment['neu']} | Neg: {sentiment['neg']} | Compound: {sentiment['compound']}"
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, f"Title: {title}\nLink: {link}\nSummary: {summary}\nSentiment: {sentiment_str}\n\n")
        self.text.config(state=tk.DISABLED)
        self.history.append({"Title": title, "URL": link, "Summary": summary, **sentiment})

    def stop_auto_search(self):
        if self.scraper:
            self.scraper_thread.join()
            self.scraper = None
            messagebox.showinfo("Stopped", "Automatic search stopped.")


root = tk.Tk()
app = StockScraperApp(root)
root.mainloop()
