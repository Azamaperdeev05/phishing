# Deploy to Railway

Бұл жоба Railway-де 2 service ретінде деплойланады:

- `backend` (FastAPI)
- `frontend` (Next.js)

## 1) Railway project ашу

1. Railway-ге кіріңіз
2. `New Project` -> `Deploy from GitHub Repo`
3. Осы репоны таңдаңыз

## 2) Backend service баптау

1. `New Service` -> `GitHub Repo`
2. Сол репоны таңдаңыз
3. Service settings:
   - `Root Directory`: `backend`
   - `Config as Code file path`: `/backend/railway.toml`
4. Variables:
   - `PHISHGUARD_SECRET_KEY=<strong-random-secret>`
   - `PHISHGUARD_CORS_ORIGINS=https://<frontend-domain>.up.railway.app`

Егер `Root Directory` қоймай root-тан деплой жасасаңыз, репо түбіріндегі `railway.toml` автоматты түрде backend-ті көтереді.

## 3) Frontend service баптау

1. `New Service` -> `GitHub Repo`
2. Сол репоны таңдаңыз
3. Service settings:
   - `Root Directory`: `frontend`
   - `Config as Code file path`: `/frontend/railway.toml`
4. Variables:
   - `NEXT_PUBLIC_API_BASE_URL=https://<backend-domain>.up.railway.app/api/v1`

## 4) Domain беру

Екі service-ке де `Generate Domain` жасаңыз.

## 5) Verify

- Backend health: `https://<backend-domain>.up.railway.app/`
- Swagger: `https://<backend-domain>.up.railway.app/docs`
- Frontend: `https://<frontend-domain>.up.railway.app`

## Ескерту

- SQLite Railway-де ephemeral болуы мүмкін. Production үшін managed Postgres ұсыныңыз.
- Threat feed жаңартуды scheduled job ретінде іске қосуға болады:
  - `python scripts/update_threat_feeds.py`
