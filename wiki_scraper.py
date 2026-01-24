from argparser_logic import argparser
import exceptions as exc
from scraper_logic import Scraper
import pandas as pd
from freq_analyzer import WikiAnalyzer

class WikiScraperContoller:
    """
    Class controlling the operations based on called arguments.
    """

    def __init__(self, args, local_path=None):
        self.args = args
        self.local_path = local_path

    def count_words(self):
        scraper = Scraper(self.args.phrase, self.local_path)
        return scraper.do_count_words()

    def summary(self):
        scraper = Scraper(self.args.phrase,self.local_path)
        res = scraper.make_summary()
        print(res)
        return res

    def table(self):    
        scraper = Scraper(self.args.phrase, self.local_path)

        df = scraper.make_table(
            number=self.args.number,
            is_header=self.args.first_row_is_header
        )

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

        return df

    # Used for handling frequency anaysis
    def an_freq(self):
        analyzer = WikiAnalyzer()
        return analyzer.analyze_frequency(self.args.mode, self.args.count, self.args.chart)

    # Used for handling auto count
    def auto_count(self):
        scraper = Scraper(self.args.phrase, self.local_path)
        return scraper.auto_count(self.args.depth, self.args.wait)

    # Controller logic
    def run(self):
        cmd = self.args.command

        try:
            if cmd == "summary":
                return self.summary()

            elif cmd == "table":
                return self.table()

            elif cmd == "count-words":
                return self.count_words()

            elif cmd == "analyze-relative-word-frequency":
                return self.an_freq()

            elif cmd == "auto-count-words":
                return self.auto_count()

            else:
                raise exc.ArgumentError(f"Unknown command: {cmd}")

        except (exc.ArticleNotFoundError, exc.TableNotFoundError, exc.ArgumentError) as e:
            print(f"ERROR: {type(e).__name__}\n{e}")

    # Used for integration test
    def get_scraper(self, phrase, local_path=None):
        return Scraper(phrase, local_html_path=local_path)

if __name__ == "__main__":
    args = argparser()
    controller = WikiScraperContoller(args)
    controller.run()