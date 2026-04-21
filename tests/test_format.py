# ruff: noqa: RUF001  # intentional Bangla digit characters in test strings
import pytest

from doshomik import format
from doshomik._exceptions import FormatError


@pytest.mark.parametrize(
    "n, script, grouping, expected",
    [
        # --- lakh grouping, english ---
        (0, "english", "lakh", "0"),
        (1, "english", "lakh", "1"),
        (100, "english", "lakh", "100"),
        (999, "english", "lakh", "999"),
        (1_000, "english", "lakh", "1,000"),
        (10_000, "english", "lakh", "10,000"),
        (99_999, "english", "lakh", "99,999"),
        (100_000, "english", "lakh", "1,00,000"),
        (125_000, "english", "lakh", "1,25,000"),
        (999_999, "english", "lakh", "9,99,999"),
        (1_000_000, "english", "lakh", "10,00,000"),
        (10_000_000, "english", "lakh", "1,00,00,000"),
        (12_500_000, "english", "lakh", "1,25,00,000"),
        (1_000_000_000, "english", "lakh", "1,00,00,00,000"),
        # --- lakh grouping, bangla ---
        (0, "bangla", "lakh", "০"),
        (1_000, "bangla", "lakh", "১,০০০"),
        (100_000, "bangla", "lakh", "১,০০,০০০"),
        (125_000, "bangla", "lakh", "১,২৫,০০০"),
        (10_000_000, "bangla", "lakh", "১,০০,০০,০০০"),
        (12_500_000, "bangla", "lakh", "১,২৫,০০,০০০"),
        # --- western grouping, english ---
        (0, "english", "western", "0"),
        (1_000, "english", "western", "1,000"),
        (1_000_000, "english", "western", "1,000,000"),
        (1_000_000_000, "english", "western", "1,000,000,000"),
        # --- western grouping, bangla ---
        (1_000, "bangla", "western", "১,০০০"),
        (1_000_000, "bangla", "western", "১,০০০,০০০"),
        # --- no grouping, english ---
        (0, "english", "none", "0"),
        (125_000, "english", "none", "125000"),
        (10_000_000, "english", "none", "10000000"),
        # --- no grouping, bangla ---
        (0, "bangla", "none", "০"),
        (125_000, "bangla", "none", "১২৫০০০"),
        (10_000_000, "bangla", "none", "১০০০০০০০"),
        # --- negative numbers ---
        (-1, "english", "lakh", "-1"),
        (-1_000, "english", "lakh", "-1,000"),
        (-100_000, "english", "lakh", "-1,00,000"),
        (-100_000, "bangla", "lakh", "-১,০০,০০০"),
        (-1_000_000, "english", "western", "-1,000,000"),
        (-125_000, "english", "none", "-125000"),
    ],
)
def test_format_valid(n: int, script: str, grouping: str, expected: str) -> None:
    assert format(n, script=script, grouping=grouping) == expected


@pytest.mark.parametrize(
    "n, script, grouping",
    [
        # booleans rejected
        (True, "english", "lakh"),
        (False, "bangla", "none"),
        # non-int types
        (1.5, "english", "lakh"),
        ("1", "english", "lakh"),
        (None, "english", "lakh"),
        # invalid script
        (100, "hindi", "lakh"),
        (100, "English", "lakh"),
        (100, "", "lakh"),
        # invalid grouping
        (100, "english", "indian"),
        (100, "bangla", "Western"),
        (100, "english", ""),
    ],
)
def test_format_invalid(n: object, script: str, grouping: str) -> None:
    with pytest.raises(FormatError):
        format(n, script=script, grouping=grouping)  # type: ignore[arg-type]
