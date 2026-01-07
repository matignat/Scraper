import argparse
import sys
import exceptions as exc
from scraper_logic import Scraper
import pandas as pd

class WikiScraperContoller:
    """
    Class controlling the operations based on called arguments.
    """

    def __init__(self, args):
        """Gets parsed user arguments"""
        self.args = args

    def run(self):
        """Decides on action to take based on arguments"""
    
        if self.args.summary:
            scraper = Scraper(self.args.summary)
            try:
                print(scraper.make_summary())
            except exc.ArticleNotFoundError as e:
                print(e)
            
        if self.args.table:
            if not self.args.number:
                print('Error: Table feature requires the number of the table (--number n).')
                sys.exit(1)
        
            scraper = Scraper(self.args.table)
            try:
                df = scraper.make_table(
                    number=self.args.number,
                    is_header=self.args.first_row_is_header
                )

                # Can't be only if df as DF objects cant be evaluated into bool
                if df is not None:
                    print(df)
                    print("\nFrequency of values (excluding headers):")
                    # Creates SQL like structure and counts unique values
                    # Delete empty slots and decrese dimension (to list)
                    values = df.values.flatten()
                    # Delete NaN
                    values = pd.Series(values).dropna()
                    # Count and display
                    freq = values.value_counts()
                    print(freq)
            except exc.ArticleNotFoundError as e:
                print(e)
            except exc.TableNotFoundError as e:
                print(e)

    # Used for integration test
    def get_scraper(self, phrase, local_path=None):
        return Scraper(phrase, local_html_path=local_path)

    def main():
        """Parses arguments and starts the programme"""
        parser = argparse.ArgumentParser()
        # Summary feature arguments
        parser.add_argument('--summary', help='Search phrase for summary')

        # Table feature arguments
        parser.add_argument('--table', help='Search phrase for the table')
        parser.add_argument('--number', type=int, help='The n-th table to be found (starts from 1)')
        parser.add_argument(
            '--first-row-is-header', 
            action='store_true',
            help='Treat the first row as column headers'
            )
        
        # Word count feature arguments
        parser.add_argument('--count-words', help='For each run adds word count to JSON file')
        
        # Frequency analysis arguments 
        parser.add_argument(
            '--analyze-relative-word-frequency', 
            action='store_true',
            help='Compare word usage frequency in the article with whole language frequency'
            )
        parser.add_argument(
            '--mode',
            choices=['article', 'language'], 
            help='Sort results by wiki frequency ("article") or general English frequency ("language")'
            )
        parser.add_argument('--count', type=int, help='Number of words to analyze')
        parser.add_argument("--chart", help='Path to save the generated chart')
        
        # Auto word count feature arguments
        parser.add_argument('--auto-count-words', help='Counts words on subpages')
        parser.add_argument('--depth', type=int, help='Depth of link graph to be traversed')
        parser.add_argument('--wait', type=int, help='Wait time between links')

        args = parser.parse_args()

        controller = WikiScraperContoller(args)
        controller.run()

if __name__ == "__main__":
    WikiScraperContoller.main()