class ScraperError(Exception):
    """Base ERROR for scraper"""
    pass

class ControllerError(Exception):
    """Base ERROR for controller module"""

class ArticleNotFoundError(ScraperError):
    """Thrown when no article found for given phrase"""
    pass

class TableNotFoundError(ScraperError):
    """Thrown if no table of given number found"""
    pass

class ArgumentError(ControllerError):
    """Thrown when wrong / not all required arguments passed by user"""
    pass