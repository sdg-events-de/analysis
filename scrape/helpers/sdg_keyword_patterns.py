import re

SDG_KEYWORD_PATTERNS = [
    re.compile(r"\bSDG[0-9]+\b", flags=re.IGNORECASE),
    re.compile(r"\bSustainable Development Goals?\b", flags=re.IGNORECASE),
    re.compile(r"\bNachhaltigkeitsziele?\b", flags=re.IGNORECASE),
    re.compile(r"\bZiele? für Nachhaltige Entwicklung\b", flags=re.IGNORECASE),
]