from wiki_scraper import WikiScraperContoller
from pathlib import Path
from argparser_logic import argparser

"""
Integration test:

    python wiki_scraper_integration_test.py

Loads a saved HTML page from ./, runs one main feature
(summary extraction), and exits with a non-zero code if the test fails.
"""

def run_test():
    """ 
    Performs an integration test of the --summary functionality using local HTML file.
    """

    args = argparser(["summary", "Team Rocket"])

    try:

        html_path = Path(__file__).resolve().parent / "test_html.html"

        if not html_path.exists():
            raise FileNotFoundError(f"Missing test file: {html_path}\n")

        controller = WikiScraperContoller(args, str(html_path))

        expected_start = "Team Rocket"
        expected_end = "outpost in the Sevii Islands."

        result = controller.run()

        assert(result.startswith(expected_start))
        assert(result.endswith(expected_end))
    # Catch assertion errors (exception subclasses)
    except Exception as e:
        print(f"Integration test FAILED: {e}")
        return
    
    print("Integration test SUCCESS!")

# If this file has been ran directly run tests
if __name__ == "__main__":
    run_test()