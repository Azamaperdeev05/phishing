# Trusted domains whitelist — these are safe and skip deep analysis
TRUSTED_DOMAINS = {
    # Kazakhstan banks
    "kaspi.kz",
    "halykbank.kz",
    "homebank.kz",
    "onlinebank.kz",
    "jusan.kz",
    "forte.kz",
    "bfrbank.kz",
    "centercredit.kz",
    "bankrbk.kz",
    "eubank.kz",

    # Kazakhstan government
    "egov.kz",
    "gov.kz",
    "elicense.kz",
    "adilet.gov.kz",
    "salyk.kz",
    "stat.gov.kz",
    "enbek.kz",

    # Kazakhstan services
    "qazpost.kz",
    "beeline.kz",
    "kcell.kz",
    "tele2.kz",
    "activ.kz",
    "olx.kz",
    "kolesa.kz",
    "krisha.kz",

    # Global trusted
    "google.com", "google.kz",
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "whatsapp.com",
    "telegram.org",
    "apple.com",
    "microsoft.com",
    "github.com",
    "stackoverflow.com",
    "wikipedia.org",
    "amazon.com",
    "netflix.com",
    "linkedin.com",
    "twitter.com",
    "paypal.com",
}


def is_whitelisted(domain: str) -> bool:
    """Check if domain or its parent is in the trusted whitelist."""
    domain = domain.lower().strip()
    if domain in TRUSTED_DOMAINS:
        return True
    # Check if it's a subdomain of a trusted domain
    for trusted in TRUSTED_DOMAINS:
        if domain.endswith("." + trusted):
            return True
    return False
