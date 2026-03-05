from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    scans = relationship("ScanResult", back_populates="user")


class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Optional link to user
    url = Column(String(2048), nullable=False)
    domain = Column(String(255), nullable=False)
    score = Column(Float, nullable=False)  # 0-100
    verdict = Column(String(20), nullable=False)  # SAFE, SUSPICIOUS, PHISHING
    risk_level = Column(String(10), nullable=False)  # LOW, MEDIUM, HIGH
    factors = Column(JSON, nullable=False)  # Individual factor scores
    warnings = Column(JSON, nullable=False)  # List of warning messages
    recommendation = Column(Text, nullable=True)
    scan_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="scans")
