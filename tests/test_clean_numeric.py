import pytest
from src.csvsmith.clean_numeric import clean_numeric


def test_clean_numeric_with_valid_integer_string() -> None:
    assert clean_numeric("1,234") == 1234.0


def test_clean_numeric_with_valid_float_string() -> None:
    assert clean_numeric("1,234.56") == 1234.56


def test_clean_numeric_with_custom_separator() -> None:
    assert clean_numeric("1.234,56", sep=".", decimal=",") == 1234.56


def test_clean_numeric_with_negative_value() -> None:
    assert clean_numeric("-1,234.56") == -1234.56


def test_clean_numeric_with_parenthesis_for_negative() -> None:
    assert clean_numeric("(1,234.56)") == -1234.56


def test_clean_numeric_with_invalid_value_raises_valueerror() -> None:
    with pytest.raises(ValueError, match="Could not convert 'abc'.*"):
        clean_numeric("abc")


def test_clean_numeric_with_multiple_decimal_points_raises_valueerror() -> None:
    with pytest.raises(ValueError, match="Could not convert '1,234.5.6'.*"):
        clean_numeric("1,234.5.6")


def test_clean_numeric_with_none_value() -> None:
    assert clean_numeric(None) == 0.0
