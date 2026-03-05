from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ScanResult
from schemas import ScanRequest, ScanResponse, FactorScores
from whitelist import is_whitelisted
from dependencies import get_optional_current_user
from scoring import (
    calculate_score,
    get_verdict,
    get_risk_level,
    get_recommendation,
    WHITELISTED_RECOMMENDATION,
)
from analyzers.url_analyzer import analyze_url
from analyzers.ssl_analyzer import analyze_ssl
from analyzers.whois_analyzer import analyze_whois
from analyzers.content_analyzer import analyze_content
from analyzers.text_analyzer import analyze_text
from analyzers.ml_analyzer import analyze_ml
from analyzers.blacklist_analyzer import analyze_blacklist

router = APIRouter()


@router.post("/scan", response_model=ScanResponse)
def scan_url(
    request: ScanRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user),
):
    url = request.url.strip()

    # Ensure URL has a scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Parse domain
    parsed = urlparse(url)
    domain = parsed.hostname
    if not domain:
        raise HTTPException(status_code=400, detail="URL дұрыс емес / Invalid URL")

    # Check whitelist
    if is_whitelisted(domain):
        factors = FactorScores(
            url_analysis=100,
            ssl_check=100,
            whois_check=100,
            content_analysis=100,
            text_analysis=100,
            ml_analysis=100,
            blacklist_check=100,
        )
        result = ScanResponse(
            url=url,
            domain=domain,
            score=100,
            verdict="SAFE",
            risk_level="LOW",
            factors=factors,
            warnings=[],
            recommendation=WHITELISTED_RECOMMENDATION.get(
                request.language, WHITELISTED_RECOMMENDATION["kk"]
            ),
        )
        # Save to DB
        db_result = ScanResult(
            user_id=current_user.id if current_user else None,
            url=url,
            domain=domain,
            score=100,
            verdict="SAFE",
            risk_level="LOW",
            factors=factors.model_dump(),
            warnings=[],
            recommendation=result.recommendation,
        )
        db.add(db_result)
        db.commit()
        return result

    # Run all analyzers
    url_result = analyze_url(url)
    ssl_result = analyze_ssl(url)
    whois_result = analyze_whois(url)
    content_result = analyze_content(url)
    text_result = analyze_text(url)
    ml_result = analyze_ml(url)
    blacklist_result = analyze_blacklist(url)

    # Aggregate factor scores
    factor_scores = {
        "url_analysis": url_result["score"],
        "ssl_check": ssl_result["score"],
        "whois_check": whois_result["score"],
        "content_analysis": content_result["score"],
        "text_analysis": text_result["score"],
        "ml_analysis": ml_result["score"],
        "blacklist_check": blacklist_result["score"],
    }

    factors = FactorScores(**factor_scores)
    overall_score = calculate_score(factor_scores)
    verdict = get_verdict(overall_score)
    risk_level = get_risk_level(overall_score)
    recommendation = get_recommendation(overall_score, request.language)

    # Collect all warnings
    all_warnings = (
        url_result["warnings"]
        + ssl_result["warnings"]
        + whois_result["warnings"]
        + content_result["warnings"]
        + text_result["warnings"]
        + ml_result["warnings"]
        + blacklist_result["warnings"]
    )

    result = ScanResponse(
        url=url,
        domain=domain,
        score=overall_score,
        verdict=verdict,
        risk_level=risk_level,
        factors=factors,
        warnings=all_warnings,
        recommendation=recommendation,
    )

    # Save to DB
    db_result = ScanResult(
        user_id=current_user.id if current_user else None,
        url=url,
        domain=domain,
        score=overall_score,
        verdict=verdict,
        risk_level=risk_level,
        factors=factors.model_dump(),
        warnings=all_warnings,
        recommendation=recommendation,
    )
    db.add(db_result)
    db.commit()

    return result
