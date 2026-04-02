import unicodedata


def normalize(text, ignore_case=True, ignore_whitespace=True, nfkc=True):
    """
    Standardizes strings to bypass Excel formatting artifacts.
    """
    if text is None:
        return ""

    # Cast to string to handle numeric cells safely
    text = str(text)

    # 1. Unicode Compatibility (Handles full-width/ligatures)
    if nfkc:
        text = unicodedata.normalize('NFKC', text)

    # 2. Case Folding
    if ignore_case:
        text = text.lower()

    # 3. Whitespace handling
    # Always trim outer whitespace, and optionally remove all internal whitespace.
    text = text.strip()
    if ignore_whitespace:
        text = "".join(text.split())

    return text