# ruff: noqa: RUF001  # intentional Bangla digit characters in test strings
from decimal import Decimal

import pytest

from doshomik._tokens import Currency, Multiplier, Number, Token, tokenize


@pytest.mark.parametrize(
    "s, expected",
    [
        # single digit
        ("1", [Number(Decimal("1"))]),
        ("০", [Number(Decimal("0"))]),
        ("৯", [Number(Decimal("9"))]),
        # Bangla word multiplier
        ("১ কোটি", [Number(Decimal("1")), Multiplier(10_000_000)]),
        ("১ হাজার", [Number(Decimal("1")), Multiplier(1_000)]),
        ("১ লাখ", [Number(Decimal("1")), Multiplier(100_000)]),
        ("১ লক্ষ", [Number(Decimal("1")), Multiplier(100_000)]),
        # English word multipliers
        ("2.5 crore", [Number(Decimal("2.5")), Multiplier(10_000_000)]),
        ("1 lakh", [Number(Decimal("1")), Multiplier(100_000)]),
        ("1 million", [Number(Decimal("1")), Multiplier(1_000_000)]),
        # grouping commas are stripped into a single NUMBER token
        ("1,25,000", [Number(Decimal("125000"))]),
        ("1,000,000", [Number(Decimal("1000000"))]),
        # currency markers produce Currency tokens and are then ignored by parse
        ("৳ 500", [Currency("৳"), Number(Decimal("500"))]),
        ("500 taka", [Number(Decimal("500")), Currency("taka")]),
        ("500 tk.", [Number(Decimal("500")), Currency("tk")]),
        # compound
        (
            "১ কোটি ২৫ লক্ষ",
            [
                Number(Decimal("1")),
                Multiplier(10_000_000),
                Number(Decimal("25")),
                Multiplier(100_000),
            ],
        ),
        # unknown words are silently dropped
        ("100 apples", [Number(Decimal("100"))]),
        # whitespace-only produces nothing
        ("   ", []),
    ],
)
def test_tokenize(s: str, expected: list[Token]) -> None:
    assert list(tokenize(s)) == expected
