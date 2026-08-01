# File: tests/test_normalize.py

from csvsmith.utils.normalize import normalize


def test_normalize_with_spaces():
    result = normalize("  hello  world   ")
    assert result == "helloworld"


def test_normalize_with_case_insensitivity():
    result = normalize("HeLLo WoRLD")
    assert result == "helloworld"


def test_normalize_with_nfkc():
    result = normalize("ｈｅｌｌｏ　ｗｏｒｌｄ", nfkc=True)
    assert result == "helloworld"


def test_normalize_without_nfkc():
    result = normalize("ｈｅｌｌｏ　ｗｏｒｌｄ", nfkc=False)
    assert result == "ｈｅｌｌｏｗｏｒｌｄ"  # Full-width characters remain unchanged


def test_normalize_empty_string():
    result = normalize("")
    assert result == ""


def test_normalize_none():
    result = normalize(None)
    assert result == ""


def test_normalize_spaces_only():
    result = normalize("     ")
    assert result == ""


def test_normalize_numbers():
    result = normalize(12345)
    assert result == "12345"


def test_normalize_ignore_whitespace_false():
    result = normalize("   hello   world   ", ignore_whitespace=False)
    assert result == "hello   world"


def test_normalize_ignore_case_false():
    result = normalize("HeLLo WoRLD", ignore_case=False)
    assert result == "HeLLoWoRLD"
