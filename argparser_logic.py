import argparse   

def argparser(argv=None):
        """Parses arguments and starts the programme, returns Namespace of given argument """
        # Initializes parser and names programme for --help command
        parser = argparse.ArgumentParser(prog="wiki_scraper")

        # Commands are mutually exlusive - use subparsers
        subparsers = parser.add_subparsers(
            dest="command",
            required=True,
        )

        # --- summary ---
        p_summary = subparsers.add_parser("summary", help="Print first paragraph summary of an article")
        p_summary.add_argument("phrase", help="Search phrase for summary")

        # --- table ---
        p_table = subparsers.add_parser("table", help="Extract the n-th table from an article")
        p_table.add_argument("phrase", help="Search phrase for the table page")
        p_table.add_argument("--number", type=int, required=True, help="The n-th table to be found (starts from 1)")
        p_table.add_argument(
            "--first-row-is-header",
            dest="first_row_is_header",
            action="store_true",
            help="Treat the first row as column headers"
        )
        
        # --- count-words ---
        p_count = subparsers.add_parser("count-words", help="Count words on one page and add to JSON file")
        p_count.add_argument("phrase", help="Page to count words for")
        
        # --- analyze-relative-word-frequency ---
        p_analyze = subparsers.add_parser(
            "analyze-relative-word-frequency",
            help="Compare article word frequency with general language frequency"
        )
        p_analyze.add_argument("--mode", choices=["article", "language"], required=True,
                            help="Sort results by wiki frequency ('article') or general English frequency ('language')")
        p_analyze.add_argument("--count", type=int, required=True, help="Number of words to analyze")
        p_analyze.add_argument("--chart", required=False, help="Path to save the generated chart")
        
        # --- auto-count-words ---
        p_auto = subparsers.add_parser("auto-count-words", help="Recursively counts words on subpages")
        p_auto.add_argument("phrase", help="Start page")
        p_auto.add_argument("--depth", type=int, required=True, help="Depth of link graph to be traversed")
        p_auto.add_argument("--wait", type=float, required=True, help="Wait time between links")

        return parser.parse_args(argv)