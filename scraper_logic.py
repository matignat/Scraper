import json
import re
import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

import exceptions as exc

# Helps with display
pd.set_option("display.width", None)
pd.set_option("display.max_columns", None)


class Scraper:
    """
    A class used to represent a Wiki Scraper for a Bulbapedia Pokemon fan wiki.
    
    Attributes:
        phrase (str): The search phrase provided by the user.
        local_html_path (str): Optional path to a local HTML file for offline testing.
    """

    def __init__(self, phrase, local_html_path=None):
        self.phrase = phrase.replace(" ", "_")
        self.local_html_path = local_html_path

    # Fetch HTML as text either from a local file or from internet using requests and return text
    def get_source(self): 
        if self.local_html_path:
            with open(self.local_html_path, "r", encoding="utf-8") as file:
                text = file.read()
        else:
            base_url = "https://bulbapedia.bulbagarden.net/wiki/"
            url = f"{base_url}{self.phrase}"
            
            try:
                source = requests.get(url)
            # Catch errors from requests package (connection error, wrong url ...)
            except requests.RequestException:
                raise exc.ArticleNotFoundError
            
            if source.status_code != requests.codes.ok:
                raise exc.ArticleNotFoundError(f"No article for phrase '{self.phrase}' found.")
            
            text = source.text
            
        # All wikis on MediaWiki software (Bulbapedia too) have main content in section chosen below
        soup = BeautifulSoup(text, "html.parser")
        content = soup.find("div", id="mw-content-text")

        if content is None:
            raise exc.ArticleNotFoundError("Could not find article content area.")

        return content
    
    def make_summary(self):
        """
        Finds the first paragraph of the article for chosen phrase.
        Ignores HTML tags and returns only string from the paragraph.
        """
        content = self.get_source()

        # Finds first paragraph (Tag type)
        first_p = content.find("p")

        if first_p: 
            text = first_p.get_text(" ", strip=True)
            # Deletes additional spaces before dots etc.
            text = re.sub(r"\s+([.,!?;:])", r"\1", text)
            return text
        
        raise exc.ArticleNotFoundError(f"No summary for phrase '{self.phrase}' can be found")
    
    def make_table(self, number, is_header=False):
        """
        Extracts the n-th table from the wiki page and saves it as a CSV file.
        """
        content = self.get_source()
        tables = content.find_all("table")

        if number < 1 or number > len(tables):
            raise exc.TableNotFoundError(f"Table number {number} not found. There are {len(tables)} tables.")

        # Conversion to string so we can work with pandas (doesn't work with BS object)
        target = tables[number - 1]

        target = str(target)

        # Pandas returns list of DF we only have one
        # Use StringIO to wrap HTML (deprecated warning)
        df = pd.read_html(StringIO(target), header=0 if is_header else None)[0]

        df = df.dropna(axis=1, how="all")
        df = df.dropna(axis=0, how="all")
        df.set_index(df.columns[0], inplace=True)

        file_name = f"{self.phrase}.csv"
        df.to_csv(file_name)

        return df
    
    def count_words(self):
        text = self.get_source().get_text(" ", strip=True)
        # Use regex to cut only words and make Upper case = Lower case
        words = re.findall(r"[^\W\d_]+", text.lower())

        file_path = Path(__file__).resolve().parent / "./word-counts.json"
        word_counts = {}

        # Try opening word-count.json
        if file_path.exists():
            with file_path.open("r", encoding="utf-8") as f:
                word_counts = json.load(f)

        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        with file_path.open("w", encoding="utf-8") as f:
            # Sort the file
            sorted_data = dict(sorted(word_counts.items(), key=lambda kv: kv[1], reverse=True))
            # Ensure ascii for letters like é
            json.dump(sorted_data, f, indent=1, ensure_ascii=False)

    # Recursively counts words using links
    def auto_count(self, n, t, i=0, visited=None):
        if visited is None:
            visited = set()

        if n < 0 or t < 0: 
            raise exc.ArgumentError("Depth and time parameters have to be >= 0!")

        if i > n:
            return
        
        if self.phrase in visited:
            return
        
        visited.add(self.phrase)

        print(f"Counting phrase: {self.phrase}")
        self.do_count_words()

        time.sleep(t)

        content = self.get_source()
        links = content.find_all("a", href=True)

        # We reached max depth
        if i == n:
            return

        # Recursive call for links on site
        for l in links:
            href = l.get("href")
            if not href or not href.startswith("/wiki/"):
                continue
            
            # Delete /wiki/ prefix
            next_phrase = href[len("/wiki/"):]

            # Skip namespaces 
            if ":" in next_phrase:
                continue

            child = Scraper(next_phrase)
            child.auto_count(n, t, i + 1, visited)
