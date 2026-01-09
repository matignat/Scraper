import requests
import exceptions as exc
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
from bs4 import Tag
import re
import json
from pathlib import Path

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

    def __init__(self, phrase, base_url="https://bulbapedia.bulbagarden.net", local_html_path=None):
        self.phrase = phrase.replace(' ', '_')
        self.base_url = base_url
        self.local_html_path = local_html_path

    # Fetch HTML as text either from a local file or from internet using requests
    def get_source(self): 
        if self.local_html_path:
            with open(self.local_html_path, 'r', encoding='utf-8') as file:
                return file.read()
            
        url = f'{self.base_url}/wiki/{self.phrase}'
        
        try:
            source = requests.get(url)
            # 200 is the only success code so return None if article doesn't exist
            if source.status_code != 200:
                return None
            return source.text
        # Catch errors from requests package (connection error, wrong url ...)
        except requests.RequestException:
            return None
    
    def make_summary(self):
        """
        Finds the first paragraph of the article for chosen phrase.
        Ignores HTML tags and returns only string from the paragraph.
        """
        html_struct = self.get_source()
        if not html_struct:
            raise exc.ArticleNotFoundError(f'No article for phrase "{self.phrase}" found.')
        
        soup = BeautifulSoup(html_struct, 'html.parser')
        # All wikis on MediaWiki software (Bulbapedia too) have main content in section chosen below
        content = soup.find('div', class_='mw-parser-output')

        if content:
            first_p = content.find('p')
            if first_p: 
                return first_p.get_text(strip=True)
        
        raise exc.ArticleNotFoundError(f'No summary for phrase "{self.phrase}" can be found')
    
    def make_table(self, number, is_header=False):
        """
        Extracts the n-th table from the wiki page and saves it as a CSV file.
        """
        html_struct = self.get_source()
        if not html_struct:
            raise exc.ArticleNotFoundError(f'No article for phrase "{self.phrase}" found.')
        
        soup = BeautifulSoup(html_struct, 'html.parser')
        content = soup.find('div', class_='mw-parser-output')

        if not content:
            raise exc.ArticleNotFoundError("Could not find article content area.")
        
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
        html_struct = self.get_source()
        if not html_struct:
            raise exc.ArticleNotFoundError(f'No article for phrase "{self.phrase}" found.')
        
        soup = BeautifulSoup(html_struct, 'html.parser')
        content = soup.find('div', class_='mw-parser-output')

        if not content:
            raise exc.ArticleNotFoundError("Could not find article content area.")
        
        text = content.get_text()

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



        

