import ssl
import socket
from datetime import datetime, timezone
from urllib.parse import urlparse


def analyze_ssl(url: str) -> dict:
    """Check SSL certificate validity and details."""
    score = 100
    warnings = []
    details = {}

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    port = parsed.port or 443

    if parsed.scheme != "https":
        return {
            "score": 0,
            "warnings": ["Сайт HTTPS пайдаланбайды — SSL сертификаты жоқ"],
            "details": {"has_ssl": False},
        }

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        details["has_ssl"] = True

        # Check certificate issuer
        issuer_parts = dict(x[0] for x in cert.get("issuer", ()))
        issuer_org = issuer_parts.get("organizationName", "Unknown")
        details["issuer"] = issuer_org

        # Check if self-signed or free cert
        free_issuers = ["Let's Encrypt", "ZeroSSL", "Buypass"]
        if issuer_org in free_issuers:
            score -= 5  # Minor deduction for free certs (common in phishing)
            details["free_cert"] = True

        # Check expiry date
        not_after = cert.get("notAfter", "")
        if not_after:
            expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            expiry = expiry.replace(tzinfo=timezone.utc)
            days_left = (expiry - datetime.now(timezone.utc)).days
            details["expires_in_days"] = days_left

            if days_left < 0:
                score -= 40
                warnings.append("SSL сертификатының мерзімі өтіп кеткен!")
            elif days_left < 30:
                score -= 15
                warnings.append(f"SSL сертификатының мерзімі {days_left} күнде аяқталады")

        # Check validity period (short certs are suspicious)
        not_before = cert.get("notBefore", "")
        if not_before and not_after:
            start = datetime.strptime(not_before, "%b %d %H:%M:%S %Y %Z")
            end = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            validity_days = (end - start).days
            details["validity_days"] = validity_days

            if validity_days < 90:
                score -= 15
                warnings.append(f"SSL сертификат мерзімі өте қысқа: {validity_days} күн")

        # Check subject alternative names
        san = cert.get("subjectAltName", ())
        san_domains = [x[1] for x in san if x[0] == "DNS"]
        details["san_count"] = len(san_domains)

        if len(san_domains) > 20:
            score -= 10
            warnings.append("SSL сертификатында тым көп домен тіркелген")

    except ssl.SSLCertVerificationError as e:
        score = 10
        warnings.append(f"SSL сертификаты тексерілмеді: {str(e)[:100]}")
        details["has_ssl"] = True
        details["verification_error"] = True
    except (socket.timeout, socket.gaierror, ConnectionRefusedError, OSError):
        score = 30
        warnings.append("SSL қосылу мүмкін болмады — сервер жауап бермейді")
        details["has_ssl"] = False
        details["connection_error"] = True

    return {
        "score": max(0, score),
        "warnings": warnings,
        "details": details,
    }
