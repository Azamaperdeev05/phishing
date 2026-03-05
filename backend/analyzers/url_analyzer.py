import re
from urllib.parse import urlparse, parse_qsl
from difflib import SequenceMatcher

from utils.url_utils import get_registrable_domain

# Well-known brands that phishers commonly impersonate
KNOWN_BRANDS = [
    "kaspi",
    "halyk",
    "halykbank",
    "egov",
    "google",
    "facebook",
    "instagram",
    "whatsapp",
    "telegram",
    "apple",
    "microsoft",
    "paypal",
    "amazon",
    "netflix",
    "linkedin",
    "twitter",
    "tiktok",
    "youtube",
    "yahoo",
    "outlook",
    "onlinebank",
    "homebank",
    "jusan",
    "forte",
    "bereke",
    "bcc",
    "centercredit",
    "sberbank",
    "qazpost",
    "beeline",
    "kcell",
    "tele2",
    "activ",
]

SUSPICIOUS_TLDS = [
    ".tk",
    ".ml",
    ".ga",
    ".cf",
    ".gq",
    ".buzz",
    ".top",
    ".xyz",
    ".club",
    ".work",
    ".click",
    ".link",
    ".info",
    ".site",
    ".online",
    ".icu",
    ".monster",
    ".surf",
    ".rest",
    ".beauty",
    ".date",
    ".win",
    ".bid",
]

SCAM_KEYWORDS = [
    "bet",
    "win",
    "gift",
    "bonus",
    "prize",
    "lucky",
    "lottery",
    "cash",
    "money",
    "reward",
    "promo",
    "free",
    "claim",
    "jackpot",
    "hadiah",
    "penerima",
]

# Platforms often used to host phishing pages
ABUSED_PLATFORMS = [
    "gitbook.io", "backblazeb2.com", "firebaseapp.com", "s3.amazonaws.com",
    "storage.googleapis.com", "pages.dev", "netlify.app", "vercel.app",
    "github.io", "glitch.me", "repl.co", "ngrok-free.app",
]

URL_SHORTENERS = [
    "bit.ly", "tinyurl.com", "cutt.ly", "cutt.cx", "t.co", "goo.gl", "rebrand.ly",
]

SENSITIVE_QUERY_KEYS = {
    "password",
    "passwd",
    "otp",
    "token",
    "session",
    "auth",
    "pin",
    "card",
    "cvv",
}


