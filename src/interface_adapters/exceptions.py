class InvalidUrlError(Exception):
    pass


class PageLoadingError(Exception):
    pass


class InvalidExcelFileStructure(Exception):
    pass


class ParserError(Exception):
    """Custom exception raised when parsing fails due to missing required fields."""
    pass
