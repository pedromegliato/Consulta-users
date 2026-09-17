import re

MIN_PHONE_SEARCH_DIGITS = 3

_NON_DIGITS = re.compile(r"\D")
_LETTERS = re.compile(r"[^\W\d_]")


def digits_only(value: str) -> str:
    return _NON_DIGITS.sub("", value)


def phone_search_digits(search: str) -> str | None:
    if _LETTERS.search(search):
        return None

    digits = digits_only(search)
    return digits if len(digits) >= MIN_PHONE_SEARCH_DIGITS else None