def analyze_url(url: str) -> dict:
    """Analyze URL structure for phishing indicators."""
    score = 100  # Start with perfect score, deduct for red flags
    warnings = []
    details = {}

    try:
        parsed = urlparse(url)
    except Exception:
        return {"score": 0, "warnings": ["URL-ді талдау мүмкін болмады"], "details": {}}

    domain = (parsed.hostname or "").lower()
    registrable_domain = get_registrable_domain(domain)
    path = parsed.path or ""
    full_url = url

    # 1. Check if IP address is used instead of domain
    ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    if ip_pattern.match(domain):
        score -= 40
        warnings.append("URL-де домен атауы орнына IP мекенжай қолданылған")
        details["ip_address"] = True

    # 2. Check URL length (phishing URLs tend to be long)
    if len(full_url) > 100:
        score -= 10
        warnings.append(f"URL тым ұзын ({len(full_url)} символ)")
    if len(full_url) > 200:
        score -= 10
        warnings.append("URL өте ұзын — фишинг белгісі")
    details["url_length"] = len(full_url)

    # 3. Check for suspicious characters
    if "@" in full_url:
        score -= 30
        warnings.append("URL-де '@' символы бар — бұл фишинг тәсілі болуы мүмкін")
    if full_url.count("-") > 3:
        score -= 15
        warnings.append(f"URL-де көп сызықша бар ({full_url.count('-')} дана)")
    if re.search(r"%[0-9a-fA-F]{2}", full_url):
        score -= 10
        warnings.append("URL-де кодталған символдар бар (hex encoding)")

    # 4. Check subdomain count
    subdomains = domain.split(".")
    if len(subdomains) > 3:
        score -= 15
        warnings.append(f"Көп қосалқы домен саны: {len(subdomains) - 2}")
    details["subdomain_count"] = len(subdomains) - 2

    # 4a. Check for too many digits in domain (e.g., bet83081.com)
    domain_main = subdomains[-2] if len(subdomains) >= 2 else domain
    digits = re.findall(r"\d", domain_main)
    if len(digits) > 3:
        score -= 20
        warnings.append(
            f"Доменде тым көп цифр бар ({len(digits)} дана) — фишинг белгісі"
        )

    # 4b. Check for Punycode
    if "xn--" in domain:
        score -= 30
        warnings.append(
            "Доменде Punycode қолданылған — бұл символдармен алдау тәсілі болуы мүмкін"
        )

    # 5. Check for suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            score -= 20
            warnings.append(f"Күдікті домен аймағы: {tld}")
            break

    # 6. Check HTTPS
    if parsed.scheme != "https":
        score -= 20
        warnings.append("Сайт HTTPS пайдаланбайды — қауіпті байланыс")
        details["https"] = False
    else:
        details["https"] = True

    # 7. Check domain similarity to known brands (typosquatting)
    domain_name = registrable_domain.split(".")[0] if registrable_domain else ""
    best_match = None
    best_ratio = 0
    for brand in KNOWN_BRANDS:
        ratio = SequenceMatcher(None, domain_name.lower(), brand).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = brand

    if best_match and 0.6 < best_ratio < 1.0:
        similarity_pct = int(best_ratio * 100)
        score -= 25
        warnings.append(
            f"Домен '{best_match}' брендіне ұқсас ({similarity_pct}% ұқсастық)"
        )
        details["brand_similarity"] = {"brand": best_match, "ratio": best_ratio}

    # 7a. Mixed scripts in unicode domain (possible homograph attacks)
    if any(ord(ch) > 127 for ch in domain):
        score -= 15
        warnings.append("Доменде Unicode символдар бар — homograph шабуылы болуы мүмкін")
        details["unicode_domain"] = True

    # 8. Check for suspicious path keywords
    suspicious_path_keywords = [
        "login",
        "signin",
        "verify",
        "account",
        "secure",
        "update",
        "confirm",
        "banking",
        "wallet",
    ]
    path_lower = path.lower()
    for kw in suspicious_path_keywords:
        if kw in path_lower:
            score -= 5
            warnings.append(f"URL жолында күдікті сөз: '{kw}'")

    # 8a. Excessive path depth
    path_parts = [part for part in path.split("/") if part]
    if len(path_parts) >= 5:
        score -= 10
        warnings.append(f"URL жолы тым терең ({len(path_parts)} сегмент)")

    # 8b. High-entropy path segment
    if any(len(part) > 24 and re.search(r"[a-zA-Z]", part) and re.search(r"\d", part) for part in path_parts):
        score -= 10
        warnings.append("URL жолында кездейсоқ токенге ұқсас ұзын сегмент бар")

    # 8c. Sensitive tokens in query params
    query_pairs = parse_qsl(parsed.query, keep_blank_values=True)
    sensitive_hits = 0
    for key, _ in query_pairs:
        if key.lower() in SENSITIVE_QUERY_KEYS:
            sensitive_hits += 1

    if sensitive_hits > 0:
        score -= min(20, sensitive_hits * 8)
        warnings.append(
            f"Query параметрлерінде құпия дерекке ұқсас кілттер бар ({sensitive_hits})"
        )
        details["sensitive_query_keys"] = sensitive_hits

    # 9. Check for scam keywords in domain
    for kw in SCAM_KEYWORDS:
        if kw in domain:
            score -= 15
            warnings.append(f"Доменде күдікті сөз бар: '{kw}' — ұтыс немесе бәс тігу сайты болуы мүмкін")
            break

    # 10. Check for abused platforms
    for platform in ABUSED_PLATFORMS:
        if domain.endswith(platform):
            score -= 20
            warnings.append(f"Сайт тегін хостингте/бұлтты сервисте орналасқан ({platform}) — фишинг белгісі болуы мүмкін")
            break

    # 11. Check for URL shorteners
    for shortener in URL_SHORTENERS:
        if domain == shortener or domain.endswith("." + shortener):
            score -= 15
            warnings.append(f"URL қысқартқыш қолданылған ({shortener}) — нақты адресті жасыру тәсілі")
            break
    
    # 12. Check for keywords in subdomains (impersonation)
    if len(subdomains) > 2:
        for brand in KNOWN_BRANDS:
            if any(brand in sub.lower() for sub in subdomains[:-2]):
                score -= 30
                warnings.append(f"Қосалқы доменде танымал бренд атауы табылды: '{brand}'")
                break

    # 13. Brand + security lure in same host
    lure_words = {"secure", "verify", "login", "account", "wallet", "support", "update"}
    host_tokens = re.split(r"[.\-_]", domain)
    has_brand = any(token in KNOWN_BRANDS for token in host_tokens)
    has_lure = any(token in lure_words for token in host_tokens)
    if has_brand and has_lure and domain != registrable_domain:
        score -= 15
        warnings.append("Хостта бренд атауы мен 'secure/login' секілді сөз қатар қолданылған")
        details["brand_lure_combo"] = True

    details["domain"] = domain
    details["registrable_domain"] = registrable_domain
    details["scheme"] = parsed.scheme

    return {
        "score": max(0, score),
        "warnings": warnings,
        "details": details,
    }
