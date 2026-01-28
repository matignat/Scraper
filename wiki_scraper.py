import pandas as pd

import exceptions as exc
from argparser_logic import arg_parser
from freq_analyzer import WikiAnalyzer
from scraper_logic import Scraper


class WikiScraperController:
    """
    Class controlling the operations based on called arguments.
    """

    def __init__(self, args, local_path=None):
        self.args = args
        self.local_path = local_path

    def table(self, scraper):
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

    # Controller logic
    def run(self):
        cmd = self.args.command

        try:
            scraper = Scraper(self.args.phrase, self.local_path)

            if cmd == "summary":
                res = scraper.make_summary()
                print(res)
                return res

            if cmd == "table":
                return self.table(scraper)

            if cmd == "count-words":
                return scraper.count_words()

            if cmd == "analyze-relative-word-frequency":
                analyzer = WikiAnalyzer()
                return analyzer.analyze_frequency(self.args.mode, self.args.count, self.args.chart)

            if cmd == "auto-count-words":
                return scraper.auto_count(self.args.depth, self.args.wait)

            raise exc.ArgumentError(f"Unknown command: {cmd}")

        except (exc.ArticleNotFoundError, exc.TableNotFoundError, exc.ArgumentError) as e:
            print(f"ERROR: {type(e).__name__}\n{e}")

# If explicitly called parse args and run programme
if __name__ == "__main__":
    args = arg_parser()
    controller = WikiScraperController(args)
    controller.run()