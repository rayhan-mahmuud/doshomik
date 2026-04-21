from __future__ import annotations

from doshomik._constants import BANGLA_DIGITS, ENGLISH_DIGITS
from doshomik._exceptions import FormatError

__all__ = ["format"]

_TO_BANGLA = str.maketrans(ENGLISH_DIGITS, BANGLA_DIGITS)

_VALID_SCRIPTS = {"bangla", "english"}
_VALID_GROUPINGS = {"lakh", "western", "none"}


def format(n: int, *, script: str = "bangla", grouping: str = "lakh") -> str:
    """Format an integer as a South Asian numeric string.

    Args:
        n: The integer to format. Booleans are rejected.
        script: "bangla" or "english".
        grouping: "lakh" (2-2-3 from right), "western" (3-3-3), or "none".

    Raises:
        FormatError: if n is not a plain int, or arguments are invalid.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise FormatError(f"n must be int, got {type(n).__name__}")
    if script not in _VALID_SCRIPTS:
        raise FormatError(f"script must be 'bangla' or 'english', got {script!r}")
    if grouping not in _VALID_GROUPINGS:
        raise FormatError(f"grouping must be 'lakh', 'western', or 'none', got {grouping!r}")

    sign = "-" if n < 0 else ""
    abs_n = abs(n)

    if grouping == "lakh":
        digits = _group_lakh(str(abs_n))
    elif grouping == "western":
        digits = f"{abs_n:,}"
    else:
        digits = str(abs_n)

    if script == "bangla":
        digits = digits.translate(_TO_BANGLA)

    return sign + digits


def _group_lakh(s: str) -> str:
    r = s[::-1]
    chunks = [r[:3]] + [r[i : i + 2] for i in range(3, len(r), 2)]
    return ",".join(c[::-1] for c in reversed(chunks))
