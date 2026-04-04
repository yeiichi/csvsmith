import pytest
from csvsmith.cli import build_parser, main
from csvsmith.utils.clean_numeric import clean_currency_numeric, clean_numeric


def test_main_help():
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])
    assert excinfo.value.code == 0


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


def test_clean_currency_numeric_with_currency_prefix() -> None:
    assert clean_currency_numeric("$1,000") == 1000.0


def test_clean_currency_numeric_with_euro_prefix() -> None:
    assert clean_currency_numeric("€1,000.50") == 1000.5


def test_clean_numeric_still_rejects_currency_prefix() -> None:
    with pytest.raises(ValueError, match=r"Could not convert '\$1,000'.*"):
        clean_numeric("$1,000")


def test_cli_parses_clean_currency_numeric_command():
    parser = build_parser()
    args = parser.parse_args(
        ["clean-currency-numeric", "$1,234.56", "--sep", ",", "--decimal", "."]
    )

    assert args.command == "clean-currency-numeric"
    assert args.value == "$1,234.56"
    assert args.sep == ","
    assert args.decimal == "."
