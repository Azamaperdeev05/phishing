from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import json

from database import Base, get_db
from main import app
from analyzers.url_analyzer import analyze_url
from analyzers import blacklist_analyzer


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def _register_and_login(client: TestClient, email: str = "user@test.com"):
    password = "StrongPass123!"
    reg = client.post(
        "/api/v1/register",
        json={"email": email, "password": password, "full_name": "Test User"},
    )
    assert reg.status_code == 200

    login = client.post(
        "/api/v1/login",
        data={"username": email, "password": password},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_login_and_history_access_control(client):
    # History must be protected
    history_unauth = client.get("/api/v1/history")
    assert history_unauth.status_code == 401

    headers = _register_and_login(client, "audit-user@test.com")

    # Duplicate registration must fail
    duplicate = client.post(
        "/api/v1/register",
        json={
            "email": "audit-user@test.com",
            "password": "StrongPass123!",
            "full_name": "Another User",
        },
    )
    assert duplicate.status_code == 400

    # Empty history for a new account
    history = client.get("/api/v1/history", headers=headers)
    assert history.status_code == 200
    assert history.json() == []

def test_scan_whitelisted_domain_skips_analyzers(client, monkeypatch):
    headers = _register_and_login(client, "scan-safe@test.com")

    import routers.scan as scan_router

    def fail_if_called(_):
        raise AssertionError("Analyzer should not run for whitelisted domains")

    monkeypatch.setattr(scan_router, "analyze_url", fail_if_called)
    monkeypatch.setattr(scan_router, "analyze_ssl", fail_if_called)
    monkeypatch.setattr(scan_router, "analyze_whois", fail_if_called)
    monkeypatch.setattr(scan_router, "analyze_content", fail_if_called)
    monkeypatch.setattr(scan_router, "analyze_text", fail_if_called)
    monkeypatch.setattr(scan_router, "analyze_ml", fail_if_called)
    monkeypatch.setattr(scan_router, "analyze_blacklist", fail_if_called)

    response = client.post(
        "/api/v1/scan",
        headers=headers,
        json={"url": "google.com", "language": "en"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["domain"] == "google.com"
    assert body["score"] == 100
    assert body["verdict"] == "SAFE"
    assert body["risk_level"] == "LOW"

    history = client.get("/api/v1/history", headers=headers)
    assert history.status_code == 200
    assert len(history.json()) == 1

def test_scan_aggregates_factor_scores(client, monkeypatch):
    import routers.scan as scan_router

    monkeypatch.setattr(
        scan_router,
        "analyze_url",
        lambda _url: {"score": 80, "warnings": ["url-warning"], "details": {}},
    )
    monkeypatch.setattr(
        scan_router,
        "analyze_ssl",
        lambda _url: {"score": 70, "warnings": ["ssl-warning"], "details": {}},
    )
    monkeypatch.setattr(
        scan_router,
        "analyze_whois",
        lambda _url: {"score": 60, "warnings": ["whois-warning"], "details": {}},
    )
    monkeypatch.setattr(
        scan_router,
        "analyze_content",
        lambda _url: {"score": 50, "warnings": ["content-warning"], "details": {}},
    )
    monkeypatch.setattr(
        scan_router,
        "analyze_text",
        lambda _url: {"score": 40, "warnings": ["text-warning"], "details": {}},
    )
    monkeypatch.setattr(
        scan_router,
        "analyze_ml",
        lambda _url: {"score": 90, "warnings": ["ml-warning"], "features": {}},
    )
    monkeypatch.setattr(
        scan_router,
        "analyze_blacklist",
        lambda _url: {"score": 100, "warnings": ["blacklist-warning"], "details": {}},
    )

    response = client.post(
        "/api/v1/scan",
        json={"url": "example-security-check.com", "language": "en"},
    )
    assert response.status_code == 200
    body = response.json()

    assert body["score"] == 72.5
    assert body["verdict"] == "SUSPICIOUS"
    assert body["risk_level"] == "MEDIUM"
    assert body["factors"]["url_analysis"] == 80
    assert body["factors"]["ssl_check"] == 70
    assert len(body["warnings"]) == 7

def test_scan_rejects_invalid_url(client):
    response = client.post(
        "/api/v1/scan",
        json={"url": "https://", "language": "kk"},
    )
    assert response.status_code == 400

def test_url_analyzer_detects_brand_in_subdomain():
    result = analyze_url("https://google.login-safe-example.com/account")
    assert any("Қосалқы доменде танымал бренд атауы табылды" in w for w in result["warnings"])


def test_url_analyzer_detects_sensitive_query_keys():
    result = analyze_url("https://example.com/login?token=abc123&password=secret")
    assert any("Query параметрлерінде құпия дерекке ұқсас кілттер бар" in w for w in result["warnings"])


def test_blacklist_analyzer_uses_threat_feed(tmp_path, monkeypatch):
    payload = {
        "generated_at_utc": "2026-03-05T00:00:00+00:00",
        "source_stats": {},
        "domain_count": 1,
        "domains": ["phishing-example.com"],
    }
    feed_file = tmp_path / "threat_feed_domains.json"
    feed_file.write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(blacklist_analyzer, "THREAT_FEED_PATH", feed_file)
    blacklist_analyzer._load_feed_hosts.cache_clear()

    result = blacklist_analyzer.analyze_blacklist("https://phishing-example.com/login")
    assert result["score"] == 0
    assert result["details"].get("blacklisted_threat_feed") is True
