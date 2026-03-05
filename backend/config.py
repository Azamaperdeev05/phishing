import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'phishguard_v2.db'}"

# Google Safe Browsing API key (optional)
GOOGLE_SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY", "")

# Request timeout for fetching sites
REQUEST_TIMEOUT = 10

# CORS origins
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.8.3:3000",  # Network IP from terminal
    "*",  # Allow all for dev
]

# Auth settings
SECRET_KEY = os.getenv(
    "PHISHGUARD_SECRET_KEY", "your-super-secret-key-change-it-in-prod"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
