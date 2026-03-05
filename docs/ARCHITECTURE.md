# Architecture

## Жалпы схема

```text
Frontend (Next.js)
  -> POST /scan, /login, /register, GET /history
Backend (FastAPI)
  -> Routers
  -> Analyzers
  -> Scoring engine
  -> SQLite
```

## Backend ағыны (`/scan`)

1. URL normalization (`https://` қосу, parse жасау)
2. Whitelist тексеру
3. Analyzer-лерді іске қосу:
   - `url_analyzer`
   - `ssl_analyzer`
   - `whois_analyzer`
   - `content_analyzer`
   - `text_analyzer`
   - `blacklist_analyzer`
4. Factor score aggregation
5. Final verdict/recommendation есептеу
6. DB-ге сақтау (`scan_results`)

## Мәліметтер қоры

- `users`
- `scan_results`

ORM: SQLAlchemy, DB: SQLite.

## Threat Intelligence

- Локал dataset: `phishing_test_dataset.json`
- Сыртқы фидтерден генерацияланатын файл: `backend/data/threat_feed_domains.json`
- Feed update скрипті: `backend/scripts/update_threat_feeds.py`
