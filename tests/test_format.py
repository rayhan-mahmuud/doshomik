import pytest

from doshomik import format


def test_format_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        format(1000)
