class DoshomikError(ValueError):
    """Base exception for all doshomik errors."""


class ParseError(DoshomikError):
    """Raised when a numeric string cannot be parsed."""


class FormatError(DoshomikError):
    """Raised when an integer cannot be formatted."""
