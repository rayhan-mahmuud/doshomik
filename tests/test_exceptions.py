import pytest

from doshomik import DoshomikError, FormatError, ParseError


def test_parse_error_is_doshomik_error() -> None:
    assert issubclass(ParseError, DoshomikError)


def test_format_error_is_doshomik_error() -> None:
    assert issubclass(FormatError, DoshomikError)


def test_doshomik_error_is_value_error() -> None:
    assert issubclass(DoshomikError, ValueError)


def test_parse_error_can_be_raised() -> None:
    with pytest.raises(ParseError, match="bad input"):
        raise ParseError("bad input")


def test_format_error_can_be_raised() -> None:
    with pytest.raises(FormatError, match="not an int"):
        raise FormatError("not an int")
