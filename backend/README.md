# Backend (FastAPI)

## Мақсаты

Backend URL қауіпсіздігін талдайды, score есептейді, verdict шығарады және тарихты сақтайды.

## Орнату

```bash
cd backend
python -m pip install -r requirements.txt
```

## Іске қосу

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Swagger: `http://localhost:8000/docs`

## Негізгі эндпоинттер

- `POST /api/v1/register`
- `POST /api/v1/login`
- `POST /api/v1/scan`
- `GET /api/v1/history`

Толық сипаттама: [API құжаты](../docs/API.md)

## Threat feed жаңарту

```bash
python scripts/update_threat_feeds.py
```

Бұл команда:
- `https://urlhaus.abuse.ch/downloads/text_recent/`
- `https://openphish.com/feed.txt`

фидтерін жүктеп, `backend/data/threat_feed_domains.json` файлын жаңартады.

## Тесттер

```bash
python -m pytest -q
```

## Конфигурация

`backend/config.py` арқылы:

- `PHISHGUARD_SECRET_KEY` (env)
- `GOOGLE_SAFE_BROWSING_API_KEY` (env, optional)
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `DATABASE_URL` (әдепкі: SQLite)

## Маңызды production check-list

- `PHISHGUARD_SECRET_KEY` міндетті түрде қауіпсіз мәнге ауыстыру
- CORS origins-ті нақты домендермен шектеу
- Feed update cron/scheduler орнату
- HTTPS және reverse proxy арқылы жариялау

