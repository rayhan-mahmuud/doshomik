
__all__ = ["format"]


def format(n: int, *, script: str = "bangla", grouping: str = "lakh") -> str:
    """Format an integer as a South Asian numeric string.

    Args:
        n: The integer to format. Must not be a bool.
        script: "bangla" or "english".
        grouping: "lakh" (2-2-3 from right), "western" (3-3-3), or "none".

    Raises FormatError if n is not an int or arguments are invalid.
    """
    raise NotImplementedError("format is not yet implemented — coming in phase 3")
