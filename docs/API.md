# API Reference

Base URL: `http://localhost:8000/api/v1`

## Auth

### `POST /register`

Жаңа қолданушы тіркеу.

Request:

```json
{
  "email": "user@example.com",
  "password": "StrongPass123!",
  "full_name": "Test User"
}
```

Response `200`:

```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Test User",
  "created_at": "2026-03-05T12:00:00Z"
}
```

### `POST /login`

`application/x-www-form-urlencoded`:

- `username=<email>`
- `password=<password>`

Response `200`:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

## Scan

### `POST /scan`

Auth: optional (`Bearer <token>`)

Request:

```json
{
  "url": "https://example.com",
  "language": "kk"
}
```

Response `200`:

```json
{
  "url": "https://example.com",
  "domain": "example.com",
  "score": 72.5,
  "verdict": "SUSPICIOUS",
  "risk_level": "MEDIUM",
  "factors": {
    "url_analysis": 80,
    "ssl_check": 70,
    "whois_check": 60,
    "content_analysis": 50,
    "text_analysis": 40,
    "ml_analysis": 90,
    "blacklist_check": 100
  },
  "warnings": ["..."],
  "recommendation": "..."
}
```

## History

### `GET /history?limit=20&offset=0`

Auth: required (`Bearer <token>`)

Response `200`:

```json
[
  {
    "id": 1,
    "url": "https://example.com",
    "domain": "example.com",
    "score": 72.5,
    "verdict": "SUSPICIOUS",
    "risk_level": "MEDIUM",
    "scan_date": "2026-03-05T12:05:00Z"
  }
]
```

## Error формат

Көп жағдайда FastAPI стандартты `detail` қайтарады:

```json
{
  "detail": "..."
}
```

