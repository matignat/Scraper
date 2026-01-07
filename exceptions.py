class ScraperError(Exception):
    """Base ERROR"""
    pass

class ArticleNotFoundError(ScraperError):
    """Thrown when no article found for given phrase"""
    pass

class TableNotFoundError(ScraperError):
    """Thrown if no table of given number found"""
    pass