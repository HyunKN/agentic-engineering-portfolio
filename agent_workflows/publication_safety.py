"""Shared fail-closed checks for text intended for public artifacts."""

from __future__ import annotations

import re


LOCAL_PATH_RE = re.compile(
    (
        "(?:"
        + "[A-Za-z]:"
        + r"\\Users\\"
        + "|/"
        + "[A-Za-z]:/Users/"
        + "|App"
        + r"Data[\\/]"
        + "|Local"
        + r"[\\/]Temp)"
    ),
    re.IGNORECASE,
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


def find_publication_risks(text: str) -> tuple[str, ...]:
    """Return stable risk names without exposing the matched values."""

    risks: list[str] = []
    if LOCAL_PATH_RE.search(text):
        risks.append("contains a local machine path")
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        risks.append("contains a high-risk secret pattern")
    return tuple(risks)
