import re
from typing import Any

NON_BREAKING_SPACE = "\xa0"
SEPARATOR_PATTERN = re.compile(r"[ _\xa0]")
NUMBER_PATTERN = re.compile(r"^-?(?:\d+|\d*\.\d+)$")
INVALID_NUMBER_MESSAGE = "Could not convert {value!r} to a valid number."
CURRENCY_PREFIX_PATTERN = re.compile(r"^[\$€£¥₹]")


def strip_currency_prefix(value: Any) -> Any:
    """
    Remove a single common currency symbol from the start of a value.
    """
    text = str(value).strip()
    if text and CURRENCY_PREFIX_PATTERN.match(text):
        return text[1:].strip()
    return value


def _normalize_numeric_text(value: Any, *, sep: str, decimal: str) -> str:
    """
    Normalize a numeric text string for consistent formatting.

    Converts a given value to a string representation and ensures normalization of numeric formatting,
    such as removing group separators, converting localized decimal separators, and handling negative
    values enclosed in parentheses.
    """
    numeric_text = str(value).strip()

    if numeric_text.startswith("(") and numeric_text.endswith(")"):
        numeric_text = f"-{numeric_text[1:-1]}"

    if sep:
        numeric_text = numeric_text.replace(sep, "")

    if decimal != ".":
        numeric_text = numeric_text.replace(decimal, ".")

    return numeric_text


def _has_valid_grouping(numeric_text: str, *, decimal: str) -> bool:
    """
    Checks whether a numeric text string has valid grouping based on a specified decimal character.
    """
    if not numeric_text:
        return False

    unsigned_text = numeric_text[1:] if numeric_text.startswith("-") else numeric_text

    if unsigned_text.count(decimal) > 1:
        return False

    integer_text, _, fraction_text = unsigned_text.partition(decimal)

    if not integer_text and not fraction_text:
        return False

    for part in (integer_text, fraction_text):
        if not part:
            continue
        if part.startswith("_") or part.endswith("_"):
            return False
        if part.startswith(" ") or part.endswith(" "):
            return False
        if part.startswith(NON_BREAKING_SPACE) or part.endswith(NON_BREAKING_SPACE):
            return False
        if "__" in part or "  " in part or NON_BREAKING_SPACE * 2 in part:
            return False

    stripped_text = SEPARATOR_PATTERN.sub("", numeric_text)
    return bool(NUMBER_PATTERN.fullmatch(stripped_text))


def _strip_group_separators(numeric_text: str) -> str:
    return SEPARATOR_PATTERN.sub("", numeric_text)


def _invalid_number_error(value: Any) -> ValueError:
    return ValueError(INVALID_NUMBER_MESSAGE.format(value=value))


def clean_numeric(
        value: Any, *, sep: str = ",", decimal: str = ".", relaxed: bool = False
) -> float | Any:
    """
    Cleans and converts a given input to a float by normalizing its numeric representation.
    """
    if value is None:
        return 0.0

    normalized_text = _normalize_numeric_text(value, sep=sep, decimal=decimal)

    if not _has_valid_grouping(normalized_text, decimal=decimal):
        if relaxed:
            return value
        raise _invalid_number_error(value)

    candidate_text = _strip_group_separators(normalized_text)

    try:
        return float(candidate_text)
    except ValueError as exc:
        if relaxed:
            return value
        raise _invalid_number_error(value) from exc


def clean_currency_numeric(
        value: Any, *, sep: str = ",", decimal: str = ".", relaxed: bool = False
) -> float | Any:
    """
    Cleans and converts a currency-prefixed numeric string to a float.
    """
    if value is None:
        return 0.0

    return clean_numeric(
        strip_currency_prefix(value),
        sep=sep,
        decimal=decimal,
        relaxed=relaxed,
    )
