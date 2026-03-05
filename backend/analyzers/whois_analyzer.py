from datetime import datetime, timezone
from urllib.parse import urlparse

import whois


def analyze_whois(url: str) -> dict:
    """Check domain WHOIS information including age and registrar."""
    score = 100
    warnings = []
    details = {}

    parsed = urlparse(url)
    domain = parsed.hostname or ""

    # Strip subdomains to get registrable domain
    parts = domain.split(".")
    if len(parts) > 2:
        registrable = ".".join(parts[-2:])
    else:
        registrable = domain

    try:
        w = whois.whois(registrable)

        # Domain creation date
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            if isinstance(creation_date, str):
                try:
                    creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
                except ValueError:
                    creation_date = None

        if creation_date:
            now = datetime.now(timezone.utc)
            if creation_date.tzinfo is None:
                creation_date = creation_date.replace(tzinfo=timezone.utc)
            age_days = (now - creation_date).days
            details["domain_age_days"] = age_days
            details["creation_date"] = creation_date.isoformat()

            if age_days < 30:
                score -= 40
                warnings.append(f"Домен {age_days} күн бұрын тіркелген — өте жаңа!")
            elif age_days < 90:
                score -= 25
                warnings.append(f"Домен {age_days} күн бұрын тіркелген — жаңа домен")
            elif age_days < 365:
                score -= 10
                warnings.append(f"Домен 1 жылдан аз уақыт бұрын тіркелген")
        else:
            score -= 15
            warnings.append("Домен тіркелу күнін анықтау мүмкін болмады")
            details["domain_age_days"] = None

        # Registrar
        registrar = w.registrar
        if registrar:
            details["registrar"] = registrar
        else:
            details["registrar"] = "Белгісіз"

        # Expiration date
        expiration_date = w.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if expiration_date:
            if isinstance(expiration_date, str):
                try:
                    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
                except ValueError:
                    expiration_date = None
            if expiration_date:
                details["expiration_date"] = expiration_date.isoformat()

        # Country
        if w.country:
            details["country"] = w.country

    except Exception:
        score = 50
        warnings.append("WHOIS ақпаратын алу мүмкін болмады")
        details["whois_available"] = False

    return {
        "score": max(0, score),
        "warnings": warnings,
        "details": details,
    }
