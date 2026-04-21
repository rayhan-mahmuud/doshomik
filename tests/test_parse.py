# ruff: noqa: RUF001  # intentional Bangla digit characters in test strings
import pytest

from doshomik import parse
from doshomik._exceptions import ParseError


@pytest.mark.parametrize(
    "s, expected",
    [
        # bare digits — English
        ("0", 0),
        ("1", 1),
        ("100", 100),
        ("999", 999),
        # bare digits — Bangla
        ("০", 0),
        ("৯", 9),
        ("১০", 10),
        ("১০০", 100),
        # thousands
        ("1 hazar", 1_000),
        ("1 hajar", 1_000),
        ("1 thousand", 1_000),
        ("১ হাজার", 1_000),
        ("2.5 hazar", 2_500),
        # lakhs
        ("1 lakh", 100_000),
        ("1 lac", 100_000),
        ("1 lakhs", 100_000),
        ("১ লাখ", 100_000),
        ("১ লক্ষ", 100_000),
        ("2.5 lakh", 250_000),
        # crores
        ("1 crore", 10_000_000),
        ("1 crores", 10_000_000),
        ("১ কোটি", 10_000_000),
        ("2.5 crore", 25_000_000),
        # compound — the core use-case
        ("১ কোটি ২৫ লক্ষ", 12_500_000),
        ("1 crore 25 lakh", 12_500_000),
        ("2 crore 50 lakh", 25_000_000),
        ("1 crore 50 lakh 25 hazar", 15_025_000),
        # grouping commas (lakh and western styles)
        ("1,25,000", 125_000),
        ("1,000,000", 1_000_000),
        ("10,00,000", 1_000_000),
        # decimal multipliers
        ("1.5 crore", 15_000_000),
        ("1.5 lakh", 150_000),
        ("2.5 hazar", 2_500),
        # currency markers stripped
        ("৳ 500", 500),
        ("500 taka", 500),
        ("500 tk.", 500),
        ("টাকা 1000", 1_000),
        ("bdt 250", 250),
        # millions and billions (English BD press)
        ("1 million", 1_000_000),
        ("1.5 million", 1_500_000),
        ("1 billion", 1_000_000_000),
        # mixed script
        ("১০ lakh", 1_000_000),
        ("10 লাখ", 1_000_000),
        # zero
        ("0 lakh", 0),
    ],
)
def test_parse_valid(s: str, expected: int) -> None:
    assert parse(s) == expected


@pytest.mark.parametrize(
    "s",
    [
        "",  # empty string
        "   ",  # whitespace only
        "abc",  # no numeric content
        "লাখ",  # multiplier with no preceding number
        "crore",  # multiplier with no preceding number
        "1.5",  # fractional result with no multiplier — not an integer
        "1.3 1.2",  # sum 2.5 is not an integer
    ],
)
def test_parse_invalid(s: str) -> None:
    with pytest.raises(ParseError):
        parse(s)
