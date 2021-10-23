import re

SDG_KEYWORD_PATTERNS = [
    re.compile(r"\bSDGs?[0-9]*\b", flags=re.IGNORECASE),
    re.compile(r"\b((2030 ?Agenda)|(Agenda ?2030))\b", flags=re.IGNORECASE),
    re.compile(r"\bSustainable Development Goals?\b", flags=re.IGNORECASE),
    re.compile(r"\bNachhaltigkeitsziele?\b", flags=re.IGNORECASE),
    re.compile(r"\bZiel(en?)? für Nachhaltige Entwicklung\b", flags=re.IGNORECASE),
]


def matches_sdgs(text):
    return any([pattern.search(text) for pattern in SDG_KEYWORD_PATTERNS])