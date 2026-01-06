import requests
from bs4 import BeautifulSoup

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
    
    def get_summary(self):
        """
        Finds the first paragraph of the article for chosen phrase.
        Ignores HTML tags and returns only string from the paragraph.
        """
        html_struct = self.get_source()
        if not html_struct:
            return f'ERROR: Article for "{self.phrase}" not found.'
        
        soup = BeautifulSoup(html_struct, 'html.parser')
        content = soup.find('div', class_='mw-parser-output')

        if content:
            first_p = content.find('p')
            if first_p: 
                return first_p.get_text(strip=True)
        
        return 'No summary for this phrase.'
    
    