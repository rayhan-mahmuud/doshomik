import pytest

from doshomik import parse


def test_parse_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        parse("১ কোটি")
