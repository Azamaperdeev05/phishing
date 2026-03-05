# START HERE

Бұл файл жаңа адамға жобаны 2-3 минутта түсінуге арналған.

## Не бұл?

`PhishGuard` — фишинг сайттарды анықтайтын full-stack жоба.

- `backend/`: талдау логикасы, API, threat feeds
- `frontend/`: веб интерфейс
- `docs/`: архитектура, API және қосымша нұсқаулықтар

## 60 секундта іске қосу

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python scripts/update_threat_feeds.py
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend URL: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:3000`

## Қай файлдарды бірінші оқу керек?

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/API.md`
4. `backend/README.md`
5. `frontend/README.md`

## Жиі қолданылатын терминдер

- `SAFE`: қауіпсіз сайт
- `SUSPICIOUS`: күмәнді сайт
- `PHISHING`: фишинг белгілері анықталған
- `Threat feed`: қауіпті URL тізімі (URLhaus/OpenPhish)
- `Score`: факторлар бойынша жиынтық қауіп ұпайы
- `WHOIS`: домен тіркеу ақпараты
- `Blacklist`: сенімсіз URL/домендер тізімі

## Git бойынша жылдам командалар

```bash
git pull
git checkout -b feature/my-change
git add .
git commit -m "Describe change"
git push -u origin feature/my-change
```

## Мәселе болса

- API ашылмаса: backend logs және `http://localhost:8000/docs` тексеріңіз.
- Frontend дерек әкелмесе: API URL және backend running күйін тексеріңіз.
- Threat анализ әлсіз болса: feed жаңартуын қайта іске қосыңыз.
