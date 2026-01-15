import requests
import exceptions as exc
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
from bs4 import Tag
import re
import json
from pathlib import Path
import time

# Helps with display
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


class Scraper:
    """
    A class used to represent a Wiki Scraper for a Bulbapedia Pokemon fan wiki.
    
    Attributes:
        phrase (str): The search phrase provided by the user.
        base_url (str): The base URL of the wiki being scraped.
        local_html_path (str): Optional path to a local HTML file for offline testing.
    """

    def __init__(self, phrase, base_url='https://bulbapedia.bulbagarden.net/wiki/', local_html_path=None):
        self.phrase = phrase.replace(' ', '_')
        self.base_url = base_url
        self.local_html_path = local_html_path

    # Fetch HTML as text either from a local file or from internet using requests and return text
    def get_source(self): 
        if self.local_html_path:
            with open(self.local_html_path, 'r', encoding='utf-8') as file:
                return file.read()
            
        url = f'{self.base_url}{self.phrase}'
        
        try:
            source = requests.get(url)
        # Catch errors from requests package (connection error, wrong url ...)
        except requests.RequestException:
            raise exc.ArticleNotFoundError
        
        # 200 is the only success code so return None if article doesn't exist
        if source.status_code != 200:
                raise exc.ArticleNotFoundError(f'No article for phrase "{self.phrase}" found.')

        if source is None:
            raise exc.ArticleNotFoundError(f'No article for phrase "{self.phrase}" found.')
        
        # All wikis on MediaWiki software (Bulbapedia too) have main content in section chosen below
        soup = BeautifulSoup(source.text, 'html.parser')
        content = soup.find('div', class_='mw-parser-output')

        if content is None:
            raise exc.ArticleNotFoundError('Could not find article content area.')

        return content
    
    def make_summary(self):
        """
        Finds the first paragraph of the article for chosen phrase.
        Ignores HTML tags and returns only string from the paragraph.
        """
        content = self.get_source()

        # Finds first paragraph (Tag type)
        first_p = content.find('p')

        if first_p: 
            return first_p.get_text(strip=True)
        
        raise exc.ArticleNotFoundError(f'No summary for phrase "{self.phrase}" can be found')
    
    def make_table(self, number, is_header=False):
        """
        Extracts the n-th table from the wiki page and saves it as a CSV file.
        """
        content = self.get_source()
        tables = content.find_all('table')

        if number < 1 or number > len(tables):
            raise exc.TableNotFoundError(f'Table number {number} not found. There are {len(tables)} tables.')

        
        # Conversion to string so we can work with pandas (doesn't work with BS object)
        target = tables[number - 1]

        target = str(target)

        # Pandas returns list of DF we only have one
        # Use StringIO to wrap HTML (deprecated warning)
        df = pd.read_html(StringIO(target), header=0 if is_header else None)[0]

        df = df.dropna(axis=1, how='all')
        df = df.dropna(axis=0, how='all')
        df.set_index(df.columns[0], inplace=True)

        file_name = f'{self.phrase}.csv'
        df.to_csv(file_name)

        return df
    
    def do_count_words(self):
        text = self.get_source().get_text(strip=True)
        # Use regex to cut only words and make Upper case = Lower case
        words = re.findall(r'\w+', text.lower())

        file_path = Path(__file__).resolve().parent / './word-counts.json'
        word_counts = {}

        if file_path.exists():
            with file_path.open('r', encoding='utf-8') as f:
                word_counts = json.load(f)

        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        with file_path.open('w', encoding='utf-8') as f:
            # Ensure ascii for letters like é
            json.dump(word_counts, f, indent=1, ensure_ascii=False)

    # Recursively counts words using links
    def auto_count(self, n, t, i=0, visited=None):
        if visited is None:
            visited = set()

        if n < 0 or t < 0: 
            raise exc.ArgumentError('Depth and time parameters have to be >= 0!')

        if i > n:
            return
        
        if self.phrase in visited:
            return
        
        visited.add(self.phrase)

        print(f'Counting phrase: {self.phrase}')
        self.do_count_words()

        time.sleep(t)

        content = self.get_source()
        links = content.find_all('a', href=True)

        # We reached max depth
        if i == n:
            return
    
        for l in links:
            href = l.get('href')
            if not href or not href.startswith('/wiki/'):
                continue

            self.phrase = href

            self.auto_count(n, t, i + 1, visited)
