PROVIDER_WEIGHTS: dict[str, float] = {
    "google_safe_browsing": 0.35,
    "virustotal": 0.35,
    "whois": 0.15,
    "ssl": 0.15,
}

VERDICT_THRESHOLDS: dict[str, tuple[int, int]] = {
    "safe": (0, 24),
    "suspicious": (25, 59),
    "malicious": (60, 100),
}

TRUST_PRIORITY: list[str] = [
    "google_safe_browsing",
    "virustotal",
    "ssl",
    "whois",
]
