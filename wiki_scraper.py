import argparse
import sys
import exceptions as exc
from scraper_logic import Scraper
import pandas as pd
from freq_analyzer import WikiAnalyzer

class WikiScraperContoller:
    """
    Class controlling the operations based on called arguments.
    """

    def __init__(self, args):
        """Gets parsed user arguments"""
        self.args = args

    # Fucntion used for handling table argument
    def table_arg(self):
        if not self.args.number:
                raise exc.ArgumentError('Table feature requires the number of the table (--number n).')
        
        scraper = Scraper(self.args.table)

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

    # Used for handling frequency anaysis
    def an_freq_arg(self):
        # No choices check - argparse does it
        if not self.args.mode:
            raise exc.ArgumentError('Frequency analysis requires the mode argument!.')
        
        if not self.args.count:
            raise exc.ArgumentError('Frequency analysis requires the count argument!.')
        
        analyzer = WikiAnalyzer()
        analyzer.analyze_frequency(self.args.mode, self.args.count, self.args.chart) 

    # Controller logic
    def run(self):
        """Decides on action to take based on arguments"""

        # Make summary
        if self.args.summary:
            scraper = Scraper(self.args.summary)
            try:
                print(scraper.make_summary())
            except exc.ArticleNotFoundError as e:
                print(e)
        
        # Make table
        if self.args.table:
            try:
                self.table_arg()
            except (exc.ArticleNotFoundError, exc.TableNotFoundError, exc.ArgumentError) as e:
                print(f"ERROR: {type(e).__name__} \n{e}")
        
        # Count words
        if self.args.count_words:
            scraper = Scraper(self.args.count_words)
            try:
                scraper.do_count_words()
            except exc.ArticleNotFoundError as e:
                print(e)

        # Frequency analysis
        if self.args.analyze_relative_word_frequency:
            try:
                self.an_freq_arg()
            except (exc.ArticleNotFoundError, exc.ArgumentError) as e:
                print(f"ERROR: {type(e).__name__} \n{e}")

    # Used for integration test
    def get_scraper(self, phrase, local_path=None):
        return Scraper(phrase, local_html_path=local_path)

    def main():
        """Parses arguments and starts the programme"""
        parser = argparse.ArgumentParser()
        # Summary feature arguments
        parser.add_argument('--summary', help='Search phrase for summary')

        # Table feature arguments
        parser.add_argument('--table', help='Search phrase for the n-th table (number required!)')
        parser.add_argument('--number', type=int, help='The n-th table to be found (starts from 1)')
        parser.add_argument(
            '--first-row-is-header', 
            dest='first_row_is_header',
            action='store_true',
            help='Treat the first row as column headers'
            )
        
        # Word count feature arguments
        parser.add_argument('--count-words', dest="count_words", help='For each run adds word count to JSON file')
        
        # Frequency analysis arguments 
        parser.add_argument(
            '--analyze-relative-word-frequency', 
            dest='analyze_relative_word_frequency',
            action='store_true',
            help='Compare word usage frequency in the article with Wiki\'s language frequency (mode and count required!)'
            )
        parser.add_argument(
            '--mode',
            choices=['article', 'language'], 
            help='Sort results by wiki frequency ("article") or general English frequency ("language")'
            )
        parser.add_argument('--count', type=int, help='Number of words to analyze')
        parser.add_argument("--chart", help='Path to save the generated chart')
        
        # Auto word count feature arguments
        parser.add_argument(
            '--auto-count-words',
            dest='auto_count_words', 
            help='Counts words on subpages (depth and wait required!)'
            )
        parser.add_argument('--depth', type=int, help='Depth of link graph to be traversed')
        parser.add_argument('--wait', type=int, help='Wait time between links')

        args = parser.parse_args()

        controller = WikiScraperContoller(args)
        controller.run()

if __name__ == "__main__":
    WikiScraperContoller.main()