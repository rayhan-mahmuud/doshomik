from __future__ import annotations

import contextlib
import re
import unicodedata
from collections.abc import Iterator
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from doshomik._constants import CURRENCY_MARKERS, DIGIT_MAP, MULTIPLIERS

__all__ = ["Currency", "Multiplier", "Number", "Token", "tokenize"]


@dataclass
class Number:
    value: Decimal


@dataclass
class Multiplier:
    value: int


@dataclass
class Currency:
    text: str


Token = Number | Multiplier | Currency

# After normalization, Bangla digits are already replaced with ASCII digits,
# so [0-9] is sufficient — no need for \d (which also matches Bangla digits).
_TOKEN_RE = re.compile(
    r"(?P<number>[0-9][0-9,]*(?:\.[0-9]+)?)"
    # Match any non-digit, non-whitespace, non-comma run as a word token.
    # This covers ASCII words, Bangla words (letters + combining vowel marks),
    # and currency symbols like ৳ — all in one pattern.
    r"|(?P<word>[^\d\s,]+)",
    re.UNICODE,
)


def _normalize(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = "".join(DIGIT_MAP.get(ch, ch) for ch in s)
    return s.lower()


def tokenize(s: str) -> Iterator[Token]:
    for match in _TOKEN_RE.finditer(_normalize(s)):
        num_str = match.group("number")
        if num_str is not None:
            clean = num_str.replace(",", "")
            with contextlib.suppress(InvalidOperation):
                yield Number(Decimal(clean))
            continue

        word = match.group("word")
        if word is not None:
            key = word.rstrip(".")
            if key in MULTIPLIERS:
                yield Multiplier(MULTIPLIERS[key])
            elif key in CURRENCY_MARKERS or word in CURRENCY_MARKERS:
                yield Currency(key)
