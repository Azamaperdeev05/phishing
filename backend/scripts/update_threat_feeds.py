import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from utils.url_utils import get_registrable_domain, normalize_hostname


SOURCES = {
    "urlhaus_recent": "https://urlhaus.abuse.ch/downloads/text_recent/",
    "openphish_feed": "https://openphish.com/feed.txt",
}


def _extract_domain(raw: str) -> str:
    value = raw.strip()
    if not value or value.startswith("#"):
        return ""

    parsed = urlparse(value)
    host = normalize_hostname(parsed.hostname or "")
    if not host:
        return ""

    return get_registrable_domain(host)


def fetch_domains(url: str, timeout: int) -> tuple[set[str], int]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    total_lines = 0
    domains = set()
    for line in response.text.splitlines():
        total_lines += 1
        domain = _extract_domain(line)
        if domain:
            domains.add(domain)

    return domains, total_lines


def build_feed(timeout: int) -> dict:
    union_domains = set()
    source_stats = {}

    for source_name, url in SOURCES.items():
        domains, total_lines = fetch_domains(url, timeout)
        union_domains.update(domains)
        source_stats[source_name] = {
            "url": url,
            "line_count": total_lines,
            "domain_count": len(domains),
        }

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_stats": source_stats,
        "domain_count": len(union_domains),
        "domains": sorted(union_domains),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Download threat-intel feeds and build local phishing domain set."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="HTTP timeout for feed downloads (seconds)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/threat_feed_domains.json",
        help="Output JSON path relative to backend directory",
    )
    args = parser.parse_args()

    output_path = (BACKEND_DIR / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = build_feed(timeout=args.timeout)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Saved {payload['domain_count']} domains to {output_path}")
    for source, stats in payload["source_stats"].items():
        print(f"- {source}: {stats['domain_count']} domains ({stats['line_count']} lines)")


if __name__ == "__main__":
    main()
