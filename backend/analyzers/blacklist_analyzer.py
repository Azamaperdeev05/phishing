import json
from functools import lru_cache
from pathlib import Path

from utils.url_utils import extract_hostname, get_registrable_domain

# Path to the local dataset
DATASET_PATH = (
    Path(__file__).resolve().parent.parent.parent / "phishing_test_dataset.json"
)
THREAT_FEED_PATH = Path(__file__).resolve().parent.parent / "data" / "threat_feed_domains.json"


@lru_cache(maxsize=8)
def _load_dataset_hosts(path: str, mtime: float) -> set[str]:
    with open(path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    blocked_hosts = set()
    for item in dataset:
        if item.get("label") != "phishing":
            continue
        hostname = extract_hostname(item.get("url", ""))
        if hostname:
            blocked_hosts.add(hostname)

    return blocked_hosts


@lru_cache(maxsize=8)
def _load_feed_hosts(path: str, mtime: float) -> tuple[set[str], str]:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    generated_at = payload.get("generated_at_utc", "")
    domains = payload.get("domains", [])
    blocked_hosts = {extract_hostname(domain) for domain in domains}
    blocked_hosts = {d for d in blocked_hosts if d}
    return blocked_hosts, generated_at


def analyze_blacklist(url: str) -> dict:
    """Check if URL is in the local phishing blacklist."""
    score = 100
    warnings = []
    details = {}
    scanned_hostname = extract_hostname(url)

    try:
        if DATASET_PATH.exists():
            dataset_hosts = _load_dataset_hosts(
                str(DATASET_PATH), DATASET_PATH.stat().st_mtime
            )
            if scanned_hostname in dataset_hosts:
                score = 0
                warnings.append("КРИТИКАЛЫҚ: Домен локалды фишинг базасында табылды!")
                details["blacklisted_local_dataset"] = True

        if score > 0 and THREAT_FEED_PATH.exists():
            feed_hosts, generated_at = _load_feed_hosts(
                str(THREAT_FEED_PATH), THREAT_FEED_PATH.stat().st_mtime
            )
            details["threat_feed_updated_at"] = generated_at
            if scanned_hostname in feed_hosts:
                score = 0
                warnings.append("КРИТИКАЛЫҚ: Домен сыртқы threat-intel фидінде табылды!")
                details["blacklisted_threat_feed"] = True

        details["checked_dataset"] = True
        details["checked_threat_feed"] = THREAT_FEED_PATH.exists()
        details["scanned_hostname"] = scanned_hostname
        details["scanned_registrable_domain"] = get_registrable_domain(scanned_hostname)
    except Exception:
        details["blacklist_check_error"] = True

    return {
        "score": score,
        "warnings": warnings,
        "details": details,
    }
