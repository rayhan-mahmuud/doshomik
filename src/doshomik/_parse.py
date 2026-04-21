
__all__ = ["parse"]


def parse(s: str) -> int:
    """Parse a South Asian numeric string and return an integer.

    Supports Bangla and English digits, lakh/crore multipliers, and common
    spelling variants. Currency markers (৳, taka, etc.) are ignored.

    Raises ParseError if the string cannot be interpreted as an integer.
    """
    raise NotImplementedError("parse is not yet implemented — coming in phase 2")
