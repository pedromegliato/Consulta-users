import re

from app.domain.text import digits_only

MIN_DIGITS = 8

_EXTENSION = re.compile(r"\s*(x|ext\.?|ramal)\s*\d+\s*$", re.IGNORECASE)


def normalize_phone(value: str | None) -> str | None:
    if value is None:
        return None

    digits = digits_only(_EXTENSION.sub("", value))
    return digits if len(digits) >= MIN_DIGITS else None
