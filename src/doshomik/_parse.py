from __future__ import annotations

from decimal import Decimal

from doshomik._exceptions import ParseError
from doshomik._tokens import Currency, Multiplier, Number, Token, tokenize

__all__ = ["parse"]


def parse(s: str) -> int:
    """Parse a South Asian numeric string and return an integer.

    Supports Bangla and English digits, lakh/crore multipliers, and common
    spelling variants. Currency markers (৳, taka, etc.) are ignored.

    Raises ParseError if the string cannot be interpreted as an integer.
    """
    if not isinstance(s, str):
        raise ParseError(f"expected str, got {type(s).__name__}")
    tokens: list[Token] = [t for t in tokenize(s) if not isinstance(t, Currency)]
    if not tokens:
        raise ParseError(f"no numeric content found in {s!r}")
    return _reduce(tokens)


def _reduce(tokens: list[Token]) -> int:
    total = Decimal(0)
    i = 0
    while i < len(tokens):
        match tokens[i]:
            case Number(value=v):
                if i + 1 < len(tokens):
                    match tokens[i + 1]:
                        case Multiplier(value=m):
                            total += v * m
                            i += 2
                        case _:
                            total += v
                            i += 1
                else:
                    total += v
                    i += 1
            case Multiplier():
                raise ParseError("multiplier without a preceding number")
            case _:
                i += 1
    if total != total.to_integral_value():
        raise ParseError(f"result is not an integer: {total}")
    return int(total)
