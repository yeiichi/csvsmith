import re
from typing import Any

NON_BREAKING_SPACE = "\xa0"
SEPARATOR_PATTERN = re.compile(r"[ _\xa0]")
NUMBER_PATTERN = re.compile(r"^-?(?:\d+|\d*\.\d+)$")


def _normalize_numeric_text(value: Any, *, sep: str, decimal: str) -> str:
    """
    Normalize a numeric text string for consistent formatting.

    Converts a given value to a string representation and ensures normalization of numeric formatting,
    such as removing group separators, converting localized decimal separators, and handling negative
    values enclosed in parentheses.

    :param value: The value to be normalized, which may be of any type.
    :type value: Any
    :param sep: The character used as a group separator in the input value, which will be removed
        during normalization.
    :type sep: str
    :param decimal: The character used as the decimal separator in the input value, which will
        be replaced with a standard period ('.') during normalization.
    :type decimal: str
    :return: A normalized numeric string with consistent formatting.
    :rtype: str
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

    This function validates the structure of the given numeric text to determine if it adheres to allowed
    grouping conventions. It ensures the string does not contain invalid or misplaced group separators,
    decimal points, or spacing characters.

    :param numeric_text: A string representing the numeric text to be validated.
    :type numeric_text: str
    :param decimal: A string representing the character used as the decimal point.
    :type decimal: str
    :return: True if the numeric text satisfies the grouping rules; otherwise, False.
    :rtype: bool
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


def clean_numeric(
    value: Any, *, sep: str = ",", decimal: str = ".", relaxed: bool = False
) -> float | Any:
    """
    Cleans and converts a given input to a float by normalizing its numeric representation.
    Handles separators and decimal points based on the provided arguments. If the input
    value is invalid or cannot be converted, a ValueError is raised unless relaxed mode
    is enabled.

    :param value: The input value to be cleaned and converted.
    :type value: Any
    :param sep: The character used as a thousands separator in the input value. Default is ",".
    :type sep: str
    :param decimal: The character used as a decimal point in the input value. Default is ".".
    :type decimal: str
    :param relaxed: If True, return the original input when it is not numeric.
    :type relaxed: bool
    :return: The cleaned and converted numeric value as a float, or the original value in relaxed mode.
    :rtype: float | Any
    :raises ValueError: If the input value cannot be converted to a valid number and relaxed is False.
    """
    if value is None:
        return 0.0

    normalized_number_text = _normalize_numeric_text(value, sep=sep, decimal=decimal)

    if not _has_valid_grouping(normalized_number_text, decimal=decimal):
        if relaxed:
            return value
        raise ValueError(f"Could not convert {value!r} to a valid number.")

    numeric_text = SEPARATOR_PATTERN.sub("", normalized_number_text)

    try:
        return float(numeric_text)
    except ValueError as exc:
        if relaxed:
            return value
        raise ValueError(f"Could not convert {value!r} to a valid number.") from exc
