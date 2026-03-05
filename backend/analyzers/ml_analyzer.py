import re
from urllib.parse import urlparse


import math
from collections import Counter


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not text:
        return 0
    probs = [n / len(text) for n in Counter(text).values()]
    return -sum(p * math.log2(p) for p in probs)


def analyze_ml(url: str) -> dict:
    """
    Simulated Machine Learning Analyzer.
    """
    score = 100
    warnings = []
    features = {}

    parsed = urlparse(url)
    domain = parsed.hostname or ""

    # Feature 1: Digits to alphabet ratio in domain
    letters = len(re.findall(r"[a-z]", domain.lower()))
    digits = len(re.findall(r"\d", domain))
    digit_ratio = digits / (letters + digits) if (letters + digits) > 0 else 0
    features["digit_ratio"] = digit_ratio

    if digit_ratio > 0.4:
        score -= 30
        warnings.append(f"Доменде цифрлар үлесі өте жоғары ({int(digit_ratio*100)}%)")

    # Feature 2: Entropy of domain (randomness test)
    parts = domain.split(".")
    domain_main = parts[-2] if len(parts) >= 2 else domain
    entropy = calculate_entropy(domain_main)
    features["entropy"] = entropy

    if entropy > 4.0:  # High entropy usually means random string
        score -= 20
        warnings.append("Домен атауы кездейсоқ символдар тізбегіне ұқсайды (entropy)")

    # Feature 3: Long domain parts (phishing URLs often have very long parts)
    for part in parts:
        if len(part) > 30:
            score -= 25
            warnings.append(f"Доменнің бір бөлігі тым ұзын ({len(part)} символ)")
            break

    # Feature 4: Hyphen count in main domain
    hyphen_count = domain_main.count("-")
    if hyphen_count > 2:
        score -= 15
        warnings.append("Домен атауында көп сызықшалар бар")

    return {
        "score": max(0, score),
        "warnings": warnings,
        "features": features,
    }
