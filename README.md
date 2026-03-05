# PhishGuard

PhishGuard — фишинг сайттарды анықтауға арналған full-stack жоба.  
Жоба URL құрылымы, SSL, WHOIS, HTML/JS контент, мәтіндік паттерндер, ML-эвристика және threat-intel blacklist арқылы талдау жасайды.

Жылдам навигация: [START-HERE.md](./START-HERE.md)

## Негізгі мүмкіндіктер

- URL сканерлеу: `SAFE / SUSPICIOUS / PHISHING`
- Әр фактор бойынша score (0-100)
- Пайдаланушы тіркеу/кіру (JWT)
- Сканерлеу тарихын сақтау
- Threat feed интеграциясы (URLhaus + OpenPhish)
- Web UI (Next.js 16, минималистік Apple-style дизайн)

## Технологиялар

- Backend: FastAPI, SQLAlchemy, Pydantic, JWT
- Frontend: Next.js, React, Tailwind CSS
- DB: SQLite (`backend/phishguard_v2.db`)

## Жылдам іске қосу

### 1) Backend

```bash
cd backend
python -m pip install -r requirements.txt
python scripts/update_threat_feeds.py
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API құжаттамасы: `http://localhost:8000/docs`

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:3000`

## Жоба құрылымы

```text
phishing/
  backend/
    analyzers/           # detection logic
    routers/             # API routes
    scripts/             # feed update scripts
    tests/               # pytest tests
    data/                # generated threat feed data
  frontend/
    src/app/             # pages
    src/components/      # UI components
    src/lib/api.ts       # API client
  docs/
```

## Құжаттама

- [Backend нұсқаулығы](./backend/README.md)
- [Frontend нұсқаулығы](./frontend/README.md)
- [API Reference](./docs/API.md)
- [Архитектура](./docs/ARCHITECTURE.md)
- [Threat Feeds](./docs/THREAT_FEEDS.md)
- [Contributing](./CONTRIBUTING.md)
- [Security](./SECURITY.md)
- [Changelog](./CHANGELOG.md)

## Маңызды ескертулер

- `PHISHGUARD_SECRET_KEY` production ортада міндетті түрде өзгертілуі керек.
- Threat feeds автоматты түрде жаңару үшін `backend/scripts/update_threat_feeds.py` периодты түрде іске қосылсын.
