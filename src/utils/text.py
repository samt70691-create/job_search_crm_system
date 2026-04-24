import re
from difflib import SequenceMatcher


def normalize_text(value: str) -> str:
    if not value:
        return ''
    value = value.lower().strip()
    value = re.sub(r'\s+', ' ', value)
    return value


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()
