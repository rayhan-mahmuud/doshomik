from hypothesis import given
from hypothesis import strategies as st

from doshomik import format, parse

_NONNEG_INTS = st.integers(min_value=0, max_value=10**15)


@given(_NONNEG_INTS)
def test_roundtrip_lakh_bangla(n: int) -> None:
    assert parse(format(n, script="bangla", grouping="lakh")) == n


@given(_NONNEG_INTS)
def test_roundtrip_western_english(n: int) -> None:
    assert parse(format(n, script="english", grouping="western")) == n


@given(_NONNEG_INTS)
def test_roundtrip_none_bangla(n: int) -> None:
    assert parse(format(n, script="bangla", grouping="none")) == n
