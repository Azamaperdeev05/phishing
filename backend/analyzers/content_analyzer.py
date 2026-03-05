import re
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT


def analyze_content(url: str) -> dict:
    """Analyze website HTML content for phishing indicators."""
    score = 100
    warnings = []
    details = {}

    parsed = urlparse(url)
    base_domain = parsed.hostname or ""

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, timeout=REQUEST_TIMEOUT, headers=headers, verify=False)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
    except requests.RequestException as e:
        return {
            "score": 50,
            "warnings": [f"Сайт мазмұнын алу мүмкін болмады: {str(e)[:80]}"],
            "details": {"accessible": False},
        }

    details["accessible"] = True
    details["status_code"] = response.status_code

    # 1. Login forms detection
    password_inputs = soup.find_all("input", attrs={"type": "password"})
    email_inputs = soup.find_all("input", attrs={"type": re.compile(r"email|text", re.I)})
    forms = soup.find_all("form")

    details["has_login_form"] = len(password_inputs) > 0
    details["form_count"] = len(forms)
    details["password_fields"] = len(password_inputs)

    if password_inputs:
        score -= 10  # Having a login form itself is not bad, but suspicious in context
        warnings.append(f"Сайтта құпия сөз енгізу формасы табылды ({len(password_inputs)} дана)")

    # 2. External form actions (data exfiltration)
    for form in forms:
        action = form.get("action", "")
        if action:
            action_url = urljoin(url, action)
            action_domain = urlparse(action_url).hostname or ""
            if action_domain and action_domain != base_domain:
                score -= 30
                warnings.append(f"Форма деректерді сыртқы серверге жібереді: {action_domain}")
                details["external_form_action"] = action_domain

    # 3. JavaScript analysis
    scripts = soup.find_all("script")
    js_content = " ".join(s.string or "" for s in scripts)

    # eval() usage
    eval_count = js_content.lower().count("eval(")
    if eval_count > 0:
        score -= 15
        warnings.append(f"JavaScript-те eval() функциясы қолданылған ({eval_count} рет)")
        details["eval_usage"] = eval_count

    # base64 encoding in JS
    if "atob(" in js_content or "btoa(" in js_content:
        score -= 10
        warnings.append("JavaScript-те base64 кодтау табылды")
        details["base64_in_js"] = True

    # Obfuscated JS (high entropy, lots of hex/unicode escapes)
    hex_escapes = len(re.findall(r"\\x[0-9a-fA-F]{2}", js_content))
    unicode_escapes = len(re.findall(r"\\u[0-9a-fA-F]{4}", js_content))
    if hex_escapes + unicode_escapes > 20:
        score -= 20
        warnings.append("Обфускацияланған JavaScript код табылды")
        details["obfuscated_js"] = True

    # Keylogger indicators
    keylogger_patterns = ["onkeypress", "onkeydown", "onkeyup", "addEventListener('key"]
    for pattern in keylogger_patterns:
        if pattern in js_content.lower() or pattern in html.lower():
            score -= 20
            warnings.append("Пернетақта оқиғаларын тыңдау табылды (keylogger белгісі)")
            details["keylogger_indicator"] = True
            break

    # 4. Hidden iframes
    iframes = soup.find_all("iframe")
    hidden_iframes = []
    for iframe in iframes:
        style = iframe.get("style", "")
        width = iframe.get("width", "")
        height = iframe.get("height", "")
        if ("display:none" in style.replace(" ", "") or
            "visibility:hidden" in style.replace(" ", "") or
            width in ("0", "1") or height in ("0", "1")):
            hidden_iframes.append(iframe.get("src", "unknown"))

    if hidden_iframes:
        score -= 20
        warnings.append(f"Жасырын iframe табылды ({len(hidden_iframes)} дана)")
        details["hidden_iframes"] = len(hidden_iframes)

    # 5. External resources count
    external_links = []
    for tag in soup.find_all(["a", "link", "script", "img"]):
        href = tag.get("href") or tag.get("src") or ""
        if href.startswith(("http://", "https://")):
            link_domain = urlparse(href).hostname or ""
            if link_domain and link_domain != base_domain:
                external_links.append(link_domain)

    details["external_resources"] = len(external_links)
    if len(external_links) > 20:
        score -= 5
        warnings.append(f"Көп сыртқы ресурстар: {len(external_links)} сілтеме")

    # 6. Meta tags check
    title_tag = soup.find("title")
    details["title"] = title_tag.string.strip() if title_tag and title_tag.string else ""

    favicon = soup.find("link", rel=re.compile(r"icon", re.I))
    if favicon:
        favicon_href = favicon.get("href", "")
        if favicon_href.startswith(("http://", "https://")):
            fav_domain = urlparse(favicon_href).hostname or ""
            if fav_domain and fav_domain != base_domain:
                score -= 15
                warnings.append(f"Favicon сыртқы домендерден жүктелген: {fav_domain}")
                details["external_favicon"] = fav_domain

    # 7. Redirect check
    if len(response.history) > 2:
        score -= 10
        warnings.append(f"Көп бағыттау (redirect) табылды: {len(response.history)} рет")
        details["redirects"] = len(response.history)

    return {
        "score": max(0, score),
        "warnings": warnings,
        "details": details,
    }
