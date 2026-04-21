import pytest
from hypothesis import given
from hypothesis import strategies as st

from doshomik import format, parse


@pytest.mark.skip(reason="format not yet implemented — enable in Phase 3")
@given(st.integers(min_value=0, max_value=10**15))
def test_roundtrip_lakh_bangla(n: int) -> None:
    assert parse(format(n, script="bangla", grouping="lakh")) == n


@pytest.mark.skip(reason="format not yet implemented — enable in Phase 3")
@given(st.integers(min_value=0, max_value=10**15))
def test_roundtrip_western_english(n: int) -> None:
    assert parse(format(n, script="english", grouping="western")) == n


@pytest.mark.skip(reason="format not yet implemented — enable in Phase 3")
@given(st.integers(min_value=0, max_value=10**15))
def test_roundtrip_none_bangla(n: int) -> None:
    assert parse(format(n, script="bangla", grouping="none")) == n
