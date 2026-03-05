from schemas import FactorScores

# Weights for each analysis factor (must sum to 1.0)
WEIGHTS = {
    "url_analysis": 0.24,
    "ssl_check": 0.18,
    "whois_check": 0.12,
    "content_analysis": 0.18,
    "text_analysis": 0.12,
    "blacklist_check": 0.16,
}

# Verdict thresholds
THRESHOLDS = {
    "safe": 81,  # 81-100 = Safe
    "suspicious": 51,  # 51-80 = Suspicious
    # 0-50 = Phishing
}

# Recommendation messages by language
RECOMMENDATIONS = {
    "kk": {
        "safe": "Бұл сайт қауіпсіз деп бағаланды. Дегенмен, жеке деректеріңізді енгізу кезінде абай болыңыз.",
        "suspicious": "Бұл сайт күдікті. Жеке деректеріңізді енгізбеуді ұсынамыз. Ресми сайтқа тікелей кіріңіз.",
        "phishing": "БҰЛ САЙТҚА КІРМЕҢІЗ! Бұл фишинг сайты болуы мүмкін. Ешқандай деректер енгізбеңіз!",
    },
    "ru": {
        "safe": "Этот сайт оценён как безопасный. Тем не менее, будьте осторожны при вводе личных данных.",
        "suspicious": "Этот сайт вызывает подозрения. Рекомендуем не вводить личные данные. Перейдите на официальный сайт напрямую.",
        "phishing": "НЕ ЗАХОДИТЕ НА ЭТОТ САЙТ! Это может быть фишинговый сайт. Не вводите никаких данных!",
    },
    "en": {
        "safe": "This site is rated as safe. However, be cautious when entering personal data.",
        "suspicious": "This site is suspicious. We recommend not entering personal data. Go to the official site directly.",
        "phishing": "DO NOT USE THIS SITE! This may be a phishing site. Do not enter any data!",
    },
}

WHITELISTED_RECOMMENDATION = {
    "kk": "Бұл сайт сенімді тізімде. Ресми және қауіпсіз сайт.",
    "ru": "Этот сайт находится в белом списке. Это официальный и безопасный сайт.",
    "en": "This site is whitelisted. It is an official and safe site.",
}


def calculate_score(factor_scores: dict) -> float:
    """Calculate weighted overall score from individual factor scores."""
    # Special case: Blacklist hit is an immediate failure
    if factor_scores.get("blacklist_check", 100) == 0:
        return 10.0

    # Special case: No SSL + low URL score is very suspicious
    if (
        factor_scores.get("ssl_check", 100) == 0
        and factor_scores.get("url_analysis", 100) < 50
    ):
        return min(30.0, sum(factor_scores.values()) / len(factor_scores))

    total = 0.0
    for factor, weight in WEIGHTS.items():
        total += factor_scores.get(factor, 50) * weight
    return round(total, 1)


def get_verdict(score: float) -> str:
    if score >= THRESHOLDS["safe"]:
        return "SAFE"
    elif score >= THRESHOLDS["suspicious"]:
        return "SUSPICIOUS"
    return "PHISHING"


def get_risk_level(score: float) -> str:
    if score >= THRESHOLDS["safe"]:
        return "LOW"
    elif score >= THRESHOLDS["suspicious"]:
        return "MEDIUM"
    return "HIGH"


def get_recommendation(score: float, language: str = "kk") -> str:
    lang = language if language in RECOMMENDATIONS else "kk"
    if score >= THRESHOLDS["safe"]:
        return RECOMMENDATIONS[lang]["safe"]
    elif score >= THRESHOLDS["suspicious"]:
        return RECOMMENDATIONS[lang]["suspicious"]
    return RECOMMENDATIONS[lang]["phishing"]
