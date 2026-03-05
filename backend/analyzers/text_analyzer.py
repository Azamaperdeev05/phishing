import re

import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT

# Phishing urgency/fear patterns in Kazakh, Russian, and English
PHISHING_PATTERNS = {
    "kk": [
        r"аккаунт\w*\s+бұғаттал",
        r"шұғыл\s+түрде",
        r"тексер[іу]ңіз",
        r"жүлде\w*\s+ал",
        r"құпия\s+сөз\w*\s+жаңарт",
        r"карта\w*\s+бұғаттал",
        r"қауіпсіздік\s+тексер",
        r"деректер\w*\s+растаңыз",
        r"24\s*сағат\s+ішінде",
        r"тез\s+арада",
        r"ескерту.*хабарлама",
        r"сыйлық\w*\s+ұт",
    ],
    "ru": [
        r"аккаунт\w*\s+заблокирован",
        r"срочно\s+проверьте",
        r"подтвердите\s+данные",
        r"ваш\s+приз",
        r"получите\s+выигрыш",
        r"обновите\s+пароль",
        r"карта\s+заблокирована",
        r"в\s+течение\s+24\s*часов",
        r"немедленно",
        r"ваш\s+аккаунт\s+будет\s+удален",
        r"подозрительная\s+активность",
        r"безопасность\s+аккаунта",
        r"войдите.*подтвердить",
        r"сумма\s+выплаты",
        r"забрать\s+деньги",
    ],
    "en": [
        r"account\s+suspended",
        r"verify\s+your\s+(?:account|identity)",
        r"urgent\s+action\s+required",
        r"confirm\s+your\s+(?:details|identity|password)",
        r"your\s+account\s+(?:has\s+been|will\s+be)\s+(?:locked|suspended|deleted)",
        r"update\s+your\s+(?:payment|billing|password)",
        r"unusual\s+(?:activity|sign.in)",
        r"claim\s+your\s+(?:prize|reward)",
        r"within\s+24\s*hours",
        r"immediately",
        r"congratulations.*(?:won|winner)",
        r"security\s+alert",
        r"kepra",
        r"sucesso",
        r"aumento",
        r"limite",
    ],
}


def analyze_text(url: str) -> dict:
    """Analyze website text content for phishing language patterns."""
    score = 100
    warnings = []
    details = {}
    matched_patterns = []

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(
            url, timeout=REQUEST_TIMEOUT, headers=headers, verify=False
        )
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True).lower()
    except requests.RequestException:
        return {
            "score": 50,
            "warnings": ["Сайт мәтінін алу мүмкін болмады"],
            "details": {"accessible": False},
        }

    details["text_length"] = len(text)

    if len(text) < 50:
        score -= 10
        warnings.append("Сайтта мәтін өте аз — бос немесе жасырын бет болуы мүмкін")

    # Check phishing patterns in all languages
    total_matches = 0
    for lang, patterns in PHISHING_PATTERNS.items():
        lang_name = {"kk": "қазақша", "ru": "орысша", "en": "ағылшынша"}[lang]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                total_matches += len(matches)
                matched_patterns.append(
                    {"lang": lang, "pattern": pattern, "count": len(matches)}
                )

    if total_matches > 0:
        deduction = min(50, total_matches * 10)
        score -= deduction
        warnings.append(
            f"Шұғыл/қорқытушы мәтін табылды: {total_matches} фишинг белгісі"
        )
        details["phishing_text_matches"] = total_matches
        # Show first few matched patterns
        for m in matched_patterns[:3]:
            lang_name = {"kk": "QAZ", "ru": "RUS", "en": "ENG"}[m["lang"]]
            warnings.append(f"[{lang_name}] Фишинг паттерн табылды")

    # Check for excessive exclamation/question marks (urgency signals)
    exclamation_count = text.count("!")
    if exclamation_count > 5:
        score -= 5
        warnings.append(f"Мәтінде көп леп белгісі: {exclamation_count} дана")

    # Check for common data collection phrases
    data_collection_phrases = [
        r"введите.*(?:номер|данные|пароль|код)",
        r"enter.*(?:card|password|ssn|pin|code)",
        r"енгіз.*(?:нөмір|деректер|құпия|код)",
    ]
    for phrase in data_collection_phrases:
        if re.search(phrase, text, re.IGNORECASE):
            score -= 10
            warnings.append("Жеке деректерді сұрайтын мәтін табылды")
            details["asks_personal_data"] = True
            break

    details["matched_patterns"] = len(matched_patterns)

    return {
        "score": max(0, score),
        "warnings": warnings,
        "details": details,
    }
