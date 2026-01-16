import sys
from wiki_scraper import WikiScraperContoller
from scraper_logic import Scraper

class MockArgs:
    """
    A helper class to simulate the object returned by argparse.
    This allows us to test the Controller without actual command-line input.
    """
    # Test summary feature
    def __init__(self, summary=None, local_path=None):
        self.summary = summary
        self.local_path = local_path

def run_test():
    """
    Performs an integration test of the --summary functionality using local HTML file.
    """

    # Create our arguments (local path is not used by a controller itself it's just for the test)
    args = MockArgs(
        summary='Team Rocket',
        local_path='team_rocket.html'
    )

    try:
        controller = WikiScraperContoller(args)
        scraper = controller.get_scraper(args.summary, args.local_path)

        expected_start = 'Team Rocket'
        expected_end = 'outpost in the Sevil Islands.'

        result = scraper.make_summary()

        if not result.startswith(expected_start):
            raise AssertionError(f'Wrong starting phrase')

        if not result.endswith(expected_end):    
            raise AssertionError(f'Wrong ending phrase')

        print('Integration test PASSED!')
        sys.exit(0)

    # Catch assertion errors (exception subclasses)
    except Exception as e:
        print(f'Integration test FAILED: {e}')
        sys.exit(1)

# If this file has been ran directly run tests
if __name__ == '__main__':
    run_test()