import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, scrolledtext, Canvas, ttk
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import threading
import time
from googlesearch import search
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import PyPDF2
import traceback
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class FinanceScraper:
    def __init__(self, company, nasdaq_code, seo_words, display_callback):
        self.company = company
        self.nasdaq_code = nasdaq_code
        self.seo_words = seo_words
        self.display_callback = display_callback
        self.history = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        ]

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def fetch_article_summary(self, url):
        headers = {'User-Agent': self.get_random_user_agent()}
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            summary = ' '.join([para.get_text() for para in paragraphs])
            return summary
        except Exception as e:
            print(f"Error fetching article: {e}")
            return ""

    def scrape_google_search(self):
        query = f"{self.company} {self.nasdaq_code} {' '.join(self.seo_words)} finance news"
        print(f"Starting search with query: {query}")
        time.sleep(random.uniform(2, 5))
        try:
            urls = []
            for url in search(query, num_results=10):
                urls.append(url)
                time.sleep(random.uniform(3, 7))
            print(f"Found {len(urls)} URLs to process")
            for url in urls:
                try:
                    print(f"Processing URL: {url}")
                    time.sleep(random.uniform(2, 4))
                    headers = {'User-Agent': self.get_random_user_agent()}
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    paragraphs = soup.find_all('p')
                    summary = ' '.join([para.get_text().strip() for para in paragraphs if para.get_text().strip()])
                    if summary and len(summary.strip()) > 0:
                        self.display_callback(self.company, url, summary)
                        self.history.append({
                            "Title": self.company,
                            "URL": url,
                            "Summary": summary
                        })
                        print(f"Successfully processed URL: {url}")
                    else:
                        print(f"No content found for URL: {url}")
                    time.sleep(random.uniform(5, 10))
                except requests.exceptions.RequestException as e:
                    print(f"Request error for {url}: {e}")
                    time.sleep(random.uniform(10, 15))
                    continue
                except Exception as e:
                    print(f"Error processing {url}: {e}")
                    time.sleep(random.uniform(10, 15))
                    continue
        except Exception as e:
            print(f"Error in scrape_google_search: {e}")
            time.sleep(random.uniform(15, 20))

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
        self.root.title("JLT Terminal")
        self.text_content = ""
        self.chunk_size = 5000
        self.current_position = 0
        self.history = []
        self.scraper_thread = None
        self.scraper = None
        self.sentiment_model = None
        self.sentiment_tokenizer = None
        self.sentiment_pipeline = None
        self.model_load_error = None
        self.last_sentiment_results = None
        self._load_sentiment_model()
        self.setup_frames()
        self.setup_buttons()
        self.setup_text_display()
        self.setup_icon()

    def _load_sentiment_model(self):
        try:
            self.sentiment_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
            self.sentiment_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
            self.sentiment_pipeline = pipeline("sentiment-analysis", model=self.sentiment_model, tokenizer=self.sentiment_tokenizer)
        except Exception as e:
            self.model_load_error = str(e)
            print(f"[ERROR] Failed to load FinBERT model: {e}")

    def setup_frames(self):
        self.left_frame = tk.Frame(self.root, width=200, relief=tk.RAISED, borderwidth=2, bg='white')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.right_frame = tk.Frame(self.root, bg='white')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def setup_buttons(self):
        tk.Label(self.left_frame, text="Select File:", bg='white').pack(fill=tk.X, padx=5)
        self.url_entry = tk.Entry(self.left_frame, width=20)
        self.url_entry.pack(fill=tk.X, padx=5)
        self.add_buttons()

    def add_buttons(self):
        commands = [
            ("Select File", self.load_from_file),
            ("Highlight Text", self.highlight_text),
            ("Unhighlight Text", self.unhighlight_text),
            ("Clear Screen", self.clear_screen),
            ("Sentiment Analysis", self.perform_sentiment_analysis),
            ("Visualize Sentiment", self.visualize_sentiment)
        ]
        for (text, command) in commands:
            tk.Button(self.left_frame, text=text, command=command, bg='red', fg='white').pack(fill=tk.X, padx=5, pady=5)

    def clear_screen(self):
        self.text_content = ""
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.config(state=tk.DISABLED)

    def setup_text_display(self):
        self.text = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, bg='black', fg='white')
        self.text.pack(fill=tk.BOTH, expand=True)

    def setup_icon(self):
        canvas = Canvas(self.left_frame, width=20, height=20, bg='white', highlightthickness=0)
        canvas.pack(side=tk.BOTTOM, pady=10, expand=True)

    def load_from_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            threading.Thread(target=self.read_file_thread, args=(file_path,)).start()

    def read_file_thread(self, file_path):
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
                text_content = df.to_string()
            elif file_path.endswith('.pdf'):
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in reader.pages:
                        text += page.extract_text() or ''
                    text_content = text
            else:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    text_content = file.read()
            self.root.after(0, lambda: self.on_file_loaded(text_content))
        except Exception as e:
            print("[ERROR] Failed to read file:")
            traceback.print_exc()
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to read file: {e}"))

    def on_file_loaded(self, text_content):
        self.text_content = text_content
        self.current_position = 0
        self.update_text_display()
        print("\n--- Loaded Text Content ---\n")
        try:
            print(self.text_content.encode('utf-8', errors='replace').decode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Could not print text content: {e}")
        self.root.after(0, lambda: self.perform_sentiment_analysis(auto=True, print_to_terminal=True))

    def update_text_display(self):
        if self.text_content:
            self.text.config(state=tk.NORMAL)
            self.text.delete(1.0, tk.END)
            try:
                self.text.insert(tk.END, self.text_content[self.current_position:self.current_position + self.chunk_size])
            except Exception:
                safe_text = self.text_content[self.current_position:self.current_position + self.chunk_size].encode('utf-8', errors='replace').decode('utf-8')
                self.text.insert(tk.END, safe_text)
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
            self.text.tag_config("highlight", background="yellow", foreground="black")

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

    def export_sentiment_csv(self):
        if not hasattr(self, 'last_sentiment_results') or not self.last_sentiment_results:
            messagebox.showerror("Error", "No sentiment analysis results to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.DataFrame(self.last_sentiment_results)
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Export Successful", f"Sentiment results exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export CSV: {e}")

    def perform_sentiment_analysis(self, auto=False, print_to_terminal=False):
        import numpy as np
        if not self.text_content:
            messagebox.showerror("Error", "No content loaded. Please load a file first.")
            return
        if self.model_load_error:
            messagebox.showerror("Model Load Error", f"Failed to load FinBERT model: {self.model_load_error}")
            return
        if not self.sentiment_pipeline:
            messagebox.showerror("Model Error", "FinBERT sentiment pipeline is not available.")
            return
        soup = BeautifulSoup(self.text_content, 'html.parser')
        webpage_text = soup.get_text()
        sentences = [s.strip() for s in re.split(r'[.!?]', webpage_text) if s.strip()]
        if not sentences:
            messagebox.showerror("Error", "No sentences found for sentiment analysis.")
            return
        sentiments = []
        pos_count, neg_count, neu_count = 0, 0, 0
        sentiment_records = []
        sentiment_numeric = []
        weighted_sum = 0
        weighted_total = 0
        for idx, sent in enumerate(sentences):
            try:
                result = self.sentiment_pipeline(sent[:512])[0]
                sentiments.append(result)
                label = result['label'].upper()
                score = result['score']
                sentiment_records.append({
                    'Sentence': sent,
                    'Sentiment': label,
                    'Score': score
                })
                if label == 'POSITIVE':
                    pos_count += 1
                    sentiment_numeric.append(1)
                elif label == 'NEGATIVE':
                    neg_count += 1
                    sentiment_numeric.append(-1)
                else:
                    neu_count += 1
                    sentiment_numeric.append(0)
                if label == 'POSITIVE':
                    weighted_sum += score * 1
                elif label == 'NEGATIVE':
                    weighted_sum += score * -1
                weighted_total += score
            except Exception as e:
                print(f"[ERROR] Sentiment analysis failed for sentence: {sent}\n{e}")
                continue
        total = max(1, len(sentiments))
        pos_ratio = pos_count / total
        neg_ratio = neg_count / total
        neu_ratio = neu_count / total
        overall_score = np.mean(sentiment_numeric) if sentiment_numeric else 0
        volatility = np.std(sentiment_numeric) if sentiment_numeric else 0
        weighted_sentiment = weighted_sum / weighted_total if weighted_total > 0 else 0
        half = len(sentiment_numeric) // 2
        first_half_score = np.mean(sentiment_numeric[:half]) if half > 0 else 0
        second_half_score = np.mean(sentiment_numeric[half:]) if half > 0 else 0
        momentum = second_half_score - first_half_score
        if pos_ratio > neg_ratio and pos_ratio > neu_ratio:
            stock_msg = "Stock likely to go up."
        elif neg_ratio > pos_ratio and neg_ratio > neu_ratio:
            stock_msg = "Stock likely to go down."
        else:
            stock_msg = "Stock likely to remain stable."
        sentiment_msg = (
            f"FinBERT Sentiment Analysis:\n"
            f"Positive: {pos_count} ({pos_ratio:.2%}) | Negative: {neg_count} ({neg_ratio:.2%}) | Neutral: {neu_count} ({neu_ratio:.2%})\n"
            f"\nMath-based Sentiment Metrics:\n"
            f"Overall Score (mean): {overall_score:.2f}\n"
            f"Weighted Sentiment: {weighted_sentiment:.2f}\n"
            f"Sentiment Volatility (std): {volatility:.2f}\n"
            f"Momentum (2nd half - 1st half): {momentum:.2f}\n"
            f"\n{stock_msg}"
        )
        self.last_sentiment_results = sentiment_records
        if print_to_terminal:
            print("\n--- FinBERT Sentiment Analysis Result ---\n")
            print(sentiment_msg)
        sentiment_window = tk.Toplevel()
        sentiment_window.title("Sentiment Analysis Results (FinBERT)")
        results_text = tk.Text(sentiment_window, wrap=tk.WORD)
        results_text.insert(tk.END, sentiment_msg)
        results_text.pack(fill=tk.BOTH, expand=True)
        sentiment_window.mainloop()

    def visualize_sentiment(self):
        if not hasattr(self, 'last_sentiment_results') or not self.last_sentiment_results:
            messagebox.showerror("Error", "No sentiment analysis results to visualize.")
            return
        sentiment_window = tk.Toplevel()
        sentiment_window.title("Visualize Sentiment")
        df = pd.DataFrame(self.last_sentiment_results)
        sentiment_counts = df['Sentiment'].value_counts()
        stats_text = f"Statistics:\n"
        stats_text += f"Total Sentences: {len(df)}\n"
        stats_text += f"Sentiment Distribution:\n{sentiment_counts.to_string()}\n"
        stats_frame = tk.Frame(sentiment_window)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        stats_label = tk.Label(stats_frame, text=stats_text, justify=tk.LEFT)
        stats_label.pack(padx=10, pady=10)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(x='Sentiment', data=df, palette='Set2', ax=ax)
        ax.set_title('Sentiment Distribution')
        canvas = FigureCanvasTkAgg(fig, master=sentiment_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def display_article(self, title, link, summary, sentiment):
        sentiment_str = f"Pos: {sentiment['pos']:.2f} | Neu: {sentiment['neu']:.2f} | Neg: {sentiment['neg']:.2f} | Compound: {sentiment['compound']:.2f}"
        
        display_text = f"\n{'='*80}\n"
        display_text += f"Title: {title}\n"
        display_text += f"Link: {link}\n"
        display_text += f"Summary: {summary[:500]}...\n"
        display_text += f"Sentiment: {sentiment_str}\n"
        display_text += f"{'='*80}\n"

        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, display_text)
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)
        
        self.root.update_idletasks()
        
        self.history.append({
            "Title": title,
            "URL": link,
            "Summary": summary,
            "Positive Words": ', '.join([word for word, score in sentiment.items() if score > 0.05]),
            "Negative Words": ', '.join([word for word, score in sentiment.items() if score < -0.05]),
            "Overall Sentiment": "Good" if sentiment['compound'] >= 0.05 else "Bad" if sentiment['compound'] <= -0.05 else "Moderate"
        })
        
        print(f"Displayed article: {title}")

root = tk.Tk()
app = StockScraperApp(root)
root.mainloop()
