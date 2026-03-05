from urllib.parse import urlparse

import tldextract


_EXTRACTOR = tldextract.TLDExtract(suffix_list_urls=None)


def normalize_hostname(hostname: str) -> str:
    value = (hostname or "").strip().lower()
    if value.startswith("www."):
        value = value[4:]
    return value.strip(".")


def extract_hostname(value: str) -> str:
    raw = (value or "").strip()
    if not raw:
        return ""

    parsed = urlparse(raw)
    host = parsed.hostname

    if host:
        return normalize_hostname(host)

    # Fallback: treat input as a plain hostname
    return normalize_hostname(raw.split("/")[0])


def get_registrable_domain(hostname: str) -> str:
    host = normalize_hostname(hostname)
    if not host:
        return ""

    extracted = _EXTRACTOR(host)
    if extracted.domain and extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}".lower()
    return host
