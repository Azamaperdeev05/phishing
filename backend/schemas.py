from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ScanRequest(BaseModel):
    url: str
    deep_scan: bool = False
    language: str = "kk"  # kk, ru, en


class FactorScores(BaseModel):
    url_analysis: float = 0
    ssl_check: float = 0
    whois_check: float = 0
    content_analysis: float = 0
    text_analysis: float = 0
    blacklist_check: float = 0


class ScanResponse(BaseModel):
    url: str
    domain: str
    score: float
    verdict: str  # SAFE, SUSPICIOUS, PHISHING
    risk_level: str  # LOW, MEDIUM, HIGH
    factors: FactorScores
    warnings: list[str]
    recommendation: str

    class Config:
        from_attributes = True


class HistoryItem(BaseModel):
    id: int
    url: str
    domain: str
    score: float
    verdict: str
    risk_level: str
    scan_date: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
